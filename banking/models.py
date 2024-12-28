from django.db import models

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()  

    def __str__(self):
        return self.name

# Account Model
class Account(models.Model):
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Account {self.account_number} - {self.customer.name}"

    def deposit(self, amount):
        """Function to handle deposit to the account"""
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Function to handle withdrawal from the account"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient balance")

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.timestamp})"

# Loan Model
class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()

    def __str__(self):
        return f"Loan for {self.customer.name} - {self.loan_amount} at {self.interest_rate}% for {self.duration_months} months"

    def calculate_monthly_payment(self):
        """Calculates the monthly payment for the loan based on the loan amount, interest rate, and duration"""
        interest_rate_decimal = self.interest_rate / 100
        monthly_rate = interest_rate_decimal / 12
        number_of_months = self.duration_months
        monthly_payment = self.loan_amount * (monthly_rate * (1 + monthly_rate) ** number_of_months) / ((1 + monthly_rate) ** number_of_months - 1)
        return monthly_payment

    def total_repayment(self):
        """Calculates the total repayment for the loan, including interest"""
        monthly_payment = self.calculate_monthly_payment()
        return monthly_payment * self.duration_months
