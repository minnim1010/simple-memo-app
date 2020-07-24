from django.urls import path

from memo import views

urlpatterns = [
    path('', views.ListMemo.as_view()),
    path('<int:pk>/', views.DetailMemo.as_view()),
]