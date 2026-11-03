import io
from pypdf import PdfWriter
from pdfjin_ai_chat.core import extract_pdf_text


def test_extract_pdf_text():
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    buf = io.BytesIO()
    writer.write(buf)

    text = extract_pdf_text(buf.getvalue())
    assert isinstance(text, str)
