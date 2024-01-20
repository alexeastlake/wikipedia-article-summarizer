import requests
import random

API_URL = "https://en.wikipedia.org/w/api.php"

def get_article_text(article_title):
    request_params = {
        "action": "query",
        "titles": article_title,
        "prop": "extracts",
        "exintro" : False,
        "explaintext": True,
        "redirects": True,
        "format": "json"
    }

    response = requests.get(API_URL, request_params)
    response_json = response.json()

    page_text = next(iter((response_json.get("query").get("pages").values()))).get("extract")

    return page_text

def get_article_image(image_title):
    request_params = {
        "action": "query",
        "titles": image_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    response = requests.get(API_URL, request_params)
    response_json = response.json()

    image_url = next(iter((response_json.get("query").get("pages").values()))).get("imageinfo")[0].get("url")

    response = requests.get(url = image_url, headers = {"User-Agent": "Script"}, allow_redirects = True)

    return response.content

def get_article_images(article_title, num_images):   
    request_params = {
        "action": "query",
        "titles": article_title,
        "prop": "images",
        "imlimit": "max",
        "redirects": True,
        "format": "json"
    }

    response = requests.get(API_URL, request_params)
    response_json = response.json()

    page_images = next(iter((response_json.get("query").get("pages").values()))).get("images")
    page_image_titles = [image.get("title") for image in page_images]
    filtered_page_image_titles = [title for title in page_image_titles if ".svg" not in title.lower()]
    chosen_indexes = random.sample(range(len(filtered_page_image_titles)), num_images)
    chosen_page_image_titles = [filtered_page_image_titles[i] for i in chosen_indexes]
    
    images = []

    for image_title in chosen_page_image_titles:
        if len(images) >= num_images: break

        images.append(get_article_image(image_title))

    return images