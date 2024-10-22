import PyPDF2

file_path = "C:\\Users\\Moses\\Downloads\\ni-zingahe_.pdf"

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Initialize a variable to hold all the extracted text
        extracted_text = ''
        
        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()
        
        return extracted_text

# Path to your PDF file

# Extract the text
pdf_text = extract_text_from_pdf(file_path)

# Print or save the extracted text
print(pdf_text)

# Optionally, save the extracted text to a file
with open('extracted_text.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(pdf_text)
