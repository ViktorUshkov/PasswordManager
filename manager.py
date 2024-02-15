"""
Файл предоставляет класс для работы с менеджером паролей. Данный класс предоставляет возможность просмотреть список
имеющихся паролей, а также добавить в список новые пароли. Пароли хранятся в файле, путь к которому хранится в поле
экземпляра класса
"""

import cryptography


class PasswordManager:
    """ Класс, организующий работу с менеджером паролей """

    # разделитель между элементами одной записи в файле
    SEPARATOR = ' | '
    KEY_FILE_PATH = 'key.key'

    def __init__(self, master_password: str, file: str):
        """
        Инициализация класса менеджера паролей

        :param master_password: Мастер-пароль, по которому доступен файл с паролями.
        :param file: Путь к файлу, в котором хранятся пароли
        """
        self.master_password = master_password
        self.file = file

    def add_passwords(self, service: str, login: str, password: str) -> None:
        """
        Функция, добавляющая запись, состоящую из названия интернет-сервиса (service), логина (login) и пароля (password)
        в файл self.file

        :param service: название интернет-сервиса, от учетной записи которого сохраняем пароль
        :param login: логин от учетной записи
        :param password: сохраняемый пароль
        """
        with open(self.file, 'a') as file:
            file.write(service + self.SEPARATOR + login + self.SEPARATOR + password)

    def view_passwords(self) -> None:
        """
        Функция, выводящая на экран список паролей из файла self.file
        """
        with open(self.file, 'r') as file:
            for line in file.readlines():
                # составляющие части одной записи в файле - интернет-сервис, логин и пароль
                service, login, password = line.rstrip().split(self.SEPARATOR)
                print(f'{service}: логин - {login}, пароль - {password}')

    def save_encrypt_key(self) -> None:
        pass

    def get_encrypt_key(self) -> str:
        pass

    def check_master_password(self) -> bool:
        pass

    def interact(self) -> None:
        pass
