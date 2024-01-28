import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from PIL import Image as PILImage

# Export given data to PDF
def export_pdf(dir, title, content):
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

        flowables = add_title(flowables, title)
        
        passed_data = content.keys()

        if "thumbnail" in passed_data:
            flowables = add_thumbnail(flowables, content["thumbnail"])
        if "images" in passed_data:
            flowables = add_images_table(flowables, content["images"])
        if "text" in passed_data:
            flowables = add_text(flowables, content["text"])
        if "source" in passed_data:
            flowables = add_text(flowables, content["source"])

        pdf.build(flowables)

        print("{}.pdf saved in {}".format(title, dir))
    except Exception as e:
        print("Failed to export to PDF")
        print(e)

def add_title(flowables, text):
    styles = getSampleStyleSheet()
    flowables.append(Paragraph(text, styles["Title"]))

    return flowables

def add_thumbnail(flowables, image):
    x, y = calculate_image_dimensions(image, 200)
    flowables.append(ReportLabImage(BytesIO(image), x, y))

    return flowables

def add_images_table(flowables, images):
    images_table = [[]]

    for image in images:
        x, y = calculate_image_dimensions(image, 350 / len(images))
        images_table[0].append(ReportLabImage(BytesIO(image), x, y))

    flowables.append(Table(data = images_table, style = TableStyle([("VALIGN", (-1, -1), (-1, -1), "MIDDLE")])))

    return flowables

def add_text(flowables, text):
    styles = getSampleStyleSheet()
    text = text.replace("\n", "<br/><br/>")
    flowables.append(Paragraph(text, styles["BodyText"]))

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