import threading

from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.users.models import User


pending_registrations_dict = {}
pending_registrations_lock = threading.Lock()


def start_registration(user_id: str) -> str:
    with pending_registrations_lock:
        if user_id in pending_registrations_dict:
            return "Você ja iniciou o processo de registro. Por favor, envie seu número de celular."
        pending_registrations_dict[user_id] = True

    return "Por favor, envie seu número de celular para se registrar."


def is_pending_registration(user_id: str) -> bool:
    with pending_registrations_lock:
        return pending_registrations_dict.get(user_id, False)


def finish_registration(user_id: str, phone_number: str) -> str:
    with pending_registrations_lock:
        if user_id not in pending_registrations_dict:
            return "Você não iniciou o processo de registro. Por favor, envie /register para começar."

    if not phone_number.startswith('+') or not phone_number[1:].isdigit():
        return "Número de celular inválido. Por favor, envie um número no formato +1234567890."
    
    if TelegramUserSettings.objects.filter(telegram_id=user_id).exists():
        with pending_registrations_lock:
            pending_registrations_dict.pop(user_id)
        return "Você já está registrado."

    user = User.objects.filter(phone_number=phone_number).first()
    if not user:
        with pending_registrations_lock:
            pending_registrations_dict.pop(user_id)
        return "Número de celular não encontrado. Por favor, registre-se no site primeiro."

    TelegramUserSettings.objects.create(
        user=user,
        telegram_id=user_id,
        phone_number=phone_number,
    )

    with pending_registrations_lock:
        pending_registrations_dict.pop(user_id)

    return "Registro concluído com sucesso!"
