import requests

from asyncio import sleep

from telethon import TelegramClient

from django.db import IntegrityError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.request import Request
from rest_framework.utils import json

from config.settings import API_ID, API_HASH

from api.utils import create_db_user, find_db_user, get_wb_request_url, get_item_link
from api.tasks import login_background


# Create your views here.
@csrf_exempt
async def login(request: Request) -> JsonResponse:
    """Endpoint для аутентификации пользователя в telegram-клиенте по QR-коду."""

    if request.method == 'POST':
        if not request.body:
            return JsonResponse({'message': 'You need to input your number.'})

        try:
            phone = json.loads(request.body)['phone']
        except KeyError:
            return JsonResponse({'message': 'You need to input your number.'})

        client = TelegramClient(str(phone), API_ID, API_HASH)
        await client.connect()

        auth_status = await client.is_user_authorized()
        if auth_status is True:
            client.disconnect()
            return JsonResponse({'message': 'You already logged in.'})

        try:
            await create_db_user(int(phone))
        except IntegrityError:
            db_user = await find_db_user(int(phone))
            if db_user.qr_link:
                client.disconnect()
                return JsonResponse({'message': f'You already have QR-link.'})
        login_background.delay(str(phone))  # Отправляем task в очередь для создания QR-кода и сохранения его
        # ссылки в БД.
        await sleep(5)
        db_user = await find_db_user(int(phone))  # Получаем ссылку на QR-код из БД.
        client.disconnect()
        return JsonResponse({'qr_link_url': f'{db_user.qr_link}'})


async def check_login(request: Request) -> JsonResponse:
    """Endpoint для получения информации по статусу пользователя из БД."""

    if request.method == 'GET':
        phone = request.GET.get('phone')
        db_user = await find_db_user(int(phone))
        if db_user:
            return JsonResponse({'status': f'{db_user.login_status}'})
        return JsonResponse({'message': f'User didn\'t start auth process in this telegram-client.'})


@csrf_exempt
async def messages(request: Request) -> JsonResponse:
    """Endpoint для получения и отправки сообщений."""

    if request.method == 'GET':
        phone = request.GET.get('phone')
        uname = request.GET.get('uname')
        if not phone or not uname:
            return JsonResponse(
                {'detail': 'You should enter your phone or uname.'},
                json_dumps_params={'ensure_ascii': False}
            )

        client = TelegramClient(phone, API_ID, API_HASH)
        await client.connect()

        auth_status = await client.is_user_authorized()
        if auth_status is False:
            return JsonResponse({'message': 'You need to login.'})

        client_messages = await client.get_messages(entity=uname, limit=50)
        messages_list = [
            {
                'username': uname,
                'is_self': message.out,
                'message_text': message.message
            }
            for message in client_messages
        ]

        client.disconnect()
        return JsonResponse({'messages': messages_list}, json_dumps_params={'ensure_ascii': False})

    elif request.method == 'POST':
        data = json.loads(request.body)
        client = TelegramClient(data['from_phone'], API_ID, API_HASH)
        await client.connect()

        auth_status = await client.is_user_authorized()
        if auth_status is False:
            return JsonResponse({'message': 'You need to login.'})

        try:
            await client.send_message(message=data['message_text'], entity=data['username'])
        except Exception:
            client.disconnect()
            return JsonResponse({'status': 'error'})

        client.disconnect()
        return JsonResponse({'status': 'ok'})


async def wild(request: Request) -> JsonResponse:
    """Endpoint для получения списка товаров с WB."""

    if request.method == 'GET':
        item = request.GET.get('item')
        wild_items = requests.get(get_wb_request_url(item))
        items = json.loads(wild_items.text)['data']['products']
        items = [{item['name']: get_item_link(item['id'])} for item in items]
        return JsonResponse({'items': items}, json_dumps_params={'ensure_ascii': False})
