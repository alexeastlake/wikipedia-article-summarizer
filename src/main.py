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
            "short": True,
            "max_images": 3,
            "image_file_types": [".jpeg", ".jpg", ".png"]
        }

        page_content = get_page_contents(page_title, content)

        # Exports page data to PDF
        output_dir = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")), "output")
        pdf_utils.export_pdf(dir = output_dir, title = page_title, content = page_content)
    except Exception as e:
        print("An error occurred: {}\n".format(e))
        exit()

# Loop to search for page titles using user input
def search_page_titles():
    try:
        while True:
            search_term = input("Enter a search term: ")

            page_titles = wikipedia_api_utils.get_page_titles(search_term)
            print("Search results: {}\n".format(", ".join(page_titles)))

            if search_term in page_titles:
                print("Search results contain page with name: {}".format(search_term))
                confirmation = input("Confirm this page? (y/n):  ")

                if confirmation == "y":
                    return page_titles[0]

                print()
            elif page_titles and len(page_titles) > 1:
                continue
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
                    data["text"] = wikipedia_api_utils.get_page_text(page_title, content["short"])
                    print ("Text retrieved")
                case "thumbnail":
                    try:
                        data["thumbnail"] = wikipedia_api_utils.get_page_thumbnail(page_title)
                        print("Thumbnail retrieved")
                    except Exception as e:
                        print(e)
                case "images":
                    if "max_images" in content.keys() and "image_file_types" in content.keys():
                        data["images"] = wikipedia_api_utils.get_page_images(page_title, content["image_file_types"], content["max_images"])
                        print("Images retrieved")
                    else:
                        print("Option images requires: string[] image_file_types, int max_images")
                case "source":
                    data["source"] = wikipedia_api_utils.get_page_url(page_title)
                    print("Source retrieved")

        return data
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()