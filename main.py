import datetime
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def generate_pdf():
    # URL of the website
    url = "https://daffodilvarsity.edu.bd/department/swe/notice"

    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all notice links within the page
    notice_links = soup.find_all('h3', class_='heading')

    # Extract notice titles and links
    titles = [link.a.text.strip() for link in notice_links]
    links = [link.a['href'] for link in notice_links]

    # Get today's date
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Define the table data
    data = [['Title', 'Link']]  # Headers

    # Add notice titles and links to the table data
    for title, link in zip(titles, links):
        data.append([title, link])

    # Create PDF
    pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if pdf_file:
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        # Create table
        table = Table(data)

        # Add style to table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)

        # Add table to the PDF
        doc.build([table])

        messagebox.showinfo("Success", f"PDF file saved successfully at:\n{pdf_file}")
        app.destroy()  # Close the application window


# Create Tkinter app
app = tk.Tk()
app.title("PDF Generator")

# Create generate button
generate_button = tk.Button(app, text="Generate PDF", command=generate_pdf)
generate_button.pack(pady=10)

# Run the app
app.mainloop()
