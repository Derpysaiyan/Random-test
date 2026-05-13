from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path("availability/", views.add_availability, name="availability"),
    path("logout/", views.logout_view, name="logout"),
    path("runs/", views.runs, name="runs" )
]