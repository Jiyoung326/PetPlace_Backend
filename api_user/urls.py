from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('<str:u_id>', views.UserView.as_view())
]