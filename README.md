# django_stripe
# Django Stripe Integration

Проект реализует интеграцию Django с платежной системой Stripe, включая мультивалютные платежи, систему заказов, скидки и налоги.

## 🌟 Особенности проекта

- 💳 **Мультивалютные платежи** (USD, EUR)
- 🛒 **Система заказов** с группировкой товаров
- 🎁 **Автоматические скидки** и **налоги**
- 🧾 **Stripe Checkout** для безопасных платежей
- ⚙️ **Админ-панель** для управления данными
- 🐳 **Docker-контейнеризация** для простого развертывания
- 🔒 **Переменные окружения** для защиты ключей
- 📊 **Интеграция налогов и скидок** в платежи Stripe

## 🚀 Запуск через Docker (рекомендуется)

### Требования
- Docker 20.10+
- Docker Compose 2.0+
- Stripe API ключи (тестовые)

### Шаги установки

1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/FieryHop/django_stripe

## Отредактируйте .env файл, добавив ваши Stripe API ключи:

env
# Stripe Keys (USD)
STRIPE_PUBLIC_KEY_USD=Ваш публ. ключ
STRIPE_SECRET_KEY_USD=Ваш секр. ключ

# Stripe Keys (EUR)
STRIPE_PUBLIC_KEY_EUR=Ваш публ. ключ
STRIPE_SECRET_KEY_EUR=Ваш секр. ключ

# Django
SECRET_KEY=ваш django секр. ключ
DEBUG=True

## Запустите контейнеры:

bash
docker-compose up --build -d
## Примените миграции:

bash
docker-compose exec web python manage.py migrate
## Загрузите тестовые данные:

bash
docker-compose exec web python manage.py loaddata items.json
## Создайте администратора:

bash
docker-compose exec web python manage.py createsuperuser
## Приложение доступно по адресу:
http://localhost:8000

### 🛠 Использование проекта
## Основные эндпоинты
# Эндпоинт	Метод	Описание
/item/<id>/	GET	Страница товара с кнопкой оплаты
/buy/<id>/	GET	Получение Stripe Session ID товара
/order/<id>/	GET	Страница заказа с кнопкой оплаты
/buy_order/<id>/	GET	Получение Stripe Session ID заказа
/admin/	GET	Административная панель
#Работа с товарами
#Просмотр товара:

Откройте: http://localhost:8000/item/1/

## Вы увидите информацию о товаре и кнопку "Buy"

## Оплата товара:

## Нажмите "Buy"

## Вы будете перенаправлены на страницу Stripe Checkout

# Используйте тестовую карту: 4242 4242 4242 4242

### Работа с заказами
## Создайте заказ через админ-панель:

# Перейдите: http://localhost:8000/admin

# Логин: admin (по умолчанию)

# Пароль: установленный при создании суперпользователя

### Создайте заказ в разделе "Orders"

## Просмотр заказа:

# Откройте: http://localhost:8000/order/1/

# Вы увидите список товаров, общую сумму, скидки и налоги

# Оплата заказа:

# Нажмите "Pay Now"

# Процесс оплаты аналогичен оплате товара

# Примеры API запросов
# Получить информацию о товаре:

bash
curl http://localhost:8000/item/1/
Получить Stripe Session ID для оплаты товара:

bash
curl http://localhost:8000/buy/1/
Получить информацию о заказе:

bash
curl http://localhost:8000/order/1/
Получить Stripe Session ID для оплаты заказа:

bash
curl http://localhost:8000/buy_order/1/
