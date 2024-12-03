from django.urls import path
from rest_framework import routers

from . import views

app_name = "news"

router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('login/', views.login_user, name="login"),
    path('news/', views.news, name="news")
]
