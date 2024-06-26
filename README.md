## Получение данных от API HeadHunter и работа с бд PostgreSQL

### Технологии:

```text
psycopg2 ^2.9.9
requests ^2.31.0
```

### Инструкция для запуска проекта:

```text
1. Клонировать проект
2. Создать и активировать виртуального окружения и установите зависимости
3. Отредактировать файл database.ini.sample
4. Запустить проект
```

#### 1. Клонирование проекта:

Клонируйте репозиторий используя следующую команду

```sh
git clone https://github.com/ArturYes/CW_5.git
```

#### 2. Настройка виртуального окружение и установка зависимостей:

- [Инструкция по установке](https://sky.pro/media/kak-sozdat-virtualnoe-okruzhenie-python/)

#### 3. Настройка database.ini

Переименуйте файл **database.ini.sample** в **database.ini** и настройте параметры

```ini
[postgresql]
host = адрес вашего хоста
user = имя пользователя БД
password = пароль БД
port = порт БД
```

#### 4. Запуск проекта:

```text
Для запуска проекта запустите файл main.py и следуйте инструкциям интерфейса
```

### Описание работы программы:

При старте программы пользователю предлагается выбор получить вакансии от API HeadHunter или работать с данными БД.

При выборе работы с API программа проходится по списку работодателей получает о них данные и их вакансиях,
затем сохраняет данные в БД PostgreSQL и предлагает работать с ними или выйти.

При выборе работы с данными БД программа предлагает сделать выбор по каким критериям вывести данные из БД,
доступные варианты:

```text
1. Получить список всех компаний и количество вакансий
2. Получить список всех вакансий с подробной информацией
3. Получить среднюю зарплату всех вакансий
4. Получить список всех вакансий с зарплатой выше средней
5. Получить список вакансий по ключевому слову
```

Программа выводит данные в соответствие с выбором.
Для выхода из программы выберите соответствующий пункт.