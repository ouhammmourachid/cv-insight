import PyPDF2


def pdf_to_text(pdf_file):
    with open(pdf_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ''
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            page_text = page.extract_text()
            text += page_text
    return text

