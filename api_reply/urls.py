from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReplyView.as_view()),
    path('<int:b_id>', views.ReplyView.as_view())
]