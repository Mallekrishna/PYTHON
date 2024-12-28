from django.contrib import admin
from .models import Customer, Account, Transaction,Loan

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)

admin.site.site_header = "Core Banking Admin"
admin.site.site_title = "Core Banking Portal"
admin.site.index_title = "Welcome to Core Banking Administration"

