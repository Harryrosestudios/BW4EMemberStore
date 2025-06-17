from django.urls import path
from . import views

app_name = 'store_core' # Optional: for namespacing URLs

urlpatterns = [
    path('home/', views.HomePageView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('redeem/<int:product_id>/', views.RedeemProductView.as_view(), name='redeem_product'),
]
