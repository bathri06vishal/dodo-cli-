#!/usr/bin/env python3
"""
Generate PDF documentation from markdown file.
"""

import markdown
import pdfkit
from pathlib import Path

def generate_pdf():
    """Convert markdown documentation to PDF."""
    
    # Read markdown file
    md_file = Path('/home/user/test_dodo/DODO_Documentation.md')
    pdf_file = Path('/home/user/test_dodo/DODO_Documentation.pdf')
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'toc', 'codehilite'])
    
    # Add CSS styling for better PDF appearance
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>DODO Documentation</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #2c3e50;
                margin-top: 30px;
                margin-bottom: 15px;
            }}
            h1 {{
                font-size: 28px;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                font-size: 22px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 8px;
            }}
            h3 {{
                font-size: 18px;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 5px;
            }}
            code {{
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 2px 4px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 16px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 0;
                padding-left: 20px;
                color: #7f8c8d;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            .toc {{
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .toc ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            .toc li {{
                margin: 5px 0;
            }}
            .toc a {{
                text-decoration: none;
                color: #3498db;
            }}
            .toc a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Configure PDF options
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    
    try:
        # Convert HTML to PDF
        pdfkit.from_string(styled_html, str(pdf_file), options=options)
        print(f"✅ PDF generated successfully: {pdf_file}")
        print(f"📄 File size: {pdf_file.stat().st_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print("💡 Make sure wkhtmltopdf is installed:")
        print("   sudo apt-get install wkhtmltopdf  # Ubuntu/Debian")
        print("   brew install wkhtmltopdf        # macOS")

if __name__ == "__main__":
    generate_pdf()
