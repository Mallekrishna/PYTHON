from django.test import TestCase
from django.urls import reverse
from .models import Account, Customer, Transaction, Loan



class HomeViewTest(TestCase):
    def setUp(self):
        # Create some test accounts
        Account.objects.create(account_number="12345", balance=1000)
        Account.objects.create(account_number="67890", balance=2000)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "12345")
        self.assertContains(response, "67890")
