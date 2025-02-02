import os
import time
import mimetypes
import requests


def extract_markdown_from_file(file_path: str) -> str:
    """
    Extracts text from a document using Azure Document Intelligence and returns its markdown representation.

    References:
    - [Azure AI Services Blog](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/analyze-complex-documents-with-azure-document-intelligence-markdown-output-and-a/4080770)
    - [Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0&tabs=rest%2Csample-code#output-to-markdown-format)
    
    The function reads the file, sends it to the Azure endpoint, polls for the result, and returns the markdown content.
    
    Environment Variables:
        AZURE_ENDPOINT: The Azure Document Intelligence endpoint URL.
        AZURE_KEY: The subscription key for authentication.
    
    Parameters:
        file_path (str): The local path to the document file.
    
    Returns:
        str: The markdown content extracted from the document.
    
    Raises:
        ValueError: If required environment variables are not set.
        Exception: For HTTP errors, or if analysis fails or times out.
    """
    # Retrieve endpoint and key from environment
    endpoint = os.environ.get("AZURE_ENDPOINT")
    key = os.environ.get("AZURE_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_ENDPOINT and AZURE_KEY must be set in environment variables.")

    # Remove trailing slash if present
    endpoint = endpoint.rstrip('/')

    # Determine the file's mimetype; default to PDF if unknown
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/pdf"

    # Construct the analysis URL with markdown output parameter
    url = f"{endpoint}/formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31&outputContentFormat=markdown"

    headers = {
        "Content-Type": content_type,
        "Ocp-Apim-Subscription-Key": key
    }

    # Read the file in binary mode
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Initiate the analysis request
    response = requests.post(url, headers=headers, data=file_data)
    if response.status_code != 202:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")

    # Retrieve the operation-location header for polling results
    operation_url = response.headers.get("operation-location")
    if not operation_url:
        raise Exception("Operation location header not found in the response.")

    # Poll for the result
    max_retries = 20
    for _ in range(max_retries):
        time.sleep(1)  # wait a second before polling
        status_response = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": key})
        status_json = status_response.json()

        status = status_json.get("status")
        if status == "succeeded":
            # Return the markdown content from the analyzeResult
            return status_json["analyzeResult"].get("content", "")
        elif status == "failed":
            raise Exception("Document analysis failed.")

    raise Exception("Timed out waiting for the analysis result.") 

#print(extract_markdown_from_file("test.pdf"))