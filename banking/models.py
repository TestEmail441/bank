from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=4)
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"



def generate_unique_reference_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)  # 'deposit' or 'withdrawal'
    reference_id = models.CharField(max_length=15, default=generate_unique_reference_id)  # Unique reference ID
    description = models.TextField(default="No description provided")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set timestamp on creation

    def generate_otp(self):
        otp = ''.join(random.choices(string.digits, k=6))
        self.otp = otp
        self.save()
        return otp
