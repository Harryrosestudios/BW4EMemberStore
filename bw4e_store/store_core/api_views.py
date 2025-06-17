from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response

from .models import Partner, Product, Redemption
from .serializers import PartnerSerializer, ProductSerializer, RedemptionSerializer

class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows partners to be viewed.
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Handled by global settings

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Handled by global settings

    def get_queryset(self):
        """
        Optionally filter products, e.g., only show currently available ones.
        For now, shows all products.
        """
        # Example: Filter for active products
        # now = timezone.now()
        # return Product.objects.filter(
        #     available_from__lte=now,
        #     available_to__gte=now
        # ).select_related('partner')
        return Product.objects.all().select_related('partner')


class UserRedemptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view their redemptions and create new ones.
    """
    serializer_class = RedemptionSerializer
    permission_classes = [permissions.IsAuthenticated] # Overrides global to ensure only authenticated users
    http_method_names = ['get', 'post', 'head', 'options'] # Disallow PUT/PATCH/DELETE for redemptions

    def get_queryset(self):
        """
        This view should return a list of all the redemptions
        for the currently authenticated user.
        """
        return Redemption.objects.filter(user=self.request.user).select_related('product', 'product__partner').order_by('-redeemed_at')

    def perform_create(self, serializer):
        """
        Handles the creation of a new redemption.
        Includes eligibility checks for the product.
        """
        product_instance = serializer.validated_data['product'] # Get Product instance from validated data

        # --- Start of Eligibility Checks (similar to old RedeemProductView) ---
        try:
            with transaction.atomic():
                # Fetch the product again with select_for_update to lock the row if stock is involved
                product_to_redeem = Product.objects.select_for_update().get(pk=product_instance.pk)

                # 1. Check if redeemable once and already redeemed by this user
                if product_to_redeem.redeemable_once:
                    if Redemption.objects.filter(user=self.request.user, product=product_to_redeem).exists():
                        raise serializers.ValidationError("You have already redeemed this product.")

                # 2. Check stock
                if product_to_redeem.stock is not None:
                    if product_to_redeem.stock <= 0:
                        raise serializers.ValidationError("This product is out of stock.")

                # 3. Check availability window
                now = timezone.now()
                if product_to_redeem.available_from and now < product_to_redeem.available_from:
                    raise serializers.ValidationError("This product is not yet available for redemption.")
                if product_to_redeem.available_to and now > product_to_redeem.available_to:
                    raise serializers.ValidationError("This product is no longer available for redemption.")

                # TODO: Partner Integration Point (Placeholder)
                # partner_confirmation_code_from_api = None
                # if product_to_redeem.product_type == 'promotion':
                #     # Call partner API, potentially get partner_confirmation_code_from_api
                #     # If error: raise serializers.ValidationError("Failed with partner system: [reason]")
                #     pass
                # elif product_to_redeem.product_type == 'service':
                #     # Call partner API
                #     pass

                # All checks passed, save the redemption
                # The user is automatically set by serializer.save() due to perform_create context
                # partner_confirmation_id would be passed if available from API call
                redemption = serializer.save(user=self.request.user) #, partner_confirmation_id=partner_confirmation_code_from_api)

                # Decrement stock if applicable
                if product_to_redeem.stock is not None:
                    product_to_redeem.stock -= 1
                    product_to_redeem.save(update_fields=['stock'])

                # No need to explicitly call messages.success for APIs,
                # a 201 Created status is success. Additional data can be in response.

        except Product.DoesNotExist: # Should be caught by serializer if PrimaryKeyRelatedField is used correctly
             raise serializers.ValidationError("Invalid product specified.")
        # Note: The serializers.ValidationError raised will result in a 400 Bad Request response.
        # Other unexpected errors will result in a 500 Internal Server Error.

    # To pass product_id directly in POST body instead of product instance URI:
    # You might need to customize the create method or use a different serializer field for product_id
    # and then fetch the product instance within perform_create or create.
    # For example, if 'product' field in serializer was just an IntegerField for product_id:
    # product_id = serializer.validated_data['product_id']
    # product_instance = get_object_or_404(Product, pk=product_id)
    # Then proceed with checks and serializer.save(user=self.request.user, product=product_instance)
    # However, PrimaryKeyRelatedField is standard DRF practice for foreign keys.
    # The client would POST: {"product": <product_pk>, "notes": "some notes"}
    # And DRF handles resolving <product_pk> to a Product instance for validated_data.
