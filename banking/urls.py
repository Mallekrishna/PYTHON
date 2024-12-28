from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # The home page URL
    path('customer/create/', views.create_customer, name='create_customer'),
    path('customer/update/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('customer/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('account/create/', views.create_account, name='create_account'),
    path('account/update/<int:account_id>/', views.update_account, name='update_account'),
    path('account/delete/<int:account_id>/', views.delete_account, name='delete_account'),
    path('loan/apply/', views.apply_loan, name='apply_loan'),
    path('loan/update/<int:loan_id>/', views.update_loan, name='update_loan'),
    path('loan/delete/<int:loan_id>/', views.delete_loan, name='delete_loan'),
    path('deposit/', views.deposit, name='deposit'),
    path('report/', views.report, name='report'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    

]
