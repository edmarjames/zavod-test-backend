from django.contrib.auth import authenticate
from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import News, NewsView, Tag
from .serializers import NewsSerializer, NewsStatisticsSerializer


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
                "error": serializer.errors
            }, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "GET":
        all_news = News.objects.all()
        serializer = NewsSerializer(all_news, many=True)

        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)


@api_view(["GET", "DELETE", "PATCH"])
def news_by_id(request, pk):

    try:
        news = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return Response({
            "message": "Something went wrong",
            "error": "News does not exist",
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = NewsSerializer(news)

        if news:
            NewsView.objects.create(news=news)

        return Response({
            "message": "Data successfully retrieved",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    elif request.method == "DELETE":
        news.delete()

        return Response({
            "message": "News deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PATCH":
        action = request.query_params.get("action")

        if action == "like":
            news.likes += 1
            news.save()

            return Response({
                "message": "News liked successfully",
                "data": NewsSerializer(news).data
            }, status=status.HTTP_200_OK)

        elif action == "dislike":
            news.dislikes += 1
            news.save()
            return Response({
                "message": "News disliked successfully",
                "data": NewsSerializer(news).data
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "message": "Invalid action, please use 'like' or 'dislike'",
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def news_statistics(request):

    all_news_count = News.objects.aggregate(total_count=Count("id"))
    serializer = NewsStatisticsSerializer(all_news_count)

    news_items = News.objects.annotate(views_count=Count("views"))
    news_serializer = NewsSerializer(news_items, many=True)

    tag_stats = (
        Tag.objects.annotate(news_count=Count("news")).values("name", "news_count")
    )
    tag_stats_result = {tag["name"]: tag["news_count"] for tag in tag_stats}

    return Response({
        "message": "Data successfully retrieved",
        "total_count": serializer.data,
        "news_per_tag": tag_stats_result,
        "news_stats": news_serializer.data
    }, status=status.HTTP_200_OK)
