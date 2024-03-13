***DRF Project***
===

Это веб-приложение на django DRF в котором каждый может создавать для пользователей курсы с уроками для хранения в них своих знаний!

После запуска контейнера с приложением, он будет доступен по локальному адресу `http://localhost:8000/`

---
**Структура сайта:**
-
Все подродно описано в документации приложения по адресам:
`http://localhost:8000/swagger/`
`http://localhost:8000/redoc/`

---

Для начала работы вам необходимо зарегистрировать пользователя.
Далее можно создавать курсы и заполнять их уроками.
Затем мы вожете подписываться на курсы других пользователей и получать письма, если уроки получили изменения.
Также присатсвует интеграция с платежной системой [`Stripe`](stripe.com/docs).
Автор курса может назначить на него цену, а любой желающий может его купить.
Для тестовой покупки можно использовать карту `4242 4242 4242 4242`     `02/24`   `000`
Аккаунты неактивных пользователей автоматическт удаляются по истечению месяца.


Присутсвует админка:
`http://localhost:8000/admin/`

---
Все необходиммые данные стрятанны в переменные окружения!

---
Для приложения предусмотрен docker контейнер!
Для быстрого запуска контейнера предусмотрены команды:
-
````
docker-compose build
docker-compose up
````
