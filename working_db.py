import psycopg2


def create_database(db_name: str, params: dict) -> None:
    """
    Функция создания БД
    :param db_name: название БД
    :param params: параметры для подключения к БД
    :return: None
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                city VARCHAR(50),
                site_url TEXT,
                description TEXT    
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(3),
                experience VARCHAR(50),
                area VARCHAR(50),
                vacancy_url TEXT 
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(db_name: str, params: dict, data: list) -> None:
    """
    Функция сохранения данных в БД
    :param db_name: название БД
    :param params: параметры для подключения к БД
    :param data: данные для сохранения
    :return: None
    """
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        for employer in data:
            cur.execute("""
                INSERT INTO employers (employer_id, company_name, city, site_url, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
                        (employer['id'], employer['name'], employer['area'], employer['site_url'],
                         employer['description'])
                        )
            for vacancy in employer['vacancies']:
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary_from, salary_to, currency, 
                    experience, area, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (vacancy['id'], employer['id'], vacancy['name'], vacancy['salary_from'], vacancy['salary_to'],
                          vacancy['currency'], vacancy['experience'], vacancy['area'], vacancy['url_vacancy'])
                            )
    conn.commit()
    conn.close()


class DBManager:
    """Класс для работы с БД PostgreSQL"""

    def __init__(self, bd_name: str, params: dict) -> None:
        self.bd_name = bd_name
        self.params = params

    def bd_connect(self, query: str = None):
        """Метод подключения к БД"""
        try:
            conn = psycopg2.connect(dbname=self.bd_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                for num, i in enumerate(result, 1):
                    print(f"{num}: {i}")
            conn.close()
        except Exception:
            print(f"Ошибка подключения к базе данных. Проверьте корректность данных.")

    def get_companies_and_vacancies_count(self):
        """Метод получения списка всех компаний и количества вакансий у каждой компании"""
        sql_query = ("""SELECT employers.company_name, COUNT(*) as count_vacancy
                           FROM vacancies
                           JOIN employers USING(employer_id)
                           GROUP BY employers.company_name
                           ORDER BY count_vacancy DESC""")
        self.bd_connect(sql_query)

    def get_all_vacancies(self):
        """Метод получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        sql_query = ("""SELECT employers.company_name, vacancy_name, salary_from, salary_to, currency, vacancy_url 
                           FROM vacancies
                           JOIN employers USING(employer_id)""")
        self.bd_connect(sql_query)

    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям."""
        sql_query = ("""SELECT AVG(COALESCE((salary_from + salary_to) / 2, salary_from, salary_to)) AS avg_salary 
                           FROM vacancies""")
        self.bd_connect(sql_query)

    def get_vacancies_with_higher_salary(self):
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql_query = ("""SELECT * FROM vacancies
                           WHERE COALESCE((salary_from + salary_to) / 2, 
                                           salary_from, 
                                           salary_to) > 
                                           (SELECT AVG(COALESCE((salary_from + salary_to) / 2, 
                                                                 salary_from, 
                                                                 salary_to)) 
                                           FROM vacancies)
                           ORDER BY  COALESCE((salary_from + salary_to) / 2, salary_from, salary_to) DESC""")
        self.bd_connect(sql_query)

    def get_vacancies_with_keyword(self, keyword: str) -> None:
        """Метод получения списка всех вакансий,
        в названии которых содержатся переданные в метод слова, например python."""
        keyword = keyword.lower()
        sql_query = (f"""SELECT * FROM vacancies
                           WHERE LOWER(vacancy_name) LIKE '%{keyword}' OR LOWER(vacancy_name) LIKE '{keyword}%'
                           OR LOWER(vacancy_name) LIKE '%{keyword}%'
                           """)
        self.bd_connect(sql_query)
