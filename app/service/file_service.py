import asyncio
import os
import random
import aiohttp
from uuid import uuid4


class FileService:
    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)  # Создаем директорию, если ее нет

    async def save_image(self, url: str) -> str:
        """Асинхронно скачивает изображение
        и сохраняет его с уникальным именем."""
        await asyncio.sleep(random.uniform(1, 3))

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # Генерируем уникальный ID и имя файла
                    file_id = str(uuid4())
                    file_path = os.path.join(self.directory, f"{file_id}.jpg")

                    # Сохраняем изображение
                    with open(file_path, "wb") as f:
                        f.write(await response.read())

                    return file_id  # Возвращаем ID, который можно сохранить в модели
                else:
                    raise Exception(
                        f"Не удалось скачать изображение."
                        f" Статус код: {response.status}"
                    )
