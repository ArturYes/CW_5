import random
import time
import requests


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, employer_list: list[int]):
        """
        Инициализация
        :param employer_list: список работодателей
        """
        self.employer_list = employer_list
        self.employers_vacancies = []

    def get_employers_data(self) -> list[dict[list[dict]]]:
        """
        Получение информации о работодателях и вакансиях
        :return: Список словарей работодателей, работодатель имеет список словарей вакансий
        """
        url = 'https://api.hh.ru/employers/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        for employer in self.employer_list:
            response = requests.get(url=url + str(employer), headers=headers)
            if response:
                data = response.json()
                name = data['name']
                description = data['description']
                site_url = data['site_url']
                area = data['area']['name']
                open_vacancies = data['open_vacancies']

                print(f"\nПолучаем вакансии работодателя: {name}")

                employer_vacancy = self.get_vacancies_employer(employer)

                data_employer = {
                    "id": employer,
                    "name": name,
                    "open_vacancies": open_vacancies,
                    "area": area,
                    "site_url": site_url,
                    "description": description,
                    "vacancies": employer_vacancy
                }
                self.employers_vacancies.append(data_employer)
        return self.employers_vacancies

    @staticmethod
    def get_vacancies_employer(id_employer: int) -> list[dict]:
        """
        Статический метод получения вакансий работодателя
        :param id_employer: id работодателя
        :return: список словарей вакансий
        """
        url = 'https://api.hh.ru/vacancies/'
        params = {
            "employer_id": id_employer,
            "only_with_salary": True,
            "per_page": 100,
            "page": 0
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        employer_vacancy = []
        while True:
            response = requests.get(url=url, params=params, headers=headers)
            if response:
                resp = response.json()
                items = resp['items']
                page = resp['page']
                pages = resp['pages']
                for vacancy in items:
                    id_vacancy = int(vacancy['id'])
                    name = vacancy['name']
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']
                    currency = vacancy['salary']['currency'].upper()
                    experience = vacancy.get('experience').get('name')
                    area = vacancy.get('area').get('name')
                    alternate_url = vacancy.get('alternate_url')

                    vacancy_dict = {"id": id_vacancy,
                                    "name": name,
                                    "salary_from": salary_from,
                                    "salary_to": salary_to,
                                    "currency": currency,
                                    "experience": experience,
                                    "area": area,
                                    "url_vacancy": alternate_url}

                    employer_vacancy.append(vacancy_dict)

                print(f'Загружены вакансии. Страница {page + 1} из {pages}')

                if page == pages - 1:
                    break
                params['page'] = params.get('page') + 1
                random_time = random.uniform(0.3, 0.4)
                time.sleep(random_time)

        print(f"Получено вакансий: {len(employer_vacancy)}")

        return employer_vacancy
