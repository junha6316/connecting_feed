from rest_framework.serializers import ModelSerializer

from .models import User


class RelatedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "sex",
        ]
