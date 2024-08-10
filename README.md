# Test_Task_MillionAgents
Привет! Это тестовое задание. В нём реализованы загрузка и скачивание файлов, очистка их по крону. Файл сохраняется локально, копия отсылается в S3 хранилище, а метаданные идут в PostgreSQL.

Инструкция:
- git clone https://github.com/CanICallYouJim/Test_Task_MillionAgents.git
  - в терминале войти в папку
- pip install -r requirements.txt
- создать 2 базы данных в postgresql - продакшн и для тестов
  - в корне создать файлы .env и .env.test соответственно с переменными:
  ```makefile
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_NAME=prod_db_name ИЛИ test_db_name
    DB_PASS=password
    MODE=PROD ИЛИ TEST
  ``` 
- запустить через main.py или команду в терминале fastapi run
