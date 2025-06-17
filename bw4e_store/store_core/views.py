from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils import timezone
from django.db import transaction # For atomic operations
from .models import Product, Redemption

# @method_decorator(login_required, name='dispatch')
# class HomePageView(TemplateView):
#     template_name = "store_core/home.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         return context

# @method_decorator(login_required, name='dispatch')
# class ProductListView(ListView):
#     model = Product
#     template_name = "store_core/product_list.html"
#     context_object_name = "products"

#     def get_queryset(self):
#         # Optionally filter products, e.g., only show available ones
#         # return Product.objects.filter(available_from__lte=timezone.now(), available_to__gte=timezone.now())
#         return Product.objects.all() # For now, show all

# @method_decorator(login_required, name='dispatch')
# class ProductDetailView(DetailView):
#     model = Product
#     template_name = "store_core/product_detail.html"
#     context_object_name = "product"

# @method_decorator(login_required, name='dispatch')
# class RedeemProductView(View):
#     def post(self, request, *args, **kwargs):
#         product_id = kwargs.get('product_id')
#         product = get_object_or_404(Product, pk=product_id)
#         user = request.user

#         try:
#             with transaction.atomic(): # Ensure atomicity
#                 # 1. Check if redeemable once and already redeemed
#                 if product.redeemable_once:
#                     if Redemption.objects.filter(user=user, product=product).exists():
#                         messages.error(request, "You have already redeemed this product.")
#                         return redirect('store_core:product_detail', pk=product.pk)

#                 # 2. Check stock
#                 if product.stock is not None and product.stock <= 0:
#                     messages.error(request, "This product is out of stock.")
#                     return redirect('store_core:product_detail', pk=product.pk)

#                 # 3. Check availability window
#                 now = timezone.now()
#                 if product.available_from and now < product.available_from:
#                     messages.error(request, "This product is not yet available.")
#                     return redirect('store_core:product_detail', pk=product.pk)
#                 if product.available_to and now > product.available_to:
#                     messages.error(request, "This product is no longer available.")
#                     return redirect('store_core:product_detail', pk=product.pk)

#                 # TODO: Partner Integration Point
#                 # This is where you might call out to a partner's API.
#                 # The exact logic will depend on the partner and product_type.
#                 # For now, this is a placeholder.
#                 partner_confirmation_code_from_api = None # Example variable

#                 # If product.product_type == 'promotion':
#                 #   # response = requests.post(partner_api_url, data={'product_id': product.id, 'user_id': user.id})
#                 #   # if response.status_code == 200 and response.json().get('valid'):
#                 #   #    partner_confirmation_code_from_api = response.json().get('confirmation_id')
#                 #   # else:
#                 #   #    messages.error(request, "Failed to validate promotion with partner.")
#                 #   #    return redirect('store_core:product_detail', pk=product.pk)
#                 #   pass
#                 # Elif product.product_type == 'service':
#                 #   # response = requests.post(partner_service_url, data={'service_id': product.id, 'action': 'provision'})
#                 #   # if response.status_code == 200 and response.json().get('activated'):
#                 #   #    partner_confirmation_code_from_api = response.json().get('service_ticket_id')
#                 #   # else:
#                 #   #    messages.error(request, "Failed to provision service with partner.")
#                 #   #    return redirect('store_core:product_detail', pk=product.pk)
#                 #   pass

#                 # All checks passed, create redemption
#                 # Pass partner_confirmation_id if obtained
#                 Redemption.objects.create(
#                     user=user,
#                     product=product,
#                     partner_confirmation_id=partner_confirmation_code_from_api # Store it
#                 )

#                 # Decrement stock if applicable
#                 if product.stock is not None:
#                     product.stock -= 1
#                     product.save()

#                 messages.success(request, f"Successfully redeemed '{product.name}'.")

#         except Exception as e: # Catch any other db error during transaction
#             messages.error(request, f"An error occurred during redemption: {str(e)}")

#         return redirect('store_core:product_detail', pk=product.pk)

#     def get(self, request, *args, **kwargs):
#         # GET requests are not allowed for redemption, redirect to product detail
#         product_id = kwargs.get('product_id')
#         product = get_object_or_404(Product, pk=product_id)
#         messages.info(request, "To redeem a product, please use the redeem button on its page.")
#         return redirect('store_core:product_detail', pk=product.pk)
