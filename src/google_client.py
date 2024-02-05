import os

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def get_documentai_client(config):

    # Set the path to the service account key
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join("./secrets", config["service_account_key"])

    # Initiate the client
    client_options = ClientOptions(api_endpoint=config["endpoint"])
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    return client
