from django.urls import path
from . import views

urlpatterns = [
    path('', views.FacilityView.as_view()), #facilities/뒤에 안 붙을 때
    path('<str:category>', views.FacilityView.as_view()) 
]