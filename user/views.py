from django.contrib.auth import authenticate, logout
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'login':
            return [permissions.AllowAny()]
        elif self.action == 'logout':
            return [permissions.IsAuthenticated()]
        else:
            return super().get_permissions()

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
        except (AttributeError, Token.DoesNotExist):
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        Token.objects.filter(user=user).delete()

        token = Token.objects.create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


