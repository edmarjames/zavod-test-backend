from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    NewsSerializer,
    NewsViewSerializer
)


# Create your views here.
@api_view(["POST"])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_superuser:
            return Response({
                "message": "Login successful",
                "is_admin": True,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Login failed",
                "is_admin": False
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({
            "error": "Invalid username or password"
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST", "GET"])
def news(request):

    if request.method == "POST":
        serializer = NewsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "News created successfully",
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Something went wrong",
                "error": serializer.errors,
                "status": status.HTTP_204_NO_CONTENT
            })

