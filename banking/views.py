
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import Customer, Account, Transaction, Loan

# Home View
def home(request):
    accounts = Account.objects.all()
    return render(request, 'banking/home.html', {'accounts': accounts})

# Transfer View
def transfer(request):
    if request.method == "POST":
        from_account_number = request.POST.get('from_account_number')
        to_account_number = request.POST.get('to_account_number')
        amount = Decimal(request.POST.get('amount'))

        # Get the accounts by account numbers
        from_account = get_object_or_404(Account, account_number=from_account_number)
        to_account = get_object_or_404(Account, account_number=to_account_number)

        # Check if the from_account has enough balance for the transfer
        if from_account.balance >= amount:
            # Process the transfer
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            # Create transaction records for both accounts
            Transaction.objects.create(
                account=from_account,
                transaction_type='WITHDRAWAL',
                amount=amount,
                description=f"Transfer to account {to_account_number}"
            )
            Transaction.objects.create(
                account=to_account,
                transaction_type='DEPOSIT',
                amount=amount,
                description=f"Transfer from account {from_account_number}"
            )

            messages.success(request, f"Successfully transferred {amount} from account {from_account_number} to account {to_account_number}.")
            return redirect('home')
        else:
            messages.error(request, "Insufficient balance for the transfer.")

    return render(request, 'banking/transfer.html')

# Create Customer View
def create_customer(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        date_of_birth = request.POST['date_of_birth']

        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Please use a different email.")
            return render(request, 'banking/create_customer.html')

        # Create a new customer if email is unique
        try:
            Customer.objects.create(
                name=name, email=email, phone=phone, address=address, date_of_birth=date_of_birth
            )
            messages.success(request, f"Customer {name} created successfully!")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return render(request, 'banking/create_customer.html')

    return render(request, 'banking/create_customer.html')

# Update Customer View
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        customer.name = request.POST['name']
        customer.email = request.POST['email']
        customer.phone = request.POST['phone']
        customer.address = request.POST['address']
        customer.date_of_birth = request.POST['date_of_birth']
        customer.save()
        messages.success(request, f"Customer {customer.name} updated successfully!")
        return redirect('home')
    return render(request, 'banking/update_customer.html', {'customer': customer})

# Delete Customer View
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        customer.delete()
        messages.success(request, f"Customer {customer.name} deleted successfully!")
        return redirect('home')
    return render(request, 'banking/delete_customer.html', {'customer': customer})

# Create Account View
def create_account(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        account_number = request.POST.get('account_number')
        balance = Decimal(request.POST.get('balance'))

        # Ensure that the customer exists
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            messages.error(request, 'Customer does not exist')
            return render(request, 'banking/create_account.html', {'error': 'Customer does not exist'})

        # Create the account
        Account.objects.create(
            customer=customer,
            account_number=account_number,
            balance=balance
        )
        messages.success(request, "Account created successfully!")
        return redirect('home')  # Redirect to home or a success page

    # GET request, pass customers to the template
    customers = Customer.objects.all()
    return render(request, 'banking/create_account.html', {'customers': customers})

# Update Account View
def update_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        account.account_number = request.POST['account_number']
        account.balance = Decimal(request.POST['balance'])
        account.save()
        messages.success(request, f"Account {account.account_number} updated successfully!")
        return redirect('home')
    return render(request, 'banking/update_account.html', {'account': account})

# Delete Account View
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        account.delete()
        messages.success(request, f"Account {account.account_number} deleted successfully!")
        return redirect('home')
    return render(request, 'banking/delete_account.html', {'account': account})

# Create Loan View
def apply_loan(request):
    customers = Customer.objects.all()
    if request.method == "POST":
        customer_id = request.POST['customer_id']
        try:
            loan_amount = Decimal(request.POST['loan_amount'])
            interest_rate = Decimal(request.POST['interest_rate'])
            duration_months = int(request.POST['duration_months'])

            if loan_amount <= 0 or interest_rate <= 0 or duration_months <= 0:
                messages.error(request, "Loan amount, interest rate, and duration must be positive values.")
                return redirect('home')

            customer = get_object_or_404(Customer, id=customer_id)
            Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                duration_months=duration_months
            )
            messages.success(request, f"Loan of {loan_amount} applied successfully for {customer.name}!")
        except ValueError:
            messages.error(request, "Invalid loan details entered!")
        return redirect('home')

    return render(request, 'banking/apply_loan.html', {'customers': customers})

# Update Loan View
def update_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == "POST":
        loan.loan_amount = Decimal(request.POST['loan_amount'])
        loan.interest_rate = Decimal(request.POST['interest_rate'])
        loan.duration_months = int(request.POST['duration_months'])
        loan.save()
        messages.success(request, f"Loan updated successfully!")
        return redirect('home')
    return render(request, 'banking/update_loan.html', {'loan': loan})

# Delete Loan View
def delete_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == "POST":
        loan.delete()
        messages.success(request, f"Loan deleted successfully!")
        return redirect('home')
    return render(request, 'banking/delete_loan.html', {'loan': loan})

# Deposit View
def deposit(request):
    if request.method == "POST":
        account_number = request.POST.get("account_number")
        amount = Decimal(request.POST.get("amount"))

        # Find the account by account number
        account = get_object_or_404(Account, account_number=account_number)

        # Process the deposit
        account.balance += amount
        account.save()

        # Create a transaction record for the deposit
        Transaction.objects.create(
            account=account,
            transaction_type='DEPOSIT',
            amount=amount,
            description=f"Deposit of {amount}",
        )

        messages.success(request, f"Successfully deposited {amount} to account {account_number}.")
        return redirect('home')

    return render(request, "banking/deposit.html")

# Withdraw View
def withdraw(request):
    if request.method == "POST":
        account_number = request.POST.get("account_number")
        amount = Decimal(request.POST.get("amount"))

        # Find the account by account number
        account = get_object_or_404(Account, account_number=account_number)

        # Check if the account has enough balance
        if account.balance >= amount:
            # Process the withdrawal
            account.balance -= amount
            account.save()

            # Create a transaction record for the withdrawal
            Transaction.objects.create(
                account=account,
                transaction_type='WITHDRAWAL',
                amount=amount,
                description=f"Withdrawal of {amount}",
            )

            messages.success(request, f"Successfully withdrew {amount} from account {account_number}.")
            return redirect('home')
        else:
            messages.error(request, "Insufficient balance for the withdrawal.")

    return render(request, "banking/withdraw.html")

# Report View
def report(request):
    accounts = Account.objects.all()
    transactions = Transaction.objects.all()
    loans = Loan.objects.all()
    return render(request, 'banking/report.html', {
        'accounts': accounts,
        'transactions': transactions,
        'loans': loans
    })
''''  
from django.shortcuts import render

'''
    
def search_account(request):
    name = request.GET.get('name', '').strip()  # Get the name parameter
    print(f"Searching for accounts with name: {name}")  # Debugging log

    accounts = Account.objects.filter(customer__name__icontains=name)
    print(f"Accounts found: {accounts}")  # Debugging log

    return render(request, 'banking/search_results.html', {
        'query': name,
        'accounts': accounts,
    })

