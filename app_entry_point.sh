#!/bin/sh

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 9100 --ssl-certfile=cert/fullchain.pem --ssl-keyfile=cert/privkey.pem
