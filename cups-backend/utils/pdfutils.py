import base64
import io
import sys
from typing import List
import PyPDF2
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

PARCEL_LABEL = (4.126 * inch, 5.835 * inch)
GLS_TEXT_POS = (8 * mm, 65 * mm)

# sudo apt-get install fonts-wqy-zenhei
if sys.platform == 'linux':
    pdfmetrics.registerFont(TTFont('noto', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
    FONT = 'noto'
elif sys.platform == 'win32':
    pdfmetrics.registerFont(TTFont('simsun', 'C:/Windows/Fonts/SimSun.ttc'))
    FONT ='simsun'

def create_watermark_text(watermark_text: str,
                          font_size: int = 8,
                          position: tuple = (100, 100),
                          font_color: tuple = (0, 0, 0),
                          page_size: tuple = PARCEL_LABEL) -> bytes:
    """
    Creates a watermark text as a PDF file.
    :param page_size:
    :param watermark_text:  The watermark text to create.
    :param font_size:  The font size of the watermark text.
    :param font_color:  The font color of the watermark text.
    :param position:  The position of the watermark text on the page.
    :return:  The watermark text as a PDF file as bytes.
    """
    packet = io.BytesIO()
    font = FONT
    can = canvas.Canvas(packet, pagesize=page_size, bottomup=0)
    can.setFont(font, font_size)
    can.setFillColorRGB(*font_color)
    x, y = position
    textObj = can.beginText(x, y)
    textObj.setFont(font, font_size)
    for line in watermark_text.split('\n'):
        textObj.textLine(line.strip())
    can.drawText(textObj)
    can.save()
    packet.seek(0)
    return packet.read()


def concat_pdfs(pdf_bytes_list: List[bytes]) -> bytes:
    """
    Concatenates multiple PDF files into one PDF file.
    :param pdf_bytes_list:  A list of PDF files as bytes.
    :return:  The merged PDF file as bytes.
    """
    pdf_writer = PyPDF2.PdfWriter()
    for pdf_bytes in pdf_bytes_list:
        with io.BytesIO(pdf_bytes) as fp:
            pdf_reader = PyPDF2.PdfReader(fp)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
    concat_pdf_bytes = io.BytesIO()
    pdf_writer.write(concat_pdf_bytes)
    return concat_pdf_bytes.getvalue()


def add_watermark(pdf_bytes: bytes,
                  watermark_text: str,
                  **kwargs) -> bytes:
    """
    Adds a watermark to a PDF file.
    :param pdf_bytes:  The PDF file as bytes.
    :param watermark_text:  The watermark text to add to the PDF file.
    :return:  The PDF file with the watermark added as bytes.
    """
    watermark_pdf_bytes = create_watermark_text(watermark_text=watermark_text, **kwargs)
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    watermark_pdf_reader = PyPDF2.PdfReader(io.BytesIO(watermark_pdf_bytes))
    pdf_writer = PyPDF2.PdfWriter()
    watermark_page = watermark_pdf_reader.pages[0]
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)
    watermarked_pdf_bytes = io.BytesIO()
    pdf_writer.write(watermarked_pdf_bytes)
    return watermarked_pdf_bytes.getvalue()

def add_watermark_auto_position(pdf_bytes: bytes,
                                watermark_text: str,
                                font_size: int = 8,
                                font_color: tuple = (0, 0, 0)) -> bytes:
    """
    Adds a watermark to a PDF file with automatic positioning at bottom left.
    :param pdf_bytes: 
    :param watermark_text: 
    :param font_size: 
    :return: 
    """
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    page0 = pdf_reader.pages[0]
    page_width = float(page0.mediabox.width)
    page_height = float(page0.mediabox.height)
    position = (15, page_height - 12)
    watermark_pdf_bytes = add_watermark(pdf_bytes=pdf_bytes,
                                        watermark_text=watermark_text,
                                        font_size=font_size,
                                        page_size=(page_width, page_height),
                                        font_color=font_color,
                                        position=position)
    return watermark_pdf_bytes

if __name__ == '__main__':
    # Example usage
    watermark_text = "77050p[;'üÄ77050新77050新77050新77050新"
    with open(r'F:\Download\77050.pdf', 'rb') as f:
        pdf_bytes = f.read()
        watermarked_pdf_bytes = add_watermark_auto_position(pdf_bytes=pdf_bytes,
                                                            watermark_text=watermark_text,
                                                            font_color=(0.3, 0.3, 0.3),
                                                             font_size=8)
    with open(r'F:\Download\watermarked.pdf', 'wb') as f:
        f.write(watermarked_pdf_bytes)
