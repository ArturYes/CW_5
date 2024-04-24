from hh_parser import HeadHunterAPI


def main():
    employer_list = [40912, 88787, 238354, 1008541, 1204987, 1918903, 2071925, 2223982, 5569859, 9473594]
    hh = HeadHunterAPI(employer_list)
    employer_data = hh.get_employers_data()


if __name__ == '__main__':
    main()
