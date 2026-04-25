# REST API для горных перевалов

Проект разработан на Django и Django REST Framework.

API предназначен для добавления, просмотра и редактирования информации о горных перевалах.

---

## Используемые технологии

- Python
- Django
- Django REST Framework
- SQLite / PostgreSQL

---

## Запуск проекта

### 1. Клонировать проект

```bash
git clone <ссылка_на_репозиторий>
cd <название_проекта>
2. Создать виртуальное окружение
python -m venv venv
3. Активировать виртуальное окружение
Windows:
venv\Scripts\activate
Linux / MacOS:
source venv/bin/activate
4. Установить зависимости
pip install -r requirements.txt
5. Выполнить миграции
python manage.py migrate
6. Запустить сервер
python manage.py runserver
Базовый URL
http://127.0.0.1:8000/
Методы API
1. Добавление нового перевала
Запрос:
POST /submitData/
Пример JSON:
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "user": {
    "email": "test@example.com",
    "fam": "Иванов",
    "name": "Иван",
    "otc": "Иванович",
    "phone": "+79999999999"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {
      "data": "base64_string",
      "title": "Фото перевала"
    }
  ]
}
Ответ:
{
  "status": 200,
  "message": "Отправлено успешно",
  "id": 1
}
2. Получить перевал по id
Запрос:
GET /submitData/<id>
Пример:
GET /submitData/1
Ответ:
{
  "id": 1,
  "beauty_title": "пер.",
  "title": "Пхия",
  "status": "new"
}
3. Редактирование перевала
Запрос:
PATCH /submitData/<id>
Пример:
PATCH /submitData/1

Редактирование возможно только если статус записи:

new
Нельзя изменять:
Фамилию
Имя
Отчество
Email
Телефон
Успешный ответ:
{
  "state": 1,
  "message": "Запись успешно обновлена"
}
Ошибка:
{
  "state": 0,
  "message": "Редактирование запрещено"
}
4. Получить все записи пользователя по email
Запрос:
GET /submitData/?user__email=test@example.com
Ответ:
[
  {
    "id": 1,
    "title": "Пхия",
    "status": "new"
  },
  {
    "id": 2,
    "title": "Эльбрус",
    "status": "pending"
  }
]
Статусы модерации
Статус	Значение
new	новая запись
pending	на модерации
accepted	принято
rejected	отклонено
Коды ответа сервера
Код	Описание
200	Успешно
201	Создано
400	Ошибка запроса
404	Не найдено
405	Метод не разрешён