from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('decypher/', views.decypher, name='decypher'),
    path('', views.index, name='index'),
]