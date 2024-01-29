import asyncio
import bcrypt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        await asyncio.sleep(0.1)
        if username == "admin" and password == settings.ADMIN_PASSWORD:
            hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            request.session.update({"token": hash_password.decode("utf-8")})

            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        if bcrypt.checkpw(
            password=settings.ADMIN_PASSWORD.encode(),
            hashed_password=token.encode(),
        ):
            return True

        return False


authentication_admin_backend = AdminAuth(secret_key=settings.SESSION_SECRET)
