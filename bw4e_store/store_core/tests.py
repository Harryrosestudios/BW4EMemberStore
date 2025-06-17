from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.utils import timezone
from datetime import timedelta

from .models import Partner, Product, Redemption
from .views import HomePageView, ProductListView, ProductDetailView, RedeemProductView

# Helper function to create common objects (optional, but can be useful)
def create_partner(name="Test Partner"):
    return Partner.objects.create(name=name, website="http://testpartner.com")

def create_product(partner, name="Test Product", product_type="discount", stock=10, redeemable_once=False, available_from_delta=0, available_to_delta=7):
    now = timezone.now()
    return Product.objects.create(
        name=name,
        description="A test product description.",
        product_type=product_type,
        partner=partner,
        stock=stock,
        redeemable_once=redeemable_once,
        available_from=now + timedelta(days=available_from_delta),
        available_to=now + timedelta(days=available_to_delta)
    )

def create_user(username="testuser", password="password123"):
    return User.objects.create_user(username=username, password=password)


class ModelTests(TestCase):
    def setUp(self):
        self.partner = create_partner()
        self.user = create_user()
        self.product = create_product(partner=self.partner)

    def test_partner_creation(self):
        self.assertEqual(self.partner.name, "Test Partner")
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(str(self.partner), "Test Partner")

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.partner, self.partner)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(str(self.product), f"Test Product by {self.partner.name}")

    def test_redemption_creation(self):
        redemption = Redemption.objects.create(
            user=self.user,
            product=self.product,
            notes="Test redemption notes."
        )
        self.assertEqual(redemption.user, self.user)
        self.assertEqual(redemption.product, self.product)
        self.assertEqual(redemption.notes, "Test redemption notes.")
        self.assertIsNotNone(redemption.redeemed_at)
        self.assertEqual(Redemption.objects.count(), 1)
        self.assertEqual(str(redemption), f"{self.user.username} redeemed {self.product.name}")

class URLTests(TestCase):
    def setUp(self):
        self.partner = create_partner()
        self.product = create_product(partner=self.partner, pk=1) # Ensure pk for detail view

    def test_home_url_resolves(self):
        url = reverse('store_core:home')
        self.assertEqual(resolve(url).func.view_class, HomePageView)

    def test_product_list_url_resolves(self):
        url = reverse('store_core:product_list')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url_resolves(self):
        url = reverse('store_core:product_detail', kwargs={'pk': self.product.pk})
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_redeem_product_url_resolves(self):
        url = reverse('store_core:redeem_product', kwargs={'product_id': self.product.pk})
        self.assertEqual(resolve(url).func.view_class, RedeemProductView)

