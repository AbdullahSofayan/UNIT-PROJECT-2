from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.hashers import check_password
from .models import Customer
from .forms import LoginForm, SignUpForm

def login_view(request: HttpRequest):
    error_message = None

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                customer = Customer.objects.get(username=username)
                if check_password(password, customer.password):
                    request.session['customer_id'] = customer.id
                    return redirect('accounts:customer_home_view')
                else:
                    error_message = "Incorrect password."
            except Customer.DoesNotExist:
                error_message = "Username does not exist."
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error_message": error_message})



def sign_up_view(request: HttpRequest):
    error_message = None

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            if Customer.objects.filter(username=username).exists() or Customer.objects.filter(email=email).exists():
                error_message = "Username or Email is already exists."

            else:
                Customer.objects.create(
                    username=username,
                    password=password,
                    full_name=full_name,
                    email=email,
                    role = 'Customer',
                    phone = phone,
                    address = address
                )
                return redirect("main:home_view")
    else:
        form = SignUpForm()

    return render(request, "sign_up.html", {"form": form, "error_message": error_message})


def customer_home_view(request: HttpRequest):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('accounts:login_view') 

    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return redirect('accounts:login_view')

    return render(request, "customer_home.html", {'customer': customer})

