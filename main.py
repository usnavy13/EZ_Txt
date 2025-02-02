#%%
from dotenv import load_dotenv
import os
import gradio as gr
from markitdown import MarkItDown
import tiktoken
from azure_document_intelligence import extract_markdown_from_file

load_dotenv()

# Initialize MarkItDown
markitdown = MarkItDown()

def extract_text(file_path, method):
    """Extract text from a document using the selected method and count tokens"""
    try:
        if method == "Azure Document Intelligence":
            text = extract_markdown_from_file(file_path)
        else:
            result = markitdown.convert(file_path)
            text = result.text_content
        
        # Count tokens using tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")  # Using OpenAI's encoding
        token_count = len(encoding.encode(text))
        
        return [text, f"{token_count:,} tokens"]
    except Exception as e:
        return [f"Error: {str(e)}", "0 tokens"]

with gr.Blocks(title="EZ Text Extractor") as demo:
    gr.Markdown("# Extract text from a document!")
    with gr.Row():
        file = gr.File(label="Upload a file",
                      file_types=['.pdf', '.pptx', '.docx', '.xlsx', 
                                '.png', '.jpg', '.jpeg', '.html', 
                                '.txt', '.csv', '.json', '.xml', '.zip'])
    with gr.Row():
        method = gr.Radio(choices=["MarkItDown", "Azure Document Intelligence"], label="Extraction Method", value="MarkItDown")
    with gr.Row():
        run = gr.Button(value="Extract text")
    with gr.Row():
        token_count = gr.Textbox(label="Token Count",
                        show_copy_button=True)    
    with gr.Row():
        text = gr.Textbox(label="Extracted Text!",
                         show_copy_button=True)

    
    run.click(extract_text, inputs=[file, method], outputs=[text, token_count])

# Optional settings from environment variables
username = os.getenv("user")
password = os.getenv("password")
show_api = os.getenv("show_api", "false").lower() == "true"
auth = None if not (username and password) else (username, password)

demo.launch(share=False, server_name="0.0.0.0", show_api=show_api, auth=auth)

# %%
