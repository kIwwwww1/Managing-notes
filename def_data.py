import psycopg2
from pydantic import BaseModel, Field, ValidationError
from user_data import DataBase


class BaseAddData(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=1000)


db = psycopg2.connect(
    dbname=DataBase.dbname,
    host=DataBase.host,
    user=DataBase.user,
    password=DataBase.password,
)


def create_table():
    with db as data:
        with data.cursor() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS user_note (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        description TEXT
                        )""")
            data.commit()


def create_data():
    while True:
        add_title = input("Введите название заметки: ")
        add_description = input("Введите описание заметки: ")
        try:
            all_data = BaseAddData(title=add_title, description=add_description)
            while True:
                confirm = input("Создать = 1 | Удалить = 0: ")
                match confirm:
                    case "1":
                        with db as data:
                            with data.cursor() as c:
                                c.execute(
                                    """INSERT INTO user_note (title, description) VALUES (%s, %s)""",
                                    (all_data.title, all_data.description),
                                )
                                db.commit()
                                print("Запись создана")
                        break
                    case "0":
                        print("Запись удалена")
                        break
                    case _:
                        print("Неверный ввод")
            break
        except ValidationError:
            print("Возможно допустили ошибку в название")


def read_data():
    with db as data:
        with data.cursor() as c:
            c.execute("""SELECT * FROM user_note""")
            notes = c.fetchall()
            for note in notes:
                print(f"id {note[0]} | {note[1]} -> {note[2]}")


def update_data():
    with db as data:
        with data.cursor() as c:
            while True:
                try:
                    note_id = int(input("Введите ID записи: "))
                    c.execute("""SELECT * FROM user_note WHERE id = (%s)""", (note_id,))
                    note = c.fetchone()
                    if note is not None:
                        print(f"""{note[1]} \n{note[2]}""")
                        update = int(input("Изменить название 1 | описание 2: "))
                        match update:
                            case 1:
                                new_title = input("Новое название: ")
                                c.execute(
                                    """UPDATE user_note SET title = (%s) WHERE id = (%s)""",
                                    (new_title, note_id),
                                )
                                db.commit()
                                print("Обновлено")
                                break
                            case 2:
                                new_description = input("Новое название: ")
                                c.execute(
                                    """UPDATE user_note SET description = (%s) WHERE id = (%s)""",
                                    (new_description, note_id),
                                )
                                db.commit()
                                print("Обновлено")
                                break
                            case _:
                                print("Неверный ввод")
                    else:
                        print("Данный ID не найден")
                        break
                except ValueError:
                    print("Неверный ввод")


def delete_data():
    with db as data:
        with data.cursor() as c:
            while True:
                note_id = int(input("Введите ID записи: "))
                c.execute("""SELECT * FROM user_note WHERE id = (%s)""", (note_id,))
                note = c.fetchone()
                if note is not None:
                    print(f"""{note[1]} \n{note[2]}""")
                    update = int(input("Отменить 0 | Удалить запись 1: "))
                    match update:
                        case 1:
                            c.execute(
                                """DELETE FROM user_note WHERE id = (%s)""", (note_id,)
                            )
                            db.commit()
                            print("Запись удалена")
                            break
                        case 0:
                            break
                        case _:
                            print("Неверный ввод")
                else:
                    print("Данный ID не найден")
                    break
