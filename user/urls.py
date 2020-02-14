from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path,include
from . import views
import user.views

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/',views.about,name='about'),
    path('edit/',views.edit_profile, name='edit'),

    path('public_profile/',views.public_profile, name='public_profile'),

]