from telethon import TelegramClient
from telethon.tl.custom import QRLogin

from asgiref.sync import sync_to_async

from api.models import User


async def get_qr(client: TelegramClient) -> QRLogin:
    """Функция для получения QR-кода."""
    qr = await client.qr_login()
    return qr


@sync_to_async
def create_db_user(phone: int) -> User:
    """Функция для создания в БД пользователя, в контексте асинхронной функции."""

    db_user = User.objects.create(phone=phone)
    return db_user


@sync_to_async
def find_db_user(phone: int) -> User:
    """Функция для получения из БД пользователя, в контексте асинхронной функции."""

    db_user = User.objects.filter(phone=phone).first()
    return db_user


@sync_to_async
def login_status_update(phone: int, status: str, telegram_id: str = None) -> None:
    """Функция для сохранения статуса входа и telegram_id в БД, в контексте асинхронной функции."""

    db_user = User.objects.filter(phone=phone).first()
    if status in ('error', 'logined', 'logged_out'):
        db_user.qr_link = None

    if telegram_id:
        db_user.telegram_id = telegram_id

    db_user.login_status = status
    db_user.save()


@sync_to_async
def set_qr_to_user(phone: int, qr_link: str) -> None:
    """Функция для сохранения ссылки QR-кода в БД, в контексте асинхронной функции."""
    db_user = User.objects.filter(phone=phone).first()
    db_user.qr_link = qr_link
    db_user.save()


def get_wb_request_url(item: str) -> str:
    """Функция получения ссылки для совершения запроса к WB."""

    return f'https://search.wb.ru/exactmatch/ru/common/v4/search?curr=rub&dest=-1257786&query={item}&city=Moscow' \
           f'&resultset=catalog&limit=10'


def get_item_link(item_id):
    """Функция получения ссылки товара."""

    return f'https://www.wildberries.ru/catalog/{item_id}/detail.aspx'
