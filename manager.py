"""
Файл предоставляет класс для работы с менеджером паролей. Данный класс предоставляет возможность просмотреть список
имеющихся паролей, а также добавить в список новые пароли. Пароли хранятся в файле, путь к которому хранится в поле
экземпляра класса
"""

from cryptography.fernet import Fernet


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

    def add_password(self, service: str, login: str, password: str) -> None:
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
        """
        Функция, генерирующая ключ для шифрования паролей и записывающая его в файл KEY_FILE_PATH
        """
        key: bytes = Fernet.generate_key()
        with open(self.KEY_FILE_PATH, 'wb') as file:
            file.write(key)

    def get_encrypt_key(self) -> bytes:
        """
        Функция, возвращающая ключ для шифрования паролей из файла KEY_FILE_PATH
        :return: ключ для шифрования
        """
        with open(self.KEY_FILE_PATH, 'rb') as file:
            key: bytes = file.read()
        return key

    def check_master_password(self) -> bool:
        pass

    def dict_validation(self, dict_to_check: dict[str]) -> bool:
        """
        Функция для валидации словаря, передаваемого в функцию interact
        :param dict_to_check: словарь для валидации

        :raise TypeError: ошибка вызывается, если передан не словарь, или его значения не являются строками
        :raise ValueError: ошибка вызывается, если в словаре нет какого-либо из ключей "service", "login", "password"

        :return: True, если словарь прошел валидацию, в ином случае будет вызвана ошибка
        """
        pass

    def interact(self, new_password: dict[str] = None) -> None:
        """
        Функция для взаимодействия с экземпляром класса - при вызове без аргументов вызывается функция view_passwords(),
        при вызове с аргументом

        :param new_password: словарь с аргументами для записи нового пароля, должен содержать ключи service, login и password
        """
        if not new_password:
            self.view_passwords()
        elif self.dict_validation(new_password):
            self.add_password(new_password["service"], new_password["login"], new_password["password"])

    def encrypt(self) -> None:
        pass
