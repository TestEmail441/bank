from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', views.custom_logout,
         name='logout'),
    path('signup/', views.signup, name='signup'),
    path('transfer_funds/', views.transfer_funds, name='transfer_funds'),
    path('customer_support/', views.customer_support, name='customer_support'),
    path('transaction-history/', views.transaction_history,
         name='transaction_history'),
    path('home/', views.home, name='home'),
    path('set_pin/', views.set_pin, name='set_pin'),
    path('transfer-success/', views.transfer_success_view, name='transfer_success'),
]
