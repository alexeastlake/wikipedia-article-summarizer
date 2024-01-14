import os
import sys
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def main():
    args = sys.argv

    try:
        if ((len(args) != 2) or (type(args[1]) != str)):
            raise ValueError("Invalid arguments: Must pass 1 string article name")
    except Exception as e:
        print(e)
        exit()

    searchTerm = args[1]
    
    article = get_article(searchTerm = searchTerm)
    
    outputDir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "output"))

    export_pdf(dir = outputDir, title = searchTerm, content = article)

def get_article(searchTerm):
    api_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "titles": searchTerm,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "format": "json"
    }

    response = requests.get(url = api_url, params = params)

    responseJson = response.json()

    pageid = list(responseJson["query"]["pages"].keys())[0]
    page = responseJson["query"]["pages"][pageid]
    pageText = page["extract"]

    return pageText

def export_pdf(dir, title, content):
    outputPath = os.path.join(dir, "{}.pdf".format(title))

    pdf = SimpleDocTemplate(filename = outputPath, pagesize = A4)

    styles = getSampleStyleSheet()

    pdfTitle = Paragraph(title, styles["Title"])
    pdfParagraph = Paragraph(content, styles["Normal"])

    pdf.build([pdfTitle, pdfParagraph])

    print("{}.pdf saved in {}".format(title, dir))

if __name__ == "__main__":
    main()