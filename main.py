from def_data import create_table, create_data, read_data, update_data, delete_data
from time import sleep


def main():
    def main_menu():
        create_table()

        while True:
            try:
                navigator = int(
                    input(
                        """  ________________\n1| Создание записи\n2| Прочитать записи\n3| Обновить запись\n4| Удалить запись\n0| Завершить программу\nВыберите пункт: """
                    )
                )
                match navigator:
                    case 0:
                        break
                    case 1:
                        print("===Создание Записи===")
                        create_data()
                        sleep(2)
                    case 2:
                        print("===Чтение Записи===")
                        read_data()
                        sleep(2)
                    case 3:
                        print("===Обновление Записи===")
                        update_data()
                        sleep(2)
                    case 4:
                        print("===Удаление Записи===")
                        delete_data()
                        sleep(2)
                    case _:
                        print("Ошибка ввода")
            except ValueError:
                print("Завершение программы, неверный ввод")

    main_menu()


if __name__ == "__main__":
    main()
