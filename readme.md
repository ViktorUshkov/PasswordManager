## Менеджер паролей

Программа предоставляет класс для работы с менеджером паролей. Пользователю будут доступны следующие способы взаимодействия с менеджером:
* Просмотр списка существующих паролей
* Добавление нового пароля в список

Пароли хранятся в файле в следующем формате: "{сервис} | {логин} | {пароль}". Поле пароля шифруется с помощью симметричного шифрования, реализованного с помощью функции из пакета cryptography.fernet

**Пример записи в файле:** GitHub | User3131 | (зашифрованный пароль)

При инициализации объекта класса пользователь передает мастер-пароль, с помощью которого будут защищаться пароли и путь к файлу, в котором пароли будут храниться