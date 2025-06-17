from django.contrib import admin
from .models import Partner, Product, Redemption

# Customize Admin Site Titles
admin.site.site_header = "BW4E Member Store | Admin Panel"
admin.site.site_title = "BW4E Store Admin" # More concise for browser tabs
admin.site.index_title = "Welcome to BW4E Store Administration"

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner', 'product_type', 'stock', 'available_from', 'available_to')
    list_filter = ('product_type', 'partner', 'redeemable_once')
    search_fields = ('name', 'description', 'partner__name')
    autocomplete_fields = ('partner',) # For easier partner selection

@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'redeemed_at')
    list_filter = ('redeemed_at', 'product__partner') # Filter by partner through product
    search_fields = ('user__username', 'product__name')
    autocomplete_fields = ('user', 'product') # For easier user and product selection
    readonly_fields = ('redeemed_at',) # This is set automatically

# If you prefer not to use decorators, you can use admin.site.register:
# admin.site.register(Partner, PartnerAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Redemption, RedemptionAdmin)
