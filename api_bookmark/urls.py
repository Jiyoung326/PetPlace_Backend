from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookMarkView.as_view()), 
    path('<str:user_id>', views.BookMarkView.as_view())
]