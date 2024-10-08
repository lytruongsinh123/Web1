from django.urls import path
from .views import MyModelList

urlpatterns = [
    path('mymodel/', MyModelList.as_view(), name='mymodel-list'),
]
