from abc import ABC, abstractmethod
import json


class ABCjson(ABC):
    """Абстрактный класс для добавления информации сайта в json-файл, его сортировки и удаления"""
    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def get_vacancy(self):
        pass

    @abstractmethod
    def del_vacancy(self):
        pass


class JSONSaverHH(ABCjson):
    """Класс для добавления информации сайта HH.ru в json-файл, его сортировки и удаления"""

    def __init__(self, data):
        self.data = data
        self.filename = 'work.json'

    def add_vacancy(self):
        """Сохраняем информацию в json-файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, sort_keys=True, indent=4)

    def get_vacancy(self):
        """Сортируем информацию и достаем то, что нам нужно в список словарей"""
        list_dict = []
        with open(self.filename, 'r', encoding='utf-8') as file:
            full_dict = json.load(file)['items']
            for i in full_dict:
                dictionary = {}
                name = i['name']
                url = i['url']
                if i['salary'] is None:
                    continue
                if i['salary']['currency'] != 'RUR':
                    continue
                salary_from = i['salary']['from']
                if salary_from is None:
                    salary_from = 0
                salary_to = i['salary']['to']
                requirement = i['snippet']['requirement']
                dictionary.update({'name': name, 'url': url, 'salary_from': salary_from, 'salary_to': salary_to,
                                   'requirement': requirement})
                list_dict.append(dictionary)

            return list_dict

    def del_vacancy(self):
        """Чистим следы"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            pass


class JSONSaverSJ(ABCjson):
    """Класс для добавления информации сайта Superjob.ru в json-файл, его сортировки и удаления"""

    def __init__(self, data):
        self.data = data
        self.filename = 'work.json'

    def add_vacancy(self):
        """Сохраняем информацию в json-файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, sort_keys=True, indent=4)

    def get_vacancy(self):
        """Сортируем информацию и достаем то, что нам нужно в список словарей"""
        list_dict = []
        with open(self.filename, 'r', encoding='utf-8') as file:
            full_dict = json.load(file)['objects']
            for i in full_dict:
                dictionary = {}
                name = i['profession']
                url = i['link']
                if i['payment_from'] == 0:
                    continue
                salary_from = i['payment_from']
                salary_to = i['payment_to']
                requirement = i['candidat']
                dictionary.update({'name': name, 'url': url, 'salary_from': salary_from, 'salary_to': salary_to,
                                   'requirement': requirement})
                list_dict.append(dictionary)

            return list_dict

    def del_vacancy(self):
        """Чистим следы"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            pass