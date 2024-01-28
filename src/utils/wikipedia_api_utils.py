import requests
import random

API_URL = "https://en.wikipedia.org/w/api.php"

# Gets the content of a URL
def get_url_content(url):
    try:
        return requests.get(url = url, headers = {"User-Agent": "Script"}, allow_redirects = True).content
    except Exception as e:
        raise e

def search_page_titles(page_title):
    try:
        request_params = {
            "action": "query",
            "list": "search",
            "srsearch": page_title,
            "srlimit": 10,
            "redirects": True,
            "format": "json"
        }

        response_json = (requests.get(API_URL, request_params)).json()

        pages = (response_json.get("query").get("search"))

        titles = []

        if pages:
            for page in pages:
                titles.append(page.get("title"))

        return titles
    except Exception as e:
        raise e

# Gets page intro text from page title
def get_page_text(page_title):
    try:
        request_params = {
            "action": "query",
            "titles": page_title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "exsectionformat": "wiki",
            "redirects": True,
            "format": "json"
        }

        response_json = (requests.get(API_URL, request_params)).json()

        page_text = next(iter((response_json.get("query").get("pages").values()))).get("extract")

        return page_text
    except Exception as e:
        raise e

# Gets an image from wikipedia with the given image title
def get_image(image_title):
    try:
        request_params = {
            "action": "query",
            "titles": image_title,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json"
        }

        response_json = (requests.get(API_URL, request_params)).json()

        image_url = next(iter((response_json.get("query").get("pages").values()))).get("imageinfo")[0].get("url")
        image = get_url_content(image_url)

        return image
    except Exception as e:
        raise e

def get_page_image_titles(page_title):
    try:
        request_params = {
            "action": "query",
            "titles": page_title,
            "prop": "images",
            "imlimit": "max",
            "redirects": True,
            "format": "json"
        }

        response_json = (requests.get(API_URL, request_params)).json()

        page = next(iter((response_json.get("query").get("pages").values())))

        if "images" not in page.keys():
            raise ValueError("No page images found for page {}".format(page_title))

        image_titles = [image.get("title") for image in page.get("images")]

        return image_titles
    except Exception as e:
        raise e

def filter_image_titles_filetype(image_titles, file_types):
    try:
        valid_image_titles = []

        for title in image_titles:
            if any(title.lower().endswith(file_type.lower()) for file_type in file_types):
                valid_image_titles.append(title)
            
        if not valid_image_titles:
            raise ValueError("No page images found in valid formats {}".format(file_types.join(", ")))
    except Exception as e:
        raise e

def get_random_image_titles(image_titles, max_images):
    try:
        chosen_titles = []

        for i in random.sample(range(len(image_titles)), min(len(image_titles), max_images)):
            chosen_titles.append(image_titles[i])
    except Exception as e:
        raise e

# Gets the given max number of random images from the page with the given title
def get_page_images(page_title, file_types, max_images):
    try:
        image_titles = get_page_image_titles(page_title)

        if file_types:
            image_titles = filter_image_titles_filetype(image_titles, file_types)
        
        if max_images:
            image_titles = get_random_image_titles(image_titles, max_images)

        images = []

        for image_title in image_titles:
            images.append(get_image(image_title))
        
        return images
    except Exception as e:
        raise e

# Gets the thumbnail image for a page with the given title
def get_page_thumbnail(page_title):
    try:
        print("Getting page {} thumbnail...".format(page_title))

        request_params = {
            "action": "query",
            "titles": page_title,
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": 200,
            "redirects": True,
            "format": "json"
        }

        response_json = (requests.get(API_URL, request_params)).json()

        page = next(iter((response_json.get("query").get("pages").values())))

        if "thumbnail" not in page.keys():
            raise ValueError("No thumbnail found for page")

        thumbnail = page.get("thumbnail")
        thumbnail_url = thumbnail.get("source")

        thumbnail_image = get_url_content(thumbnail_url)
        print("Retrieved page thumbnail\n")

        return thumbnail_image
    except Exception as e:
        print("Failed to retrieve page thumbnail: {}\n".format(e))

# Gets the URL of a page with the given title
def get_page_url(page_title):
    try:
        print("Getting page {} URL...".format(page_title))

        request_params = {
            "action": "query",
            "titles": page_title,
            "prop": "info",
            "inprop": "url",
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        url = next(iter((response_json.get("query").get("pages").values()))).get("fullurl")
        print("Retrieved page URL\n")

        return url
    except Exception as e:
        print("Failed to retrieve page {} URL".format(page_title))