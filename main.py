import os
import json
import pandas as pd

from tqdm import tqdm
from datetime import datetime
from src.google_client import get_documentai_client
from src.document_processor import process_document, parse_entities


def main():

    # Read config
    with open("./config.json") as f:
        config = json.load(f)

        input_dir = config["input_dir"]
        output_dir = config["output_dir"]

    # Set up the Document AI client
    client = get_documentai_client(config)

    # Get document file paths
    file_paths = [os.path.join(input_dir, x) for x in os.listdir(input_dir) if x.endswith(".pdf")]
    if not file_paths:
        print("No PDF files found in the input directory. Terminating!")
        return

    # Process the documents
    dfs = []
    for file_path in (pbar := tqdm(file_paths)):
        pbar.set_postfix_str(f"processing {(document := file_path.split('/')[-1])}")

        entities = process_document(file_path, client, config)
        df = parse_entities(entities)
        df["document"] = document

        dfs.append(df)

    # Combine the results and save to a CSV file
    output_file = f"result_{datetime.strftime(datetime.now(), '%Y%m%dT%H%M%S')}.csv"
    df = pd.concat(dfs).sort_values(["ndate", "date", "document", "article", "nprice", "price"])
    df.to_csv(os.path.join(output_dir, output_file), index=False)


if __name__ == "__main__":
    main()
