from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/",views.login_view, name="login_view"),
    path("signup/",views.sign_up_view, name="sign_up_view"),
    path("home/", views.customer_home_view, name="customer_home_view")


]