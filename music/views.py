from django.shortcuts import render


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.views import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from .decorators import validate_request_data
from .models import Song
from .serializers import SongsSerializer, TokenSerializer, UserSerializer   

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ListCreateSongsView(ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Song.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @validate_request_data
    def post(self, request, *args, **kwargs):
        song = Song.objects.create(
            title=request.data["title"],
            artist=request.data['artist']
        )
        return Response(
            data=SongsSerializer(song).data,
            status=status.HTTP_201_CREATED
        )

class SongsDetailView(RetrieveUpdateDestroyAPIView):
    """
        GET songs/:id
        DELET songs/:id
        PUT songs/:id

    """
    queryset = Song.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            
            return Response(SongsSerializer(song).data)
        except Song.DoesNotExist:
            return Response(
                data={
                    "message": f"Song with id of {kwargs['pk']} does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def post(self, request, *args, **kwargs):
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            serializer = SongsSerializer()
            updated_song = serializer.update(song,request.data)
            return Response(SongsSerializer(updated_song).data)
        except Song.DoesNotExist:
            return Response(
                data={
                    "message": f"Song with id of {kwargs['pk']} does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, *args, **kwargs):
        
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            return Response(
                data={
                    "message": f"Song with id of {kwargs['pk']} does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )

class LoginView(CreateAPIView):
    """
        POST auth/login
    """
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username","")
        password = request.data.get("password","")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            serializer = TokenSerializer(
                data={
                    "token": jwt_encode_handler(
                        jwt_payload_handler(user)
                    )
                }
            )
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(CreateAPIView):
    """
        POST auth/register
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username","")
        password = request.data.get("password","")
        email = request.data.get("email","")

        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def complete_view(request):
    return Response("Email account is activated")