from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views # Assuming your API views are in api_views.py

app_name = 'store_core'

router = DefaultRouter()
router.register(r'partners', api_views.PartnerViewSet, basename='partner')
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'redemptions', api_views.UserRedemptionViewSet, basename='user-redemption')

urlpatterns = [
    # Previous frontend URL patterns are commented out
    # path('home/', views.HomePageView.as_view(), name='home'),
    # path('products/', views.ProductListView.as_view(), name='product_list'),
    # path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    # path('redeem/<int:product_id>/', views.RedeemProductView.as_view(), name='redeem_product'),

    path('api/', include(router.urls)), # Include DRF's router URLs
]
