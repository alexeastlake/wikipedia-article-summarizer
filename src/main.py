import os
import sys
from utils import wikipedia_api_utils
from utils import pdf_utils

def main():
    args = sys.argv

    try:
        if (len(args) != 3):
            raise ValueError("Invalid arguments: Invalid number of arguments")
        elif ((type(args[1]) != str) or (type(int(args[2])) != int)):
            raise ValueError("Invalid arguments: Invalid argument types")
    except Exception as e:
        print(e)
        exit()

    article_title = args[1]

    article_text = wikipedia_api_utils.get_article_text(article_title)

    num_images = int(args[2])
    article_images = wikipedia_api_utils.get_article_images(article_title, num_images)

    output_dir = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")), "output")

    pdf_utils.export_pdf(dir = output_dir, title = article_title, text = article_text, images = article_images)

if __name__ == "__main__":
    main()