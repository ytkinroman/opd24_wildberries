import datetime
import re
import emoji
import random


def get_tg_user_request_time() -> str:
    """Получаем время запроса."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S (%d/%m/%Y)")
    return current_time


def extract_url(text) -> str | None:
    """Находит ссылку в тексте."""
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    match = re.search(regex, text)
    if match:
        return match.group(0)  # Возвращаем найденную ссылку.
    else:
        return None


def replace_emoji(comments):
    """Заменяет эмодзи на текст."""
    replaced_comments = []
    for comment in comments:
        replaced_comment = emoji.demojize(comment, language='ru', delimiters=(" <", "> "))
        replaced_comments.append(replaced_comment)
    return replaced_comments


def remove_newline(sentences):
    """Удаляет символы абзаца."""
    cleaned_sentences = []
    for sentence in sentences:
        cleaned_sentence = re.sub(r'\n', '', sentence)
        cleaned_sentences.append(cleaned_sentence)
    return cleaned_sentences


def get_random_message(messages_list: tuple[str]) -> str:
    """Функция возвращает случайное значение из картежа."""
    message = random.choice(messages_list)
    return message


def remove_double_spaces(lst: list[str]) -> list[str]:
    """
    Удаляет двойные пробелы и пробелы в конце строк из списка.
    """
    cleaned_list = []
    for string in lst:
        cleaned_string = string.strip().replace("  ", " ")
        cleaned_list.append(cleaned_string)
    return cleaned_list
