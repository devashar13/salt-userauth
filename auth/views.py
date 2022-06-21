from yaml import serialize
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework import response
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from .serializes import UserRegistrationSerializer
class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response_data = {
                'success': 'True',
                'status_code': status_code,
                'message': 'User created successfully',
            }
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {
                'success': 'False',
                'status_code': status_code,
                'message': serializer.errors,
            }
class UserLoginView(CreateAPIView):
    pass

