from django.urls import path
from stripe_app import views


urlpatterns = [
    path('item/<int:id>/', views.item_detail, name='item-detail'),
    path('buy/<int:id>/', views.buy_item, name='buy-item'),
    path('order/<int:id>/', views.order_detail, name='order-detail'),
    path('buy_order/<int:id>/', views.buy_order, name='buy-order'),

    path('', views.home, name='home'),
]