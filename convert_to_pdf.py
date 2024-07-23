import base64
import re
import markdown2
import pdfkit
from bs4 import BeautifulSoup

# Convert Markdown to HTML
with open('README.md', 'r') as file:
    markdown_text = file.read()
html = markdown2.markdown(markdown_text)

# Convert images to base64
def convert_images_to_base64(html):
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            try:
                # Read image file and encode to base64
                img_data = open(img_url, 'rb').read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                img['src'] = f"data:image/jpeg;base64,{img_base64}"
            except Exception as e:
                print(f"Error processing image {img_url}: {e}")
    return str(soup)

# Update HTML with embedded images
html_with_images = convert_images_to_base64(html)

# Path to wkhtmltopdf executable (update this path as needed)
path_to_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Adjust if needed

# Create a PDFKit configuration
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Convert HTML to PDF
pdfkit.from_string(html_with_images, 'output.pdf', configuration=config)
