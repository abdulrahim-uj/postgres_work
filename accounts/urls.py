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

    # activate user account
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),

    # user profile
    path('authenticated/dashboard/profile/', views.profile, name="my_profile"),
]
