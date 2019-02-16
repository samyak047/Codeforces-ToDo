from django.urls import path
from . import views

urlpatterns = [

	path('', views.home, name = 'home'),
	path('todo/', views.index, name = 'index'),
	path('accounts/register/', views.register, name = 'register'),

]