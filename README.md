# EZ_Txt

A simple web application to extract text from various document formats using MarkItDown.

## Features

- Extract text from multiple document formats including PDF, Office documents, images, and more
- Simple web interface using Gradio
- Optional authentication
- Optional API visibility

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Docker

You can run EZ_Txt using the pre-built Docker container:

```bash
docker pull ghcr.io/usnavy13/ez-txt:latest
docker run -p 7860:7860 ghcr.io/usnavy13/ez-txt:latest
```

Then access the application at `http://localhost:7860`

## Configuration

Create a `.env` file in the root directory with the following optional settings:

```env
# Optional authentication (remove or leave empty to disable)
user=your_username
password=your_password

# Optional API visibility (default: false)
show_api=false
```

### Azure Document Intelligence Integration

To use Azure Document Intelligence for text extraction, ensure you have an active Azure subscription and a Document Intelligence resource. Then, add the following entries to your `.env` file:

```env
AZURE_ENDPOINT=https://<your-azure-endpoint>
AZURE_API_KEY=<your-azure-api-key>
```

The application will automatically enable the "Azure Document Intelligence" extraction method when both variables are present. Make sure the environment variable names match those expected by the code.

## Usage

1. Run the application:
```bash
python main.py
```

2. Open your browser and navigate to `http://localhost:7860`
3. Upload a document and click "Extract text" to get the text content

## Supported File Types

- Documents: PDF, PPTX, DOCX, XLSX
- Images: PNG, JPG, JPEG
- Text: TXT, CSV, JSON, XML, HTML
- Archives: ZIP (will process contained files)

