import jwt
import os

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional
from abc import ABCMeta

from django.utils import timezone

TOKEN_ENCODE_ALGORITHM = os.environ.get("TOKEN_ENCODE_ALGORITHM")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


@dataclass
class Token(metaclass=ABCMeta):

    pk: int
    token_type: Optional[int]
    expirate_date: Optional[int]

    def _searialize(self) -> Dict:
        data = {
            "token_type": self.token_type,
            "pk": self.pk,
            "expirate_date": self.expirate_date.strftime("%Y/%m/%d %H:%M:%S"),
        }
        return data

    def encode(self):
        serialzed_data = self._searialize()
        return jwt.encode(serialzed_data, SECRET_KEY, algorithm=TOKEN_ENCODE_ALGORITHM)

    @classmethod
    def decode(self, token: str):
        data: Dict = jwt.decode(token, SECRET_KEY, algorithms=TOKEN_ENCODE_ALGORITHM)
        try:
            token_type: str = data.get("token_type")
            # pk: int = data.get("pk")
            exp_date: str = data.get("expirate_date")
            data["expirate_date"] = datetime.strptime(exp_date, "%Y/%m/%d %H:%M:%S")

            for subclass in Token.__subclasses__():
                if subclass.token_type == token_type:
                    return subclass(**data)

        except ValueError:
            raise Exception

    def is_validate(self) -> bool:
        if timezone.now() < self.expirate_date:
            return True
        return False


@dataclass
class RefreshToken(Token):

    token_type: str = "refresh"
    expirate_date: datetime = timezone.now() + timedelta(weeks=2)


@dataclass
class AccessToken(Token):

    token_type: str = "access"
    expirate_date: datetime = timezone.now() + timedelta(hours=30)
