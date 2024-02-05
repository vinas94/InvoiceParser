import json
import pandas as pd

from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import document_processor_service


def process_document(file_path, client, config):

    # Load the file content
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Construct the request
    request = document_processor_service.ProcessRequest(
        name=config["processor_name"],
        raw_document=documentai.RawDocument(content=file_content, mime_type=config["mime_type"])
    )

    # Process the document
    result = client.process_document(request=request)
    result_json = json.loads(documentai.Document.to_json(result.document))

    return result_json["entities"]


def parse_entities(entities):

    # First, let's find the date
    date = None
    ndate = None
    for entity in entities:
        if entity["type"] == "Datum":
            date = entity["mentionText"]
            if "normalizedValue" in entity:
                ndate = entity["normalizedValue"]["text"]
            break

    # Next, let's parse line items
    items = []
    for entity in entities:
        if entity["type"] != "Line_item":
            continue

        price = None
        nprice = None
        article = None
        properties = entity["properties"]
        for property_ in properties:

            if property_["type"] == "Preis" and price is None:
                price = property_["mentionText"]
                if "normalizedValue" in property_:
                    nprice = property_["normalizedValue"]["text"]
                    nprice = float(nprice.split(" ")[0])

            if property_["type"] == "Artikel" and article is None:
                article = property_["mentionText"]

        item = {"date": date, "ndate": ndate, "article": article, "price": price, "nprice": nprice}
        items.append(item)

    # Finally, return a dataframe
    return pd.DataFrame(items)
