import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from PIL import Image as PILImage

def export_pdf(dir, title, text, thumbnail, images):
    try:
        print("Exporting to PDF...")

        if not os.path.exists(dir):
            os.makedirs(dir)
            print("Output directory {} created\n".format(dir))

        output_path = os.path.join(dir, "{}.pdf".format(title))

        pdf = SimpleDocTemplate(filename = output_path, pagesize = A4)
        styles = getSampleStyleSheet()

        flowables = [Paragraph(title, styles["Title"])]
        print("Added title\n")
        
        if thumbnail:
            x, y = calculate_image_dimensions(thumbnail, 200)

            flowables.append(ReportLabImage(BytesIO(thumbnail), x, y))
            print("Added thumbnail\n")
            
        if images:
            images_table = [[]]

            for image in images:
                print(image[:20])
                x, y = calculate_image_dimensions(image, 350 / len(images))

                images_table[0].append(ReportLabImage(BytesIO(image), x, y))
                print("Added image\n")

            flowables.append(Table(data = images_table, style = TableStyle([("VALIGN", (-1, -1), (-1, -1), "MIDDLE")])))
        
        flowables.append(Paragraph(text, styles["BodyText"]))
        print("Added paragraph\n")

        pdf.build(flowables)

        print("{}.pdf saved in {}\n".format(title, dir))
    except Exception as e:
        print("Failed to export to PDF")
        print(e)

def calculate_image_dimensions(image, largest_side):
    old_x, old_y = PILImage.open(BytesIO(image)).size

    if old_x >= old_y:
        new_y = (old_y / old_x) * largest_side
        
        return largest_side, new_y
    else:
        new_x = (old_x / old_y) * largest_side
        
        return new_x, largest_side