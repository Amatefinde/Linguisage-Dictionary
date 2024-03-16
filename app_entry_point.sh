#!/bin/sh

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 9100 --ssl-certfile=/linguisage/cert/fullchain.pem --ssl-keyfile=/linguisage/cert/privkey.pem
