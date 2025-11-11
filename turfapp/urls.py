from django.urls import path
from  . import views


urlpatterns=[
    path('login/', views.show_login_page, name="login"),
    path('signup/', views.show_signup_page,name="signup"),
    path('', views.show_home_page,name="home")
]

