import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token:
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("유효하지 않은 토큰입니다.")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("존재하지 않는 유저입니다.")


def ws_authenticate(scope):
    headers = dict(scope["headers"])
    token = ""
    print(dict(scope))
    if b"jwt" in headers:
        token = headers[b"jwt"].decode("utf-8")
    else:
        token = scope["query_string"].decode("utf-8")
    # token = request["headers"]["Jwt"]
    if not token:
        return None
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
    )
    pk = decoded.get("pk")
    if not pk:
        raise AuthenticationFailed("유효하지 않은 토큰입니다.")
    try:
        user = User.objects.get(pk=pk)
        return (user, None)
    except User.DoesNotExist:
        raise AuthenticationFailed("존재하지 않는 유저입니다.")
