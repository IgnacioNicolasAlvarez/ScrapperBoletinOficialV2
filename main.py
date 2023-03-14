import requests
from bs4 import BeautifulSoup
from config import settings
import pymongo

url = "https://boletin.tucuman.gov.ar/boletin/view"

payload = {
    "fechaBoletin": "2023-03-13",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
response = requests.post(url, data=payload, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

avisos = soup.find_all("article", {"class": "blog-post"})[1]


try:
    titulo_numero_aviso = avisos.find_all(
        "h3", {"class": "pt-5 pb-4 mb-4 fst-italic border-bottom"}
    )

    titulo_numero_aviso = [
        n.find("a", {"name": True})["name"] for n in titulo_numero_aviso
    ]

    titulo = [
        a.text.strip() for a in avisos.find_all("h2", {"class": "blog-post-title"})
    ]
    contenido = [
        a.text.strip() for a in avisos.find_all("p", {"class": "font-monospace"})
    ]

    grouped_avisos = list(zip(titulo_numero_aviso, titulo, contenido))

    client = pymongo.MongoClient(
        f"mongodb+srv://{settings.user}:{settings.password}@cluster0.gpqkpko.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client.avisos
    collection = db["avisos"]

    for element in grouped_avisos:
        item = {"name": element[0], "title": element[1], "content": element[2]}
        collection.insert_one(item)

except Exception as e:
    print(e)
    pass