# View tests will be added below
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user(username="testuser1", password="password")
        self.partner = create_partner(name="Main Partner")
        self.product1 = create_product(partner=self.partner, name="Product One", stock=10, pk=1)
        self.product2_redeemable_once = create_product(partner=self.partner, name="Redeem Once Product", stock=5, redeemable_once=True, pk=2)
        self.product3_out_of_stock = create_product(partner=self.partner, name="Out of Stock Product", stock=0, pk=3)
        self.product4_expired = create_product(partner=self.partner, name="Expired Product", available_to_delta=-1, pk=4) # Expired yesterday
        self.product5_not_yet_available = create_product(partner=self.partner, name="Future Product", available_from_delta=1, pk=5) # Available tomorrow

    # --- Authentication Tests ---
    def test_home_view_auth_required(self):
        response = self.client.get(reverse('store_core:home'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('store_core:home')}")

        self.client.login(username="testuser1", password="password")
        response = self.client.get(reverse('store_core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_core/home.html')

    def test_product_list_view_auth_required(self):
        response = self.client.get(reverse('store_core:product_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('store_core:product_list')}")

        self.client.login(username="testuser1", password="password")
        response = self.client.get(reverse('store_core:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_core/product_list.html')
        self.assertIn('products', response.context)

    def test_product_detail_view_auth_required(self):
        url = reverse('store_core:product_detail', kwargs={'pk': self.product1.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

        self.client.login(username="testuser1", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_core/product_detail.html')
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product1)

    # --- Redemption Logic Tests ---
    def test_redeem_product_successful(self):
        self.client.login(username="testuser1", password="password")
        initial_stock = self.product1.stock
        redeem_url = reverse('store_core:redeem_product', kwargs={'product_id': self.product1.pk})

        response = self.client.post(redeem_url)

        self.assertEqual(Redemption.objects.count(), 1)
        redemption = Redemption.objects.first()
        self.assertEqual(redemption.user, self.user)
        self.assertEqual(redemption.product, self.product1)

        self.product1.refresh_from_db() # Refresh object from DB
        self.assertEqual(self.product1.stock, initial_stock - 1)

        self.assertRedirects(response, reverse('store_core:product_detail', kwargs={'pk': self.product1.pk}))

        # Check for success message (requires messages middleware and context processor)
        # For this, you often need to follow the redirect and check the new response's context
        response_redirected = self.client.get(response.url)
        messages = list(response_redirected.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Successfully redeemed '{self.product1.name}'.")


    def test_redeem_product_redeemable_once_twice(self):
        self.client.login(username="testuser1", password="password")
        redeem_url = reverse('store_core:redeem_product', kwargs={'product_id': self.product2_redeemable_once.pk})

        # First redemption
        response_first = self.client.post(redeem_url)
        self.assertEqual(Redemption.objects.filter(product=self.product2_redeemable_once).count(), 1)
        self.assertRedirects(response_first, reverse('store_core:product_detail', kwargs={'pk': self.product2_redeemable_once.pk}))

        # Second redemption attempt
        response_second = self.client.post(redeem_url)
        self.assertEqual(Redemption.objects.filter(product=self.product2_redeemable_once).count(), 1) # Still 1
        self.assertRedirects(response_second, reverse('store_core:product_detail', kwargs={'pk': self.product2_redeemable_once.pk}))

        response_redirected = self.client.get(response_second.url)
        messages = list(response_redirected.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have already redeemed this product.")

    def test_redeem_product_out_of_stock(self):
        self.client.login(username="testuser1", password="password")
        redeem_url = reverse('store_core:redeem_product', kwargs={'product_id': self.product3_out_of_stock.pk})

        response = self.client.post(redeem_url)

        self.assertEqual(Redemption.objects.count(), 0) # No redemption created
        self.assertRedirects(response, reverse('store_core:product_detail', kwargs={'pk': self.product3_out_of_stock.pk}))

        response_redirected = self.client.get(response.url)
        messages = list(response_redirected.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This product is out of stock.")

    def test_redeem_product_expired(self):
        self.client.login(username="testuser1", password="password")
        redeem_url = reverse('store_core:redeem_product', kwargs={'product_id': self.product4_expired.pk})

        response = self.client.post(redeem_url)
        self.assertEqual(Redemption.objects.count(), 0)
        self.assertRedirects(response, reverse('store_core:product_detail', kwargs={'pk': self.product4_expired.pk}))

        response_redirected = self.client.get(response.url)
        messages = list(response_redirected.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This product is no longer available.")

    def test_redeem_product_not_yet_available(self):
        self.client.login(username="testuser1", password="password")
        redeem_url = reverse('store_core:redeem_product', kwargs={'product_id': self.product5_not_yet_available.pk})

        response = self.client.post(redeem_url)
        self.assertEqual(Redemption.objects.count(), 0)
        self.assertRedirects(response, reverse('store_core:product_detail', kwargs={'pk': self.product5_not_yet_available.pk}))

        response_redirected = self.client.get(response.url)
        messages = list(response_redirected.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This product is not yet available.")

    def test_redeem_product_get_request_not_allowed(self):
        self.client.login(username="testuser1", password="password")
        redeem_url = reverse('store_core:redeem_product', kwargs={'product_id': self.product1.pk})
        response = self.client.get(redeem_url) # Use GET

        self.assertEqual(Redemption.objects.count(), 0) # No redemption
        self.assertRedirects(response, reverse('store_core:product_detail', kwargs={'pk': self.product1.pk}))

        response_redirected = self.client.get(response.url)
        messages = list(response_redirected.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "To redeem a product, please use the redeem button on its page.")
