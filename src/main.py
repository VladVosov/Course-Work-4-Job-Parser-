from abc import ABC, abstractmethod
import requests
import json


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
                if salary_from == None:
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


class Vacancy:
    """Kласс для работы с вакансиями"""

    def __init__(self, list_dict):
        self.list_dict = list_dict

    def sorted_by_pay(self):
        """Сортируем полученный список словарей с вакансиями по зарплате"""
        self.list_dict = sorted(self.list_dict, key=lambda x: x['salary_from'], reverse=True)
        return self.list_dict

    def top_n(self, top_n=int):
        """Оставляем в отсортированном списке необходимое количество вакансий"""
        del self.list_dict[top_n:]
        return self.list_dict


def search_in_hh(vac, top_vac):
    """Поиск и сортировка вакансий на сайте hh.ru"""
    hh = HH_vacancies(vac)
    hh_get = hh.get_request().json()
    from_list_hh = JSONSaverHH(hh_get)
    from_list_hh.add_vacancy()
    in_list_hh = from_list_hh.get_vacancy()
    from_list_hh.del_vacancy()
    all_vacancy_hh = Vacancy(in_list_hh)
    all_vacancy_hh.sorted_by_pay()
    return all_vacancy_hh.top_n(top_vac)


def search_in_sj(vac, top_vac):
    """Поиск и сортировка вакансий на сайте superjob.ru"""
    sj = Superjob_vacancies(vac)
    sj_get = sj.get_request().json()
    from_list_sj = JSONSaverSJ(sj_get)
    from_list_sj.add_vacancy()
    in_list_sj = from_list_sj.get_vacancy()
    from_list_sj.del_vacancy()
    all_vacancy_sj = Vacancy(in_list_sj)
    all_vacancy_sj.sorted_by_pay()
    return all_vacancy_sj.top_n(top_vac)


def search_in_all(first, second, top_vac):
    # Объединение и сортировка вакансий на двух сайтах
    in_list_all = first + second
    all_vacancy = Vacancy(in_list_all)
    all_vacancy.sorted_by_pay()
    return all_vacancy.top_n(top_vac)


def user_iteration():
    """Функция для получения списка вакансий на основании ответов пользователя"""

    print('Привет! Предлагаю тебе получить информацию о вакансиях с разных платформ в России')
    print('Доступные сайты: \n1) hh.ru \n2) superjob.ru')
    website = int(input('\nВведите "1" для поиска в hh.ru \n"2" для поиска в superjob.ru \n"3" для поиска везде\n'))
    vacancy = str(input('\nУкажите вакансию, по которой хотите произвести поиск (например - "Python")\n'))
    top_vacancy = int(input('\nУкажите топ N вакансий (например - "10")\n'))
    if website == 1:
        return search_in_hh(vacancy, top_vacancy)
    elif website == 2:
        return search_in_sj(vacancy, top_vacancy)
    elif website == 3:
        first = search_in_hh(vacancy, top_vacancy)
        second = search_in_sj(vacancy, top_vacancy)
        return search_in_all(first, second, top_vacancy)
    else:
        print("Такого сайта пока нет!")


def programm(data):
    """Функция для вывода готовой информации пользователю"""
    n = 1
    for i in data:
        print(f"{n}). Требуется: {i['name']} с зарплатой от: {i['salary_from']}; ссылка на вакансию: {i['url']}")
        n += 1


programm(user_iteration())
