import os
import json
import aiofiles

__version__ = "2.1.1"
__author__ = "ytkinroman"


async def get_generation_json(user_name: str, user_id: str, comments: list[dict], date: str, path: str) -> str:
    data_list = {
        "user_name": user_name,
        "user_id": user_id,
        "date": date,
        "comments": comments
    }

    os.makedirs(path, exist_ok=True)

    # ТУТ НУЖНО СОЗДАТЬ JSON ФАЙЛ И СОХРАНИТЬ В ДИРЕКТОРИЮ С НАЗВАНИЕМ file-{user_name}-{user_id}-{date}.json
    file_name = f"file--{user_name}--{user_id}--[{(date.replace(':', '-')).replace('/', '-')}].json"  # Проблема, недопустимые символы, из-за этого костыль ...
    full_path = os.path.join(path, file_name)
    # print(full_path)

    try:
        async with aiofiles.open(full_path, "w", encoding="utf-8") as json_file:
            await json_file.write(json.dumps(data_list, ensure_ascii=False, indent=4))
        return full_path
    except Exception as e:
        return "ERROR_JSON"
