import jwt

from rest_framework import authentication
from rest_framework import exceptions

from users.models import User
from users.tokens import Token, AccessToken


class JWTAuthentication(authentication.BaseAuthentication):
    def _check_token_type(self, token):
        if not isinstance(token, AccessToken):
            raise exceptions.AuthenticationFailed(detail="Token Type is invalid")
        return True

    def _check_token_validate(self, token):
        if not token.is_validate():
            raise exceptions.AuthenticationFailed(detail="Token is Outdated")
        return True

    def _check_token(self, token):
        return self._check_token_type and self._check_token_validate

    def authenticate(self, request):
        try:
            token: str = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            xjwt, token = token.split(" ")
            access_token: AccessToken = Token.decode(token)
            if self._check_token(access_token):
                user = User.objects.get(pk=access_token.pk)
                return user, None
        except ValueError:
            return None
        except User.DoesNotExist:
            return None
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")
