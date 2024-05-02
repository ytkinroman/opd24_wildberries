import json
import os
import json

__version__ = "2.0.0"
__author__ = "ytkinroman"


def get_generation_json(user_name: str, user_id: str, comments: list[dict], date: str, path: str) -> str:
    data_list = {
        "user_name": user_name,
        "user_id": user_id,
        "date": date,
        "comments": comments
    }

    os.makedirs(path, exist_ok=True)

    # ТУТ НУЖНО СОЗДАТЬ JSON ФАЙЛ И СОХРАНИТЬ В ДИРЕКТОРИЮ С НАЗВАНИЕМ file-{user_name}-{user_id}-{date}.json
    file_name = f"file--{user_name}--{user_id}--{(date.replace(':', '-')).replace('/', '-')}.json"  # Проблема, недопустимые символы, из-за этого костыль ...
    full_path = os.path.join(path, file_name)
    # print(full_path)

    with open(full_path, "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    return full_path
