import src.search


def user_iteration():
    """Функция для получения списка вакансий на основании ответов пользователя"""

    print('Привет! Предлагаю тебе получить информацию о вакансиях с разных платформ в России')
    print('Доступные сайты: \n1) hh.ru \n2) superjob.ru')
    website = int(input('\nВведите "1" для поиска в hh.ru \n"2" для поиска в superjob.ru \n"3" для поиска везде\n'))
    vacancy = str(input('\nУкажите вакансию, по которой хотите произвести поиск (например - "Python")\n'))
    top_vacancy = int(input('\nУкажите топ N вакансий (например - "10")\n'))
    if website == 1:
        result = src.search.Search_HH(vacancy, top_vacancy)
        return result.search()
    elif website == 2:
        result = src.search.Search_SJ(vacancy, top_vacancy)
        return result.search()
    elif website == 3:
        result = src.search.Search_all(vacancy, top_vacancy)
        return result.search()
    else:
        print("Такого сайта пока нет!")


def programm(data):
    """Функция для вывода готовой информации пользователю"""
    n = 1
    for i in data:
        print(f"{n}). Требуется: {i['name']} с зарплатой от: {i['salary_from']}; ссылка на вакансию: {i['url']}")
        n += 1


programm(user_iteration())
