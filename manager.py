"""
Файл предоставляет класс для работы с менеджером паролей. Данный класс предоставляет возможность просмотреть список
имеющихся паролей, а также добавить в список новые пароли. Пароли хранятся в зашифрованном виде в файле, путь к которому
хранится в поле экземпляра класса.
"""

from cryptography.fernet import Fernet
import os.path


class PasswordManager:
    """ Класс, организующий работу с менеджером паролей """

    # разделитель между элементами одной записи в файле
    SEPARATOR = ' | '
    # путь к файлу с ключом для шифрования
    KEY_FILE_PATH = 'key.key'
    # ключи, которые должны быть в словаре, передаваемого в self.interact для добавления нового пароля
    NEW_PASSW_DICT_KEYS = ['service', 'login', 'password']

    def __init__(self, master_password: str, file: str):
        """
        Инициализация класса менеджера паролей

        :param master_password: Мастер-пароль, по которому доступен файл с паролями.
        :param file: Путь к файлу, в котором хранятся пароли
        """
        self.master_password = master_password
        self.file = file
        self._save_encrypt_key()
        self.fernet = Fernet(self._get_encrypt_key())

    @property
    def master_password(self) -> str:
        """
        getter-свойство для мастер-пароля
        :return: мастер-пароль
        """
        return self._master_password

    @master_password.setter
    def master_password(self, new_master_password: str) -> None:
        """
        setter-свойство для мастер-пароля

        :raise TypeError: ошибка вызывается, если пароль не является строкой
        :param new_master_password: устанавливаемый мастер-пароль
        """
        if not isinstance(new_master_password, str):
            raise TypeError("Мастер-пароль должен быть строкой")
        self._master_password = new_master_password

    @property
    def file(self) -> str:
        """
        :return: возвращает путь к файлу с паролями
        """
        return self._file

    @file.setter
    def file(self, new_file: str) -> None:
        """
        Устанавливает значение поля file (путь к файлу с паролями) в экземпляре класса после валидации

        :raise TypeError: ошибка вызывается, если передан не файл
        :raise ValueError: ошибка вызывается, если переданный файл не формата .txt
        :param new_file: путь к файлу
        """
        if not os.path.isfile(new_file):
            raise TypeError("Передан не файл")

        if os.path.splitext(new_file)[1].lower() != ".txt":
            raise ValueError("Файл должен быть формата .txt")

        self._file = new_file

    def _add_password(self, service: str, login: str, password: str) -> None:
        """
        Функция, добавляющая запись, состоящую из названия интернет-сервиса (service), логина (login) и пароля (password)
        в файл self.file в зашифрованном виде.

        :param service: название интернет-сервиса, от учетной записи которого сохраняем пароль
        :param login: логин от учетной записи
        :param password: сохраняемый пароль
        """
        with open(self.file, 'a') as file:
            file.write(service + self.SEPARATOR + login + self.SEPARATOR + self.fernet.encrypt(password.encode()).decode() + "\n")

    def _view_passwords(self, decrypt: bool) -> None:
        """
        Функция, выводящая на экран список паролей из файла self.file

        :param decrypt: параметр, определяющий, в каком виде выводить пароли - в зашифрованном (False) или дешифрованном (True)
        """
        with open(self.file, 'r') as file:
            for line in file.readlines():
                # составляющие части одной записи в файле - интернет-сервис, логин и пароль
                service, login, password = line.rstrip().split(self.SEPARATOR)
                if decrypt:
                    print(f'{service}: логин - {login}, пароль - {self.fernet.decrypt(password.encode()).decode()}')
                else:
                    print(f'{service}: логин - {login}, пароль - {password}')

    def _save_encrypt_key(self) -> None:
        """
        Функция, генерирующая ключ для шифрования паролей и записывающая его в файл KEY_FILE_PATH
        """
        key: bytes = Fernet.generate_key()
        with open(self.KEY_FILE_PATH, 'wb') as file:
            file.write(key)

    def _get_encrypt_key(self) -> bytes:
        """
        Функция, возвращающая ключ для шифрования паролей из файла KEY_FILE_PATH
        :return: ключ для шифрования
        """
        with open(self.KEY_FILE_PATH, 'rb') as file:
            key: bytes = file.read()
        return key

    def _check_master_password(self, input_master_password: str) -> bool:
        """
        Проверяет, совпадает ли введенный мастер-пароль с уже имеющимся
        :param input_master_password: введенный мастер-пароль
        :return: True, если пароли совпадают, False в ином случае
        """
        return input_master_password == self.master_password

    def _dict_validation(self, dict_to_check: dict[str]) -> bool:
        """
        Функция для валидации словаря, передаваемого в функцию interact
        :param dict_to_check: словарь для валидации

        :raise TypeError: ошибка вызывается, если передан не словарь, или его значения не являются строками
        :raise ValueError: ошибка вызывается, если в словаре нет какого-либо из ключей "service", "login", "password"

        :return: True, если словарь прошел валидацию, в ином случае будет вызвана ошибка
        """
        if not isinstance(dict_to_check, dict):
            raise TypeError("Переданный объект не является словарём")

        if not all(key in dict_to_check.keys() for key in self.NEW_PASSW_DICT_KEYS):
            raise ValueError("Отсутствует один из ключей: 'service', 'login' или 'password'")

        if not isinstance(dict_to_check['service'], str):
            raise TypeError("Название сервиса должно быть строкой")

        if not isinstance(dict_to_check['login'], str):
            raise TypeError("Логин должен быть строкой")

        if not isinstance(dict_to_check['password'], str):
            raise TypeError("Пароль должен быть строкой")

        return True

    def interact(self, input_master_password: str, new_password: dict[str] = None) -> None:
        """
        Функция для взаимодействия с экземпляром класса - при вызове без аргументов вызывается функция view_passwords(),
        при вызове с аргументом

        :param input_master_password: мастер-пароль, по которому доступен список с паролями. Если он не совпадает с
                                      текущим мастер-паролем, то пароли шифруются
        :param new_password: словарь с аргументами для записи нового пароля, должен содержать ключи service, login и password
        """
        if not new_password:
            if self._check_master_password(input_master_password):
                self._view_passwords(True)
            else:
                self._view_passwords(False)
        elif self._dict_validation(new_password):
            self._add_password(new_password["service"], new_password["login"], new_password["password"])
