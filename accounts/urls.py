from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # path('', views.my_account, name='initial_getMyPanel'),
    path('register-user/', views.signup, name="registerUser"),
    # login existing user
    path('login/', views.signin, name="existing_user"),
    # logout
    path('logout/', views.signout, name="logout_user"),
    # authenticated user can redirect to own home page
    path('authenticated/dashboard/', views.dashboard, name="my_dashboard"),
]
