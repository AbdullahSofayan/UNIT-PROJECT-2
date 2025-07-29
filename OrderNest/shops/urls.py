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
    path("shop/<int:branch_id>/branch/<int:shop_id>/delete/", views.delete_branch_view, name="delete_branch_view"),
    path('edit/<int:branch_id>/<int:shop_id>/', views.edit_branch_view, name='edit_branch_view'),
    path('manage/<int:shop_id>', views.manage_orders_view, name='manage_orders'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_status'),



]