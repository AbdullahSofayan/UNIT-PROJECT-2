from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path("browse/shops/", views.browse_shops_view, name='browse_shops_view'),
    path("branches/<shop_id>", views.branches_view, name='branches_view'),
]