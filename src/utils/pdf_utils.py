import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from PIL import Image as PILImage
#import cairosvg


def export_pdf(dir, title, text, images):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)

        output_path = os.path.join(dir, "{}.pdf".format(title))

        pdf = SimpleDocTemplate(filename = output_path, pagesize = A4)

        styles = getSampleStyleSheet()

        flowables = [Paragraph(title, styles["Title"])]

        images_table = [[]]

        for image in images:
            old_x, old_y = PILImage.open(BytesIO(image)).size
            
            new_x = 400 / len(images)
            new_y = (old_y / old_x) * new_x

            images_table[0].append(ReportLabImage(BytesIO(image), new_x, new_y))

        flowables.append(Table(images_table))
        flowables.append(Paragraph(text, styles["BodyText"]))

        pdf.build(flowables)

        print("{}.pdf saved in {}".format(title, dir))
    except Exception as e:
        print(e)