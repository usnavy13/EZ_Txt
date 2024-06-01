#%%
from dotenv import load_dotenv
import os
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
import gradio as gr

load_dotenv()

azure_doc_intel_endpoint = os.getenv("azure_doc_intel_endpoint")
azure_doc_intel_key = os.getenv("azure_doc_intel_key")
unstruct_api_key = os.getenv("unstruct_api_key")

client = UnstructuredClient(
    api_key_auth=unstruct_api_key,)
    # you may need to provide your unique API URL
    # server_url="YOUR_API_URL",


def azure_text_extract(file_path):
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=azure_doc_intel_endpoint, api_key=azure_doc_intel_key, file_path=file_path, api_model="prebuilt-layout")

    documents = loader.load()
    text = documents[0].page_content
    return text



def unstruct_text_extract(filename):
    file = open(filename, "rb")
    req = shared.PartitionParameters(
        # Note that this currently only supports a single file
        files=shared.Files(
            content=file.read(),
            file_name=filename,
        ),
        # Other parameters
        strategy="hi_res",
    )

    try:
        res = client.general.partition(req)
        full_text = ' '.join([x['text'] for x in res.elements])
        return full_text
    except SDKError as e:
        return f"Error: {e}"
    

def text_extract_manager(file):
    # Check if azure_doc_intel_key and azure_doc_intel_endpoint are non-empty strings
    AZURE_SETUP = bool(azure_doc_intel_key) and bool(azure_doc_intel_endpoint)
    UNSTRUCT_SETUP = bool(unstruct_api_key)
    print(AZURE_SETUP, UNSTRUCT_SETUP)
    if AZURE_SETUP and UNSTRUCT_SETUP:
        selected = os.getenv("service")
        print(selected)
        if selected == "azure":

            return azure_text_extract(file)
        elif selected == "unstruct":
  
            return unstruct_text_extract(file)
    elif AZURE_SETUP:

        return azure_text_extract(file)
    elif UNSTRUCT_SETUP:

        return unstruct_text_extract(file)
    
with gr.Blocks(title="EZ Text Extractor") as demo:
    gr.Markdown("# Extract text from a document!")
    with gr.Row():
        file = gr.File(label="Upload a file",
                       file_types=['.eml', '.html', '.md', '.msg', '.rst', '.rtf', '.txt', '.xml', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.heic', '.csv', '.doc', '.docx', '.epub', '.odt', '.pdf', '.ppt', '.pptx', '.tsv', '.xlsx'])
        run = gr.Button(value="Extract text")
    with gr.Row():
        text = gr.Textbox(label="Extracted Text!",
                          show_copy_button=True)
    
    run.click(text_extract_manager, file, outputs=text)


username = os.getenv("user")
password = os.getenv("password")
demo.launch(share=False, server_name="0.0.0.0", show_api=False, auth=(username, password))

# %%
