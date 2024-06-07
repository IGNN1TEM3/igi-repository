from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('search/<int:pk>/', views.SearchDetailView.as_view(), name='search_detail'),
    path('profile/', views.profile_view, name='profile')
]
