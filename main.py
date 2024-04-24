from config import config
from hh_parser import HeadHunterAPI
from working_db import create_database


def main():
    employer_list = [40912, 88787, 238354, 1008541, 1204987, 1918903, 2071925, 2223982, 5569859, 9473594]

    hh = HeadHunterAPI(employer_list)
    employer_data = hh.get_employers_data()

    db_name = 'cw_5_headhunter'
    params = config()
    create_database(db_name, params)


if __name__ == '__main__':
    main()
