"""
Файл предоставляет класс для работы с менеджером паролей. Данный класс предоставляет возможность просмотреть список
имеющихся паролей, а также добавить в список новые пароли. Пароли хранятся в файле, путь к которому хранится в поле
экземпляра класса
"""


class PasswordManager:
    """ Класс, организующий работу с менеджером паролей """

    # разделитель между элементами одной записи в файле
    SEPARATOR = ' | '

    def __init__(self, master_password: str, file: str):
        """
        Инициализация класса менеджера паролей

        :param master_password: Мастер-пароль, по которому доступен файл с паролями.
        :param file: Путь к файлу, в котором хранятся пароли
        """
        self.master_password = master_password
        self.file = file

    def add_passwords(self) -> None:
        pass

    def view_passwords(self) -> None:
        pass

    def check_master_password(self) -> bool:
        pass

    def interact(self) -> None:
        pass

