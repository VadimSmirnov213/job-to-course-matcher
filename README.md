# Course Recommendation System

Система рекомендации образовательных курсов по вакансиям. Пользователь передаёт URL вакансии (hh.ru), система парсит требования и возвращает топ-N релевантных курсов на основе TF-IDF и косинусного сходства.

## Архитектура

Монорепозиторий из трёх модулей:

| Модуль | Назначение |
|--------|------------|
| frontend | SPA на React, UI для ввoда URL и отображения рекомендаций |
| backend | FastAPI-сервер, Celery-воркеры, MongoDB, Redis |
| ML-Functions-Data | Сбор и анализ вакансий hh.ru, ML-скрипты |

## Структура

```
Project1/
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── @types/
│   │   │   └── types.d.ts          # IUser, ICourse, SkillContextType
│   │   ├── components/
│   │   │   ├── analysis/           # Страница рекомендаций по URL вакансии
│   │   │   │   ├── Analysis.tsx
│   │   │   │   └── style.css
│   │   │   ├── auth/               # Авторизация
│   │   │   ├── catalogue/          # Каталог курсов
│   │   │   ├── context/
│   │   │   │   └── SkillContext.tsx # Глобальный контекст user, courses
│   │   │   ├── home/
│   │   │   ├── profile/
│   │   │   ├── reg/                # Регистрация
│   │   │   ├── sidebar/
│   │   │   └── ui/
│   │   │       └── CourseCard.tsx
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── package.json
│   └── tsconfig.json
│
├── backend/
│   └── backend/
│       ├── docker-compose.yml       # mongodb, redis, server_cfo, celery_worker, celery_flower
│       ├── prod.py
│       ├── redis/
│       │   ├── Dockerfile
│       │   └── redis.conf
│       ├── server/
│       │   ├── main.py             # FastAPI app, CORS, Redis cache
│       │   ├── config.py            # DB_HOST, REDIS_*, aws_*
│       │   ├── cel_que.py           # Celery tasks: get_dict, get_recommendations
│       │   ├── database.py
│       │   ├── storage.py
│       │   ├── routers/
│       │   │   ├── user.py
│       │   │   ├── course.py
│       │   │   ├── feedback.py
│       │   │   ├── models.py        # /api/predict/recommendation
│       │   │   └── avatars.py
│       │   ├── managers/
│       │   │   ├── user.py
│       │   │   ├── course.py
│       │   │   ├── feedback.py
│       │   │   └── vacs.py
│       │   ├── schemas/
│       │   │   ├── user.py
│       │   │   ├── course.py
│       │   │   └── feedback.py
│       │   ├── buckets/
│       │   │   └── avatar.py        # S3 для аватаров
│       │   ├── ml/
│       │   │   ├── main.py          # process_data, calculate_similarity (TF-IDF, SVD)
│       │   │   └── vaca.py         # DataCollector — парсинг вакансии по URL
│       │   ├── requirements.txt
│       │   └── Dockerfile
│       └── service1/               # Вспомогательные скрипты (course, vacancy, database)
│           ├── course.py
│           ├── vacancy.py
│           ├── database.py
│           ├── vacancy1.csv
│           └── my_data.csv
│
└── ML-Functions-Data/
    ├── hh_research/
    │   ├── researcher.py           # Точка входа: ResearcherHH
    │   ├── vacancy_by_link.py
    │   ├── soed.py
    │   ├── settings.json
    │   ├── requirements.txt
    │   ├── vacancy_list.csv
    │   ├── courses_list.csv
    │   └── src/
    │       ├── parser.py            # Settings
    │       ├── data_collector.py     # Сбор вакансий с hh.ru
    │       ├── currency_exchange.py # Exchanger
    │       ├── analyzer.py          # Analyzer, prepare_df, analyze_df
    │       ├── predictor.py
    │       └── notebooks/
    │           └── hh_analytics.ipynb
    └── ML/
        ├── MainProst.py
        ├── MainProst2.py
        ├── DataWork.py
        ├── form.py
        ├── Real_time.py
        ├── big_real_time.py
        └── new_one.py
```

## Стек

- **Frontend:** React 18, TypeScript, Material UI, React Router
- **Backend:** FastAPI, Uvicorn, Motor (MongoDB), Redis, Celery, Flower
- **ML:** scikit-learn (TfidfVectorizer, cosine_similarity, SVD), BeautifulSoup4

## Запуск

### Backend (Docker)

```bash
cd backend/backend
docker-compose up -d
```

Сервисы: MongoDB (27017), Redis (6379), API (9000), Celery worker, Flower (5555).

### Frontend

```bash
cd frontend
npm install
npm start
```

Приложение: http://localhost:3000

### Переменные окружения (backend)

```bash
cp backend/backend/server/.env.example backend/backend/server/.env-prod
```

Заполнить `backend/backend/server/.env-prod`:

- DB_HOST, DB_PORT, DB_NAME — MongoDB
- REDIS_HOST, REDIS_PORT, REDIS_NAME — Redis
- aws_access_key_id, aws_secret_access_key — S3 (аватары), опционально

## API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /api/predict/recommendation?top=N&url=... | Рекомендации курсов по URL вакансии |

Рекомендации считаются через Celery: задача `get_dict` парсит вакансию, `get_recommendations` строит TF-IDF-матрицу, применяет SVD и возвращает топ-N курсов по косинусному сходству.

## ML-Functions-Data

Модуль `hh_research` — standalone-скрипты для сбора и анализа вакансий:

```bash
cd ML-Functions-Data/hh_research
pip install -r requirements.txt
python researcher.py
```

`ML/` — вспомогательные скрипты (DataWork, MainProst и др.), не входят в основной пайплайн рекомендаций.
