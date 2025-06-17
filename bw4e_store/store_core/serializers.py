from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Partner, Product, Redemption

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'website', 'description']

class ProductSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(queryset=Partner.objects.all())
    # For a read-only nested representation of partner, you could use:
    # partner = PartnerSerializer(read_only=True)
    # Or for a writable nested serializer, you'd need to handle create/update methods.

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'product_type', 'partner',
            'image', 'terms_and_conditions', 'redeemable_once',
            'available_from', 'available_to', 'stock'
        ]

class RedemptionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    # To make product name also visible in read operations easily:
    # product_name = serializers.ReadOnlyField(source='product.name')


    class Meta:
        model = Redemption
        fields = [
            'id', 'user', 'product', # 'product_name',
            'redeemed_at', 'notes', 'partner_confirmation_id'
        ]
        read_only_fields = ['redeemed_at', 'partner_confirmation_id'] # user is already ReadOnlyField

    # Additional validation can be added here if needed, e.g.
    # def validate_product(self, value):
    #     # Example: Check if product is active before allowing redemption association
    #     if not value.is_active_for_redemption(): # Assuming such a method exists on Product model
    #         raise serializers.ValidationError("This product cannot be redeemed currently.")
    #     return value
