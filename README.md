# Django Store - Technical README

## Overview

This repository contains a Django-based e-commerce template project with:

- product catalog and category filtering
- shopping basket management
- checkout and payment processing via Stripe
- user authentication/authorization including GitHub OAuth
- asynchronous email delivery with Celery
- caching with Redis
- PostgreSQL as the primary database

The backend source code is located in `store-server`.

## Technology Stack

- `Django 6.0`
- `PostgreSQL` (via `psycopg`)
- `Redis` (cache + Celery broker/result backend)
- `Celery` for background tasks
- `Stripe` for payments and checkout sessions
- `django-allauth` for account flows and social login (GitHub)
- `django-debug-toolbar` and `django-extensions` for development

## Project Structure

Main Django apps:

- `products`:
  - `ProductCategory`, `Product`, `Basket` models
  - catalog listing, category pages, basket operations
  - catalog cache key/version helpers in `product_list_cache.py`
- `orders`:
  - order creation and order history
  - Stripe Checkout session creation
  - Stripe webhook handling and order status updates
- `users`:
  - custom `User` model
  - registration/login/profile/logout
  - email verification flow
  - GitHub social auth adapter

Core project package:

- `store/settings.py`: database/cache/email/Stripe/Celery/auth settings
- `store/urls.py`: app routes + Stripe webhook route
- `store/celery.py`: Celery app bootstrap and task autodiscovery

## Data Layer (PostgreSQL + ORM)

The project uses PostgreSQL as the default DB engine (`django.db.backends.postgresql`).

The domain models are implemented using Django ORM:

- catalog data (`ProductCategory`, `Product`)
- basket state (`Basket`)
- order snapshot (`Order.basket_history` as JSON)
- users and verification records (`User`, `EmailVerification`)

`Order.basket_history` stores a historical snapshot of purchased items (name, quantity, price, sum). This decouples the order record from future catalog changes.

## QuerySet API Usage

The project actively uses Django QuerySet API for filtering and performance:

- user-scoped filtering:
  - baskets: `Basket.objects.filter(user=request.user)`
  - orders: `Order.objects.filter(initiator=request.user)`
- relational optimization with `select_related("product")` for basket items
- ordering for stable UI:
  - products by `id`
  - baskets by `-created_timestamp`
  - orders by `-created`
- safer single-object retrieval:
  - `get_object_or_404(...)` for protected basket updates
  - `.filter(...).first()` when graceful fallback is preferred

This keeps query logic explicit and predictable across list/detail and mutation flows.

## Catalog and Basket Flow

Catalog:

- implemented with CBV (`ProductsListView`)
- supports pagination and category filtering
- product primary keys are cached and then resolved via ORM query

Basket:

- mix of CBV and FBV:
  - `BasketListView` (CBV) renders basket page and computed totals
  - `basket_add`, `basket_update`, `basket_remove` (FBV) mutate basket state
- all basket endpoints require authentication
- quantity is validated and capped by available `Product.quantity`

## Authentication and Authorization

### Local Authentication

Local account flow is implemented via:

- `UserRegistrationView` (registration + immediate login)
- `UserLoginView` (Django `LoginView`)
- `UserLogoutView` (explicit logout endpoint)
- `UserProfileView` protected by `LoginRequiredMixin`

Authorization strategy:

- route-level protection using `LoginRequiredMixin` and `@login_required`
- object-level scoping by always filtering user-owned records in queries

### GitHub OAuth Authentication

GitHub auth is provided through `django-allauth`:

- provider enabled: `allauth.socialaccount.providers.github`
- backend integration in `AUTHENTICATION_BACKENDS`
- social routes mounted under `/accounts/`

Custom behavior is implemented in `users/adapters.py`:

- for GitHub login, `is_verified_email` is set when an email is present

## Email Notifications

The project includes email verification notifications:

- `EmailVerification.send_verification_email()` prepares verification URL and message
- actual sending is delegated to Celery task `send_verification_email_task`
- SMTP configuration is managed via environment variables in settings:
  - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
  - SSL/TLS toggles

This design keeps web requests responsive while email is sent asynchronously.

## Stripe Payments

Stripe is integrated in two places:

1) Product synchronization:

- when a `Product` is saved, Stripe Product/Price objects are created or updated
- Stripe IDs are persisted in:
  - `Product.stripe_product_id`
  - `Product.stripe_product_price_id`

2) Checkout and payment confirmation:

- `OrderCreateView` builds Stripe Checkout line items from basket
- customer is redirected to hosted Stripe Checkout URL
- webhook endpoint `/webhook/stripe/` validates signatures and processes events
- on successful payment events, order status is transitioned from `CREATED` to `PAID`, and purchased basket rows are removed

## Celery: Why It Is Installed

Celery solves asynchronous/background execution requirements.

Current project responsibility:

- sending verification emails out of the request-response cycle

Why this matters:

- better user-perceived latency during registration
- retry/error isolation around external SMTP operations
- cleaner separation between web handling and slow I/O tasks

Configuration is loaded from `CELERY_*` settings and uses Redis as broker/result backend.

## Redis: Why It Is Installed

Redis is used for two separate concerns:

1) Cache backend (`django-redis`):

- caches product list PK sets for catalog/category pages
- supports cache invalidation via versioned keys

2) Celery infrastructure:

- message broker
- result backend

This improves response times for catalog endpoints and enables reliable background task orchestration.

## Django Fixtures

The project includes JSON fixtures in `products/fixtures/`:

- categories fixtures
- products fixtures

Fixtures are intended for local bootstrapping, demos, and deterministic test/dev data initialization.

Typical loading commands (from `store-server`):

```bash
python manage.py loaddata products/fixtures/categories.json
python manage.py loaddata products/fixtures/products.json
```

UTF-8 variants are also present and can be loaded similarly.

## Django Admin Implementation

Admin is configured with practical list tooling:

- `ProductAdmin`:
  - list display including Stripe IDs
  - category filter
  - inline edit for price/quantity
  - search and ordering
- `OrderAdmin`:
  - status display/editing
  - filters by status/creation date
  - search by user and customer fields
- `UserAdmin`:
  - basket data embedded via `BasketAdmin` inline
- `EmailVerificationAdmin`:
  - searchable audit of verification codes and time windows

Admin setup is focused on operational support for catalog/order/user management.

## CBV vs FBV and Mixins in This Codebase

The code intentionally combines both styles:

- CBV for structured pages and forms:
  - index, product list, basket list, profile, order list/detail/create
- FBV for compact imperative handlers:
  - basket mutations (`add/update/remove`)
  - Stripe webhook entrypoint

Mixins used:

- `LoginRequiredMixin` for access control on class-based views
- `SuccessMessageMixin` for user feedback in auth forms

This hybrid approach keeps complex render flows organized (CBV) while retaining concise handlers for simple state changes (FBV).

## Environment Variables (Key Settings)

Set these values in your environment before running:

- Django/security: `SECRET_KEY`, `DEBUG`
- PostgreSQL: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- Redis/cache: `REDIS_URL`, `USE_REDIS`
- Celery: `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- Stripe: `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_ENDPOINT_SECRET`
- Email/SMTP: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

## Local Run (Development)

From `store-server`:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Run Redis (example via Docker Compose):

```bash
docker compose up redis
```

Run Celery worker:

```bash
celery -A store worker -l info
```

and enjoy ٩(◕‿◕｡)۶

If you want to receive Stripe webhook events locally, use Stripe CLI and point it to `/webhook/stripe/`.