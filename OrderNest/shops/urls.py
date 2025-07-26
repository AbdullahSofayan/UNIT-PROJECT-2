from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path("browse/shops/", views.browse_shops_view, name='browse_shops_view'),
    path("branches/<shop_id>", views.branches_view, name='branches_view'),
    path("admin/", views.shop_admin_dashboard, name='shop_admin_dashboard'),
    path("admin/<shop_id>/details", views.shop_details_view, name='shop_details_view'),
    path("admin/<shop_id>/update", views.shop_update_view, name='shop_update_view'),
    path('branches/<int:shop_id>/add/', views.add_branch_view, name='add_branch_view'),

]