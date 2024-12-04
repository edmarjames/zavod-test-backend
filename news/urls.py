from django.urls import path
from rest_framework import routers

from . import views

app_name = "news"

router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('login/', views.login_user, name="login"),
    path('news/', views.news, name="news"),
    path('news/<int:pk>', views.news_by_id, name="news_by_id"),
    path('news/statistics', views.news_statistics, name="news_statistics"),
]
