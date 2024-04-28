from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserDetailSerializer, UserRegistrationSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        # Utiliser différents serializers en fonction de l'action CRUD
        if self.action == "create" or self.action == "update":
            return UserRegistrationSerializer
        else:
            return UserDetailSerializer
