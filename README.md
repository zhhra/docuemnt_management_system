# DMS

DMS is a Django-based application for managing documents. It runs using Docker and leverages PostgreSQL for the database and MinIO for object storage.

---

## Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Clone the Project

---

## Setup Environment

Copy the sample environment file:

```cp .env.sample .env```

Open .env and update any environment variables as needed.

Start docker with:

```docker compose up (-d)```

Run the below command:

```docker compose exec web python manage.py define_groups```

---

## Useful Commands

- Start all services:

```docker compose up (-d)```

- Live docker logs:

```docker compose logs -f```

- Stop the services:

```docker compose down```

- Apply django migrations:

```docker compose exec web python manage.py migrate```

- To create a super user:

```docker compose exec web python manage.py createsuperuser```

- To add static files:

```docker compose exec web python manage.py collectstatic```

- To add static files:

```docker compose exec web python manage.py test```

- To get in app bash:

```docker compose exec -it web /bin/bash```