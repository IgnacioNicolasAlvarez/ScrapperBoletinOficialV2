import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import settings
from src.db.repository import MongoRepository
from src.model.model import Aviso

repository = MongoRepository(
    user=settings.db.mongo.private.credentials.user,
    password=settings.db.mongo.private.credentials.password,
    server=settings.db.mongo.private.credentials.server,
    db=settings.db.mongo.public.db,
    collection=settings.db.mongo.public.collection,
)


class Scrapper:
    def __init__(self, scrap_date, url):
        self.url = url
        self.payload = {
            "fechaBoletin0": scrap_date,
        }
        self.headers = {"User-Agent": UserAgent().random}

    def _get_response(self):
        return requests.post(self.url, data=self.payload, headers=self.headers)

    def _parse_response(self, response_content):
        return BeautifulSoup(response_content, "html.parser")

    def _extract_avisos(self, soup):
        return soup.find_all("article", {"class": "blog-post"})[1]

    def _extract_titulo_numero_aviso(self, avisos):
        h3_elements = avisos.find_all(
            "h3", {"class": "pt-5 pb-4 mb-4 fst-italic border-bottom"}
        )
        return [n.find("a", {"name": True})["name"] for n in h3_elements]

    def _extract_titulo(self, avisos):
        h2_elements = avisos.find_all("h2", {"class": "blog-post-title"})
        return [a.text.strip() for a in h2_elements]

    def _extract_contenido(self, avisos):
        p_elements = avisos.find_all("p", {"class": "font-monospace"})
        return [a.text.strip() for a in p_elements]

    def get_grouped_avisos(self):
        response = self._get_response()
        soup = self._parse_response(response.content)
        avisos = self._extract_avisos(soup)

        titulo_numero_aviso = self._extract_titulo_numero_aviso(avisos)
        titulo = self._extract_titulo(avisos)
        contenido = self._extract_contenido(avisos)

        grouped_avisos = [
            Aviso(numero=a[0], titulo=a[1], body=a[2])
            for a in zip(titulo_numero_aviso, titulo, contenido)
        ]

        return grouped_avisos

    def save_aviso(self, aviso: Aviso):
        repository.insert_one(aviso)
