from django.urls import path
from . import views

urlpatterns = [
    path('', views.PhotoView.as_view()),
    path('<int:b_id>', views.PhotoView.as_view())
]