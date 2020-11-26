from django.urls import path
from . import views

urlpatterns = [
    path('customersPresentCarts', views.customersPresentCarts, name="customersPresentCarts"),
    path('restaurantReceiveCarts', views.restaurantReceiveCarts, name="restaurantReceiveCarts"),
    path('restaurantPastReceivedCarts', views.restaurantPastReceivedCarts, name="restaurantPastReceivedCarts"),
    path('restaurantManageCustomers', views.restaurantManageCustomers, name="restaurantManageCustomers"),
    path('restaurantCustomerlist', views.restaurantCustomerlist, name="restaurantCustomerlist"),
    path('customerAddCart', views.customerAddCart, name="customerAddCart"),
    path('requestFail', views.requestFail, name="requestFail"),
    path('requestSuccess', views.requestSuccess, name="requestSuccess"),
    path('customerCancelCart', views.customerCancelCart, name="customerCancelCart"),
    path('customerSendCartToRestaurant', views.customerSendCartToRestaurant, name="customerSendCartToRestaurant"),
    path('restaurantCancelCart', views.restaurantCancelCart, name="restaurantCancelCart"),
    path('restaurantAcceptCart', views.restaurantAcceptCart, name="restaurantAcceptCart"),
]
