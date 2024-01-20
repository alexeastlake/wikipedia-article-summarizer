import requests
import random

API_URL = "https://en.wikipedia.org/w/api.php"

def get_article_titles(article_title):
    try:
        if not article_title:
            raise

        print("Getting articles for {}...".format(article_title))

        request_params = {
            "action": "query",
            "list": "search",
            "srsearch": article_title,
            "srlimit": 10,
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        pages = (response_json.get("query").get("search"))

        if len(pages) <= 0:
            raise

        titles = [page.get("title") for page in pages]

        print("Retrieved articles {}".format(", ".join(titles)))

        return titles
    except Exception as e:
        print("Failed to retrieve articles: {}".format(e))

        return []

def search_article_titles():
    try:
        while True:
            search_title = input("Enter a title, or press Enter to exit: ")

            if not search_title:
                exit()

            article_titles = get_article_titles(search_title)
            
            if len(article_titles) == 1:
                return article_titles[0]
            elif len(article_titles) <= 0:             
                continue
            elif len(article_titles) > 1:
                for title in article_titles:
                    if search_title == title:
                         if input("A retrieved article has title: {}. Confirm this article(y/n)? ".format(article_titles[0])) == "y":
                            return article_titles[0]
               
                print("More than 1 article found, narrow your title search")
                continue
    except Exception as e:
        print("Failed to search articles: {}".format(e))

def get_article_text(article_title):
    try:
        print("Getting article text...")

        request_params = {
            "action": "query",
            "titles": article_title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        page_text = next(iter((response_json.get("query").get("pages").values()))).get("extract")
        print("Retrieved article text")

        return page_text
    except Exception as e:
        print("Failed to retrieve article text: {}".format(e))

def get_url_content(url):
    try:
        return requests.get(url = url, headers = {"User-Agent": "Script"}, allow_redirects = True).content
    except Exception as e:
        raise e

def get_article_image(image_title):
    try:
        print("Getting article image {}...".format(image_title))
    
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
        image = get_url_content(image_url)
        print("Retrieved article image")

        return image
    except Exception as e:
        print("Failed to retrieve article image: {}".format(e))

def get_article_images(article_title, num_images):
    try:
        print("Getting {} article {} images...".format(num_images, article_title))

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
        chosen_indexes = random.sample(range(0, len(filtered_page_image_titles)), num_images)
        chosen_page_image_titles = [filtered_page_image_titles[i] for i in chosen_indexes]
        
        images = []

        for image_title in chosen_page_image_titles:
            if len(images) >= num_images: break

            images.append(get_article_image(image_title))

        
        return images
    except Exception as e:
        print("Failed to retrieve article images: {}".format(e))

def get_article_thumbnail(article_title):
    try:
        print("Getting article {} thumbnail...".format(article_title))

        request_params = {
            "action": "query",
            "titles": article_title,
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": 200,
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        thumbnail = next(iter((response_json.get("query").get("pages").values()))).get("thumbnail")
        thumbnail_url = thumbnail.get("source")

        thumbnail_image = get_url_content(thumbnail_url)
        print("Retrieved article thumbnail")

        return thumbnail_image
    except Exception as e:
        print("Failed to retrieve article thumbnail: {}".format(e))