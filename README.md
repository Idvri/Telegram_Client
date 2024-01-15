# Telegram Client
Telegram-клиент (библиотека Telethon).

### Stack:
- Python 3.11;
- Django 5;
- Telethon;
- Redis;
- Celery;
- Docker.

### Установка и запуск (Docker):
- git clone https://github.com/Idvri/Telegram_Client.git;
- docker-compose up --build - в первый раз;
- docker-compose up.

### Доступность (адреса):
- http://127.0.0.1:8000;
- http://localhost:8000.

### Функционал (Endpoints):
- POST - http://localhost:8000/login/ - в теле запроса нужно передать номер ({"phone": "your_number"}), возвращает ссылку на QR-код, по которому можно войти в течение 1:30 (можно сгенерировать на сайте: https://www.qr-code-generator.com/).
После того, как сгенерировали код, нужно открыть камеру на своем устройстве через Telegram приложение (Настройки -> Устройства -> Подключить устройство) и навести на QR-код (выйти можно завершив сеанс в том же меню);

![login_post.png](responses%2Flogin_post.png)

- GET - http://localhost:8000/check/login?phone=your_number - возвращает статус аутентификации пользователя;

![check_login_get.png](responses%2Fcheck_login_get.png)

- GET - http://localhost:8000/messages?phone=your_number&uname=chat_username - возвращает ваши сообщений с собеседником (лимит: 50 шт.);

![messages_get.png](responses%2Fmessages_get.png)

- POST - http://localhost:8000/messages/ - в теле запроса нужно передать сообщение, ваш номер, логин получателя ({"message_text": "your_message", "from_phone":"your_phone", "username":"to_user"}), возвращает "ok", если сообщение отправлено;

![messages_post.png](responses%2Fmessages_post.png)

- GET - http://localhost:8000/wild?item=your_item - возвращает 10 наименований товаров со ссылками на них.

![wild_get.png](responses%2Fwild_get.png)