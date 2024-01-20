import os
from utils import wikipedia_api_utils
from utils import pdf_utils

def main():
    try:
        article_title = wikipedia_api_utils.search_article_titles()

        article_text = wikipedia_api_utils.get_article_text(article_title)

        article_thumbnail = wikipedia_api_utils.get_article_thumbnail(article_title)
        article_images = wikipedia_api_utils.get_article_images(article_title, 3)

        output_dir = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")), "output")

        pdf_utils.export_pdf(dir = output_dir, title = article_title, text = article_text, thumbnail = article_thumbnail, images = article_images)
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    main()