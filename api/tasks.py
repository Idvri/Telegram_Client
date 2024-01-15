import asyncio

from asyncio.exceptions import TimeoutError

from telethon import TelegramClient

from celery import shared_task
from celery.utils.log import get_task_logger

from config.settings import API_ID, API_HASH

from api.utils import get_qr, set_qr_to_user, login_status_update

logger = get_task_logger(__name__)


@shared_task
def login_background(phone) -> None:
    """Task для воспроизведения ожидания введения QR-кода пользователем."""

    client = TelegramClient(phone, API_ID, API_HASH)

    async def login_task(tel_client: TelegramClient) -> None:
        await tel_client.connect()
        qr = await get_qr(tel_client)  # Получаем QR-код.

        await set_qr_to_user(phone=int(phone), qr_link=qr.url)  # Сохраняем QR-код в БД для предоставления ссылки на
        # него в endpoint'е для аутентификации.
        await login_status_update(phone=int(phone), status='waiting_qr_login')
        try:
            await qr.wait(90)  # Ждём полторы минуты, пока клиент не войдёт по QR-коду.
        except TimeoutError:
            await login_status_update(phone=int(phone), status='error')
        else:
            user = await tel_client.get_me()
            await login_status_update(phone=int(phone), status='logined', telegram_id=user.id)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_task(tel_client=client))
    client.disconnect()
