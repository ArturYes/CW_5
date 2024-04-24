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
