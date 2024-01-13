import sys
import requests
from fpdf import FPDF

def main():
    args = sys.argv

    try:
        if ((len(args) != 2) or (type(args[1]) != str)):
            raise ValueError("Invalid arguments: Must pass 1 string article name")
    except Exception as e:
        print(e)
        exit()
    
    article = getArticle(args[1])

def getArticle(searchTerm):
    api_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "titles": searchTerm,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "format": "json"
    }

    response = requests.get(api_url, params)

    responseJson = response.json()

    pageid = list(responseJson["query"]["pages"].keys())[0]
    page = responseJson["query"]["pages"][pageid]
    pageText = page["extract"]

    return pageText

if __name__ == "__main__":
    main()