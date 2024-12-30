from django.contrib import admin
from .models import Customer, Account, Transaction,Loan


class AccountAdmin(admin.ModelAdmin):
    
    list_display = ('account_number', 'balance', 'customer')
    search_fields = ('account_number', 'customer_name')
    list_filter = ('balance', 'customer')
    ordering = ('-balance',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', ' email', 'phone', 'address', 'date_of_birth')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('birth_date')
    ordering = ('name',)
    
    



admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)

admin.site.site_header = "Core Banking Admin"
admin.site.site_title = "Core Banking Portal"
admin.site.index_title = "Welcome to Core Banking Administration"

