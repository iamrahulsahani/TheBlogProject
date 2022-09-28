from home import views
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', views.PeopleViewSets, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('index/user/<int:usr>', views.index),
    path('person/', views.people),
    path('register/', views.RegisterAPI.as_view()),
    path('login/', views.LoginAPI.as_view())




]