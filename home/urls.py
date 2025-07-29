from django.urls import path
from . import views


# URLConf    
urlpatterns = [
    path ("", views.home_start, name="home_start"),
]