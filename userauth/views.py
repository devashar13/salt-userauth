
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from .serializes import UserRegistrationSerializer
class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response_data = {
                'success': 'True',
                'message': 'User created successfully',
            }
            return Response(response_data, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {
                'success': 'False',
                'message': serializer.errors,
            }
            return Response(response_data, status=status_code)
class UserLoginView(CreateAPIView):
    pass

