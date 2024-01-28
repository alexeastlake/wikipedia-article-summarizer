import os
from utils import wikipedia_api_utils
from utils import pdf_utils

def main():
    try:
        # Searches for a wikipedia page using user input
        page_title = search_page_titles()

        # Retrieves various page data
        content = {
            "get": ["text", "thumbnail", "images", "source"],
            "max_images": 3,
            "image_file_types": [".jpeg", ".jpg", ".png"]
        }

        page_content = get_page_contents(page_title, content)

        # Exports page data to PDF
        output_dir = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")), "output")
        pdf_utils.export_pdf(dir = output_dir, title = page_title, content = page_content)
    except Exception as e:
        print("An error occurred: \n{}".format(e))
        exit()

# Loop to search for page titles using user input
def search_page_titles():
    try:
        while True:
            search_term = input("Enter a search term:")

            page_titles = wikipedia_api_utils.get_page_titles(search_term)
            
            if page_titles and len(page_titles) == 1:
                return page_titles[0]
            elif page_titles and len(page_titles > 1):
                print("Search results: {}".format(page_titles.join(", ")))
            else:
                print("No results found")
    except Exception as e:
        raise e

def get_page_contents(page_title, content):
    try:
        data = {}

        for element in content["get"]:
            match element:
                case "text":
                    data["text"] = wikipedia_api_utils.get_page_text(page_title)
                case "thumbnail":
                    data["thumbnail"] = wikipedia_api_utils.get_page_thumbnail(page_title)
                case "images":
                    if data.keys().contains("max_images"):
                        data["images"] = wikipedia_api_utils.get_page_images(page_title, content["max_images"])
                        data["images"] = wikipedia_api_utils.get_page_images(page_title, content["file_types"], content["max_images"])
                case "source":
                    data["source"] = wikipedia_api_utils.get_page_url(page_title)   

        return data
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()