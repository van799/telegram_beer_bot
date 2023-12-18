### Краткое описание телеграмм бота BeerBot

    Telegram бот помогает отслеживать и запоминать все выпитые и купленые напитки.
![Image alt](https://github.com/van799/telegram_beer_bot/blob/main/beer_bot.png)
## Локальный запуск приложения

### 1. Заполнить файл переменных среды .env (см. ниже)

### 2. Поднять контейнер с MINIO и LibreTranslate

    ```shell
    $ python run main.py
    ```

### 2.1 Запустить тесты


### 3. Telegram bot доступен в telegram-e по адресу https://t.me/community_pivo_bot

### Шаблон наполнения env-файла

```
BOT_TOKEN=6814148393:AAE0qki3Hz5L7DPEUtSI8ssCp7KIeqoR8xA
ADMIN_IDS=1111111
DEBUG=True
```

## Пояснение к запуску:

    В режиме дебага телеграмм бот работаает с БД SQLITE. 
    Для запуска Telegram бота с БД Postgres, выключите отладочный режим 
    DEBUG=False.
    Предполагется что этот телеграмм бот используется в группе друзей которые имеют к нему доступ
    поэтому нужно прописать id пользователей, с следующем виде: ADMIN_IDS=1111111

    


