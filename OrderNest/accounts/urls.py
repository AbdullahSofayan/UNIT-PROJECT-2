from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/",views.login_view, name="login_view"),
    path("signup/",views.sign_up_view, name="sign_up_view"),
    path("home/", views.customer_home_view, name="customer_home_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("profile/", views.profile_view, name="profile_view"),
    path("profile/update/", views.update_profile_view, name="update_profile_view"),
    path("reset-password/", views.reset_password_view, name="reset_password_view"),



]