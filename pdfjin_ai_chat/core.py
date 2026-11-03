import os
import io
from pathlib import Path
from typing import Union, BinaryIO, Optional
from pypdf import PdfReader


def extract_pdf_text(content: bytes, max_chars: int = 100000) -> str:
    reader = PdfReader(io.BytesIO(content))
    text = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text.append(t)
    return "\n".join(text)[:max_chars]


def chat_with_pdf(
    input_pdf: Union[str, Path, bytes, BinaryIO],
    question: str,
    api_key: Optional[str] = None,
) -> str:
    """
    Ask a question about a PDF document using Google Gemini.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is required. Pass api_key or set environment variable.")

    if isinstance(input_pdf, (str, Path)):
        with open(input_pdf, "rb") as f:
            pdf_bytes = f.read()
    elif isinstance(input_pdf, bytes):
        pdf_bytes = input_pdf
    else:
        pdf_bytes = input_pdf.read()

    document_text = extract_pdf_text(pdf_bytes)

    import google.generativeai as genai
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are a helpful PDF document assistant. Use the document excerpt below to answer the user's question accurately.

Document Context:
{document_text}

User Question:
{question}
"""
    response = model.generate_content(prompt)
    return response.text
