#!/bin/sh

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 9100 --ssl-certfile /linguisage/letsencrypt/live/api.linguisage.ru/fullchain.pem --ssl-keyfile /linguisage/letsencrypt/live/api.linguisage.ru/privkey.pem
