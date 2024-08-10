# Test_Task_MillionAgents
Привет! Это тестовое задание. В нём реализованы загрузка и скачивание файлов, очистка их по крону. Файл сохраняется локально, копия отсылается в S3 хранилище, а метаданные идут в PostgreSQL.

Инструкция:
- git clone https://github.com/CanICallYouJim/Test_Task_MillionAgents.git
  - в терминале войти в папку
- pip install -r requirements.txt
- создать базу в postgresql
  - в корне создать .env и .env.test с данными формата: DB_HOST = localhost
  DB_PORT = 5432
  DB_USER = postgres
  DB_NAME = million_agents
  DB_PASS = password
  MODE = PROD ИЛИ TEST СООТВЕТСТВЕННО
  
- запустить через main.py или команду в терминале fastapi run
