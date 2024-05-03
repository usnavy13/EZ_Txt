#%%
from dotenv import load_dotenv
import os
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
import gradio as gr

load_dotenv()

client = UnstructuredClient(
    api_key_auth=os.getenv("unstruct_api_key"),
    # you may need to provide your unique API URL
    # server_url="YOUR_API_URL",
)

def text_extract(filename):
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
    
with gr.Blocks() as demo:
    gr.Markdown("# Extract text from a document!")
    with gr.Row():
        file = gr.File(label="Upload a file",
                       file_types=['.eml', '.html', '.md', '.msg', '.rst', '.rtf', '.txt', '.xml', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.heic', '.csv', '.doc', '.docx', '.epub', '.odt', '.pdf', '.ppt', '.pptx', '.tsv', '.xlsx'])
        run = gr.Button(value="Extract text")
    with gr.Row():
        text = gr.Textbox(label="Extracted Text!",
                          show_copy_button=True)
    
    run.click(text_extract, file, outputs=text)

demo.launch(share=False, server_name="0.0.0.0", show_api=False)





    



# %%
