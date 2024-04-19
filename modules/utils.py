import datetime


def get_tg_user_request_time() -> str:
    """Получаем время запроса."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    return current_time

