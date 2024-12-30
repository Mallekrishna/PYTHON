from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from banking.models import Customer, Account, Transaction, Loan
from django.contrib.messages import get_messages

class BankingViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user (admin or regular user for authentication)
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a test customer
        self.customer = Customer.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Main St',
            date_of_birth='1990-01-01'
        )

        # Create a test account for the customer
        self.account = Account.objects.create(
            customer=self.customer,
            account_number='1234567890',
            balance=Decimal('1000.00')
        )

        # Log in with the test user
        self.client.login(username='testuser', password='password')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/home.html')
        self.assertContains(response, self.account.account_number)

    