# transactions_app
Тестовое задание: “Микросервис анализа финансовых транзакций”
# функционал Эндпоинты

##### POST /transactions — загрузка транзакции

Входные данные:
```json
{
  "transaction_id": "123456",
  "user_id": "user_001",
  "amount": 150.50,
  "currency": "USD",
  "timestamp": "2024-12-12T12:00:00"
}
```
Логика:
Сохраняет транзакцию в базу.
Отправляет задачу в очередь на обновление статистики.
Ответ:
```json
{
  "message": "Transaction received",
  "task_id": "abcd1234"
}
```
 
##### DELETE /transactions — удаление всех транзакций
Логика:
Удаляет все транзакции из базы данных.
Удаляет всю статистику и закешированные данные

 
##### GET /statistics — получение статистики по транзакциям
Логика:
Возвращает:
Общее количество транзакций.
Среднюю сумму транзакции.
Топ-3 самых крупных транзакций.
 Пример ответа:
```json
{
  "total_transactions": 25,
  "average_transaction_amount": 180.03,
  "top_transactions": [
    {"transaction_id": "1", "amount": 1000},
    {"transaction_id": "2", "amount": 850},
    {"transaction_id": "3", "amount": 500}
  ]
}
```
# Используемые технологии
- FastAPI
- SQLAlchemy + PostgreSQL
- Docker/Docker Compose
- Celery + Redis для асинхронной обработки.
# Как запустить
для начала скопируйте репозиторий
```commandline
git clone https://github.com/AlbertSabirzianov/transactions_app.git
```
перейдите в каталог проекта
```commandline
cd transactions_app
```
создайте докер образ приложения
```commandline
docker build -t test_app:latest -f docker/Dockerfile ./src/. 
```
перейдите в каталог докера
```commandline
cd docker
```
измените при необходимости переменные окружения в файле .env.example
```text
# подключение к базе данных
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
# ключь авторизации для приложения
API_KEY=key
```
запустите всё приложение включая базу данных postgres, воркер celery и redis одной командой
```commandline
docker compose --env-file .env.example up
```