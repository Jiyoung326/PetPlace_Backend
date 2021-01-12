from django.urls import path
from . import views

urlpatterns = [
    path('', views.LikeView.as_view()),
    path('<int:b_id>', views.LikeView.as_view())
]