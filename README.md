<h1 align="center">Тестовое задание Python Backend</h1>
<h2 align="center">

</h2>

## Описание

**Что из себя представляет сервер:**

Backend-сервер, отвечающий на http запросы, написан на фреймворке sanic
## Доступные запросы (routes):

###HealthEndpoint
uri = '/' 

Методы = ['GET', 'POST']

Проверка работоспособности сервера

###CreateUserEndpoint
uri = '/user' 

Методы = ['POST']

Создание пользователя для работы с сервером. Поля в body запроса:

<ul>
<li>login - str, обязательное</li>
<li>password - str, обязательное</li>
<li>first_name - str, обязательное</li>
<li>last_name - str, обязательное</li>
</ul>

###AuthUserEndpoint
uri = '/user/auth' 

Методы = ['POST']

Авторизация пользователя. Поля в body запроса:

<ul>
<li>login - str, обязательное</li>
<li>password - str, обязательное</li>
</ul>

###UserEndpoint
uri = '/user/{id пользователя}' 

Методы = ['PATCH', 'DELETE']

Необходима авторизация

Редактирование или удаление пользователя (доступно только самому пользователю). Поля в body запроса PATCH:

<ul>
<li>first_name - str</li>
<li>last_name - str</li>
</ul>

###AllUserEndpoint
uri = '/user/all' 

Методы = ['GET']

Необходима авторизация

Получение списка всех пользователей

###ParseLogsEndpoint

uri = '/parse' 

Методы = ['GET']

Необходима авторизация

Парсинг логов из файла logs.txt в папке проекта, помещение обработанных данных в БД.

###ReportEndpoint
uri = '/report/{порядковый номер отчета}' 

Методы = ['GET']

Необходима авторизация

Получение отчетов из списка:
<ol>
<li>Посетители из какой страны чаще всего посещают сайт</li>
<li>Посетители из какой страны чаще всего интересуются товарами из определенной категории “fresh_fish”</li>
<li>В какое время суток чаще всего просматривают категорию “frozen_fish”
</li>
<li>Какое максимальное число запросов на сайт за астрономический час (c 00 минут 00 секунд до 59 минут 59 секунд)?
</li>
<li>Товары из какой категории чаще всего покупают совместно с товаром из категории “semi_manufactures”
</li>
<li>Сколько не оплаченных корзин имеется
</li>
<li>Какое количество пользователей совершали повторные покупки?
</li>
</ol>

## Об архитектуре сервера
<img src="https://habrastorage.org/r/w1560/files/23a/0de/4d9/23a0de4d93d747c89f1e216077c2d604.jpg">
Когда на сервер приходит request, он проходит следующий путь:
<ul>
<li>transport (sanic)</li>
<li>API (marshmallow)</li>
<li>service</li>
<li>DB (model)</li>
<li>DB (query)</li>
</ul>

Response от сервера проходит этот путь в обратном направлении.

Подробнее про чистую архитектуру можно почитать <a href="Адрес">тут</a>

## Установка и запуск сервера

Необходимо, но не обязательно, в переменных окружение указать следующие параметры:
<ul>
<li>host - str</li>
<li>port - int</li>
<li>workers - int</li>
<li>debug - bool</li>
<li>secret - str</li>
<li>ipinfo_token - токен для библиотеки ipinfo</li>
</ul>

Затем применить последнюю миграцию и создать БД командой:
```
alembic upgrade head
```
А после:
```
python main.py
```