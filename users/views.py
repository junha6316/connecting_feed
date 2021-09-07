from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.response import Response
from rest_framework.request import Request

from .models import User
from users.tokens import AccessToken, RefreshToken, Token


@api_view(["POST"])
@permission_classes((AllowAny,))
def token(request: Request) -> Response:
    username: str = request.data.get("username")
    password: str = request.data.get("password")

    if not username or not password:
        return Response(
            status=HTTP_400_BAD_REQUEST, data={"detail": "회원정보가 입력되지 않았습니다."}
        )

    user: User = authenticate(username=username, password=password)
    if user is not None:
        access_token: str = AccessToken(pk=user.pk).encode()
        refresh_token: str = RefreshToken(pk=user.pk).encode()
        user.refresh_token = refresh_token
        user.save()
        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=HTTP_200_OK,
        )
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes((AllowAny,))
def refresh_token(request: Request) -> Response:

    refresh_token: str = request.data.get("refresh_token")
    if not refresh_token:
        return Response(status=HTTP_400_BAD_REQUEST, data={"detail": "토큰이 입력되지 않았습니다."})
    token: RefreshToken = Token.decode(refresh_token)
    try:
        user = User.objects.get(pk=token.pk)
        if user.refresh_token != refresh_token:
            return Response(
                HTTP_400_BAD_REQUEST, {"detail": "Refresh Toekn is invalid"}
            )

        if not token.is_validate():
            return Response(
                HTTP_400_BAD_REQUEST, {"detail": "Refresh Toekn is Outdated"}
            )

        access_token: AccessToken = AccessToken(user.pk).encode()
        return Response({"access_token": access_token}, status=HTTP_200_OK)

    except User.DoesNotExist:
        return Response(HTTP_400_BAD_REQUEST, {"detail": "Toekn is Invalid"})
