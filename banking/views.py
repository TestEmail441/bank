from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, OTP
from .forms import CustomSignUpForm, PinForm
from django.contrib.auth import login, authenticate, logout
import random
import string
import requests
from decimal import Decimal, InvalidOperation
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail


def generate_unique_account_number():
    while True:
        account_number = ''.join(random.choices(string.digits, k=10))
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number


@login_required
def dashboard(request):
    account, created = Account.objects.get_or_create(
        user=request.user,
        defaults={
            # Ensure this field exists in the model
            'account_number': generate_unique_account_number(),
            'balance': 0.00  # or any other default values required
        }
    )
    transactions = Transaction.objects.filter(
        account=account).order_by('-date')[:5]
    return render(request, 'dashboard.html', {'account': account, 'transactions': transactions})


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def transfer_funds(request):
    try:
        sender_account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return redirect('dashboard')

    if request.method == 'POST':
        if 'otp' in request.POST:
            entered_otp = request.POST.get('otp')
            reference_id = request.POST.get('reference_id')

            try:
                otp_instance = OTP.objects.get(
                    user=request.user, otp=entered_otp, is_verified=False)
            except OTP.DoesNotExist:
                return render(request, 'verify_otp.html', {
                    'error': 'Invalid OTP. Please try again.',
                    'reference_id': reference_id
                })

            otp_instance.is_verified = True
            otp_instance.save()

            return redirect('transfer_success')

        else:
            pin = request.POST.get('pin')
            if pin != sender_account.pin:
                return render(request, 'transfer_funds.html', {
                    'error': 'Invalid PIN. Please try again.',
                    'balance': sender_account.balance
                })

            amount = request.POST.get('amount')
            receiver_bank = request.POST.get('receiver_bank')
            receiver_account = request.POST.get('receiver_account')
            receiver_name = request.POST.get('receiver_name')

            if not amount:
                return render(request, 'transfer_funds.html', {
                    'error': 'Amount is required.',
                    'balance': sender_account.balance
                })

            try:
                amount = Decimal(amount)
            except (ValueError, InvalidOperation):
                return render(request, 'transfer_funds.html', {
                    'error': 'Invalid amount entered.',
                    'balance': sender_account.balance
                })

            if sender_account.balance < amount:
                return render(request, 'transfer_funds.html', {
                    'error': 'Insufficient balance',
                    'balance': sender_account.balance
                })

            sender_account.balance -= amount
            sender_account.save()

            Transaction.objects.create(
                account=sender_account,
                amount=-amount,
                transaction_type='withdrawal',
                description=f'Transfer to {receiver_name} at {receiver_bank}'
            )

            otp_instance = OTP.objects.create(user=request.user)
            otp = otp_instance.generate_otp()

            # Send OTP via email
            subject = 'OTP Verification for fund transfer'
            message = f'Your OTP for transferring funds is {otp}.'
            html_message = f"""
                <html>
                  <body style="text-align: center;">
                    <p style= font-size: 24px;">Your OTP for transferring funds is:</p>
                    <h2 style="color:#8b6eca ; font-size: 48px;">{otp}</h2>
                    <p>Please do not share this OTP with anyone.</p>
                  </body>
                </html>
            """

            send_mail(
                subject,
                message,
                'your-email@gmail.com',  # Sender's email
                [request.user.email],  # Recipient's email
                fail_silently=False,
                html_message=html_message
            )

            reference_id = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=15))
            return render(request, 'verify_otp.html', {'reference_id': reference_id})

    return render(request, 'transfer_funds.html', {'balance': sender_account.balance})


@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'transaction_history.html', {'transactions': transactions})


@login_required
def customer_support(request):
    return render(request, 'customer_support.html', {
        'support_email': 'suntrustsupporrrt@gmail.com',
        'support_phone': '+1234567890',
        'support_hours': 'Mon-Fri 9am-6pm'
    })


@login_required
def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')  # Redirect to login page or any other page
    else:
        return redirect('home')


@login_required
def set_pin(request):
    # Ensure the account exists or create it
    account, created = Account.objects.get_or_create(
        user=request.user,
        defaults={'account_number': generate_unique_account_number(),
                  'balance': 0.00}
    )

    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data.get('pin')
            confirm_pin = form.cleaned_data.get('confirm_pin')

            if pin == confirm_pin:
                account.pin = pin
                account.save()
                # Redirect to dashboard after setting PIN
                return redirect('dashboard')
            else:
                return render(request, 'set_pin.html', {'form': form, 'error': 'PINs do not match'})

    else:
        form = PinForm()

    return render(request, 'set_pin.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('set_pin')
        else:
            # Add this to show form errors if form is invalid
            return render(request, 'signup.html', {'form': form, 'error': form.errors})
    else:
        form = CustomSignUpForm()

    return render(request, 'signup.html', {'form': form})


def transfer_success_view(request):
    return render(request, 'transfer_success.html')
