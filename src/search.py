import src.json_code
import src.api_code


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


class Search_HH:
    """Поиск и сортировка вакансий на сайте hh.ru"""
    def __init__(self, vac, top_vac):
        self.vac = vac
        self.top_vac = top_vac

    def search(self):
        hh = src.api_code.HH_vacancies(self.vac)
        hh_get = hh.get_request().json()
        from_list_hh = src.json_code.JSONSaverHH(hh_get)
        from_list_hh.add_vacancy()
        in_list_hh = from_list_hh.get_vacancy()
        from_list_hh.del_vacancy()
        all_vacancy_hh = Vacancy(in_list_hh)
        all_vacancy_hh.sorted_by_pay()
        return all_vacancy_hh.top_n(self.top_vac)


class Search_SJ(Search_HH):
    """Поиск и сортировка вакансий на сайте superjob.ru"""
    def __init__(self, vac, top_vac):
        super().__init__(vac, top_vac)

    def search(self):
        sj = src.api_code.Superjob_vacancies(self.vac)
        sj_get = sj.get_request().json()
        from_list_sj = src.json_code.JSONSaverSJ(sj_get)
        from_list_sj.add_vacancy()
        in_list_sj = from_list_sj.get_vacancy()
        from_list_sj.del_vacancy()
        all_vacancy_sj = Vacancy(in_list_sj)
        all_vacancy_sj.sorted_by_pay()
        return all_vacancy_sj.top_n(self.top_vac)


class Search_all(Search_SJ):
    """Объединение и сортировка вакансий на двух сайтах"""
    def __init__(self, vac, top_vac):
        super().__init__(vac, top_vac)

    def search(self):
        first = Search_HH(self.vac, self.top_vac)
        second = Search_SJ(self.vac, self.top_vac)
        in_list_all = first.search() + second.search()
        all_vacancy = Vacancy(in_list_all)
        all_vacancy.sorted_by_pay()
        return all_vacancy.top_n(self.top_vac)

