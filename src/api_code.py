from abc import ABC, abstractmethod
import requests


class API(ABC):
    """Абстрактный класс API"""

    @abstractmethod
    def get_request(self):
        pass


class HH_vacancies(API):
    """Класс для работы с API сайта с вакансиями HH.ru"""

    def __init__(self, keyword, page=0):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {"text": keyword, "page": page}

    def get_request(self):
        """На основе ссылки, страницы сайта и пользовательского запроса получаем данные сайта hh.ru"""
        return requests.get(self.url, params=self.params)


class Superjob_vacancies(API):
    """Класс для работы с API сайта с вакансиями superjob.ru"""

    def __init__(self, keyword, page=1):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.params = {"keywords": keyword, "page": page}

    def get_request(self):
        """На основе ссылки, страницы сайта и пользовательского запроса получаем данные сайта superjob.ru"""
        headers = {
            "X-Api-App-Id": "v3.r.137660814.6b36405656f1054f5ce5e4e9bdd8221500c321e0.06d31b59d2723babb9a9671c1ba8d67f400cd39b"}
        return requests.get(self.url, headers=headers, params=self.params)
