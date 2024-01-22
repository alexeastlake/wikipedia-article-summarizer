import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from PIL import Image as PILImage

# Export given data to PDF
def export_pdf(dir, title, text, thumbnail, images, url):
    try:
        print("Exporting to PDF...")

        # Creates output directory if not found
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("Output directory {} created\n".format(dir))

        # PDF setup
        output_path = os.path.join(dir, "{}.pdf".format(title))
        pdf = SimpleDocTemplate(filename = output_path, pagesize = A4)
        flowables = []

        # Adds title if given title
        if title:
            flowables = add_title(flowables, title)
        
        # Adds thumbnail image if given thumbnail
        if thumbnail:
            flowables = add_thumbnail(flowables, thumbnail)
        
        # Adds the smaller image row if given images
        if images:
            flowables = add_images_table(flowables, images)
        
        # Adds text if given text
        if text:
            flowables = add_text(flowables, text)

        # Adds a source URL if given url
        if url:
            flowables = add_text(flowables, url)

        pdf.build(flowables)

        print("{}.pdf saved in {}".format(title, dir))
    except Exception as e:
        print("Failed to export to PDF")
        print(e)

def add_title(flowables, text):
    styles = getSampleStyleSheet()
    flowables.append(Paragraph(text, styles["Title"]))
    print("Added title\n")

    return flowables

def add_thumbnail(flowables, image):
    x, y = calculate_image_dimensions(image, 200)
    flowables.append(ReportLabImage(BytesIO(image), x, y))
    print("Added thumbnail\n")

    return flowables

def add_images_table(flowables, images):
    images_table = [[]]

    for image in images:
        x, y = calculate_image_dimensions(image, 350 / len(images))
        images_table[0].append(ReportLabImage(BytesIO(image), x, y))
        print("Added image to table\n")

    flowables.append(Table(data = images_table, style = TableStyle([("VALIGN", (-1, -1), (-1, -1), "MIDDLE")])))
    print("Added images table\n")

    return flowables

def add_text(flowables, text):
    styles = getSampleStyleSheet()
    text = text.replace("\n", "<br/><br/>")
    flowables.append(Paragraph(text, styles["BodyText"]))
    print("Added paragraph\n")

    return flowables

# Calculates resized image dimensions retaining the original aspect ratio, based on the desired largest side
def calculate_image_dimensions(image, largest_side):
    old_x, old_y = PILImage.open(BytesIO(image)).size

    if old_x >= old_y:
        new_y = (old_y / old_x) * largest_side
        
        return largest_side, new_y
    else:
        new_x = (old_x / old_y) * largest_side
        
        return new_x, largest_side