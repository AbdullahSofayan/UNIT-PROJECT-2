from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path("<shop_id>/menu/", views.menu_view, name="menu_view"),
    path('shop/<int:shop_id>/manage-menu/', views.manage_menu_view, name='manage_menu'),
    path('shop/<int:shop_id>/add-item/<int:category_id>/', views.add_menu_item_view, name='add_menu_item'),
    path('shop/<int:shop_id>/add-category/', views.add_category_view, name='add_category'),
     path('shop/<int:shop_id>/delete-item/<int:item_id>/', views.delete_menu_item_view, name='delete_menu_item'),
     path('shop/<int:shop_id>/delete-category/<int:category_id>/', views.delete_menu_category_view, name='delete_menu_category_view'),
     path('shop/<int:shop_id>/update-item/<int:item_id>/', views.update_menu_item_view, name='update_menu_item_view'),
     path('<int:shop_id>/category/<int:category_id>/edit/', views.update_menu_category_view, name='update_menu_category_view'),





]