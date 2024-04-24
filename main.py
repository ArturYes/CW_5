from config import config
from hh_parser import HeadHunterAPI
from working_db import create_database, save_data_to_database, DBManager


def get_work_api(db_name: str, params: dict) -> None:
    """
    Функция создает и наполняет БД данными от API HedHunter
    :return: None
    """
    employer_list = [40912, 88787, 238354, 1008541, 1204987, 1918903, 2071925, 2223982, 5569859, 9473594]

    hh = HeadHunterAPI(employer_list)
    employer_data = hh.get_employers_data()

    create_database(db_name, params)
    save_data_to_database(db_name, params, employer_data)

    print("База данных успешно создана и заполнена данными.")

    user_answer = input("Хотите продолжить работу с БД:\n"
                        "1 - Да\n"
                        "2 - Нет\n").strip()
    if user_answer == "1":
        get_work_db(db_name, params)
    else:
        exit("Спасибо за использование приложения. Всего доброго!")


def get_work_db(db_name: str, params: dict) -> None:
    """
    Функция взаимодействия с пользователем для получения данных из БД PostgreSQL
    :return: None
    """
    while True:
        user_answer = input("\nВыберите действие для работы с БД PostgreSQL:\n"
                            "1 - Получить список всех компаний и количество вакансий\n"
                            "2 - Получить список всех вакансий с подробной информацией\n"
                            "3 - Получить среднюю зарплату всех вакансий\n"
                            "4 - Получить список всех вакансий с зарплатой выше средней\n"
                            "5 - Получить список вакансий по ключевому слову\n"
                            "6 - Выход\n").strip()
        if user_answer in ["1", "2", "3", "4", "5"]:
            db_manager = DBManager(db_name, params)
            if user_answer == "1":
                db_manager.get_companies_and_vacancies_count()
            elif user_answer == "2":
                db_manager.get_all_vacancies()
            elif user_answer == "3":
                db_manager.get_avg_salary()
            elif user_answer == "4":
                db_manager.get_vacancies_with_higher_salary()
            elif user_answer == "5":
                answer = input("Введите ключевое слово для фильтрации: ").strip()
                db_manager.get_vacancies_with_keyword(answer)
        elif user_answer == "6":
            exit("Спасибо за использование приложения. Всего доброго!")


def main():
    """
    Стартовое взаимодействие
    """
    while True:
        answer = input("Добро пожаловать в программу для работы с БД PostgreSQL\n"
                       "Для продолжения выберите действие:\n"
                       "1 - Создать базу данных и наполнить ее данными\n"
                       "2 - Работать с уже существующей БД\n").strip()
        if answer in ["1", "2"]:
            break
    db_name = 'cw_5_headhunter'
    params = config()
    if answer == "1":
        get_work_api(db_name, params)
    elif answer == "2":
        get_work_db(db_name, params)
    else:
        exit("Непредвиденная ошибка. Выход.")


if __name__ == '__main__':
    main()
