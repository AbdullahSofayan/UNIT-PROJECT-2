from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password, make_password
from .models import User
from .forms import LoginForm, SignUpForm, UpdateProfileForm
from django.shortcuts import get_object_or_404


def login_view(request: HttpRequest):
    error_message = None
    login_type = request.GET.get("type", "customer")  # default to customer

    customer_form = LoginForm()
    shop_form = LoginForm()

    if request.method == "POST":
        login_type = request.POST.get("login_type", "customer")
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(username=username, role=login_type)
                if check_password(password, user.password):
                    if login_type == "customer":
                        request.session["customer_id"] = user.id
                        return redirect("accounts:customer_home_view")
                    elif login_type == "admin":
                        request.session["admin_id"] = user.id
                        return redirect("shops:shop_admin_dashboard")
                else:
                    error_message = "Incorrect password."
            except User.DoesNotExist:
                error_message = "Username does not exist."

        # Preserve filled form
        if login_type == "customer":
            customer_form = form
        else:
            shop_form = form

    return render(request, "login.html", {
        "error_message": error_message,
        "login_type": login_type,
        "customer_form": customer_form,
        "shop_form": shop_form,
    })


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

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                error_message = "Username or Email already exists."
            else:
                User.objects.create(
                    username=username,
                    password=password,
                    full_name=full_name,
                    email=email,
                    role='customer',
                    phone=phone,
                    address=address
                )
                return redirect("main:home_view")
    else:
        form = SignUpForm()

    return render(request, "sign_up.html", {"form": form, "error_message": error_message})


def logout_view(request: HttpRequest):
    request.session.flush()
    return redirect("main:home_view")


def customer_home_view(request: HttpRequest):
    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("accounts:login_view")

    try:
        customer = User.objects.get(pk=customer_id, role='customer')
    except User.DoesNotExist:
        return redirect("accounts:login_view")

    return render(request, "customer_home.html", {"customer": customer})







def profile_view(request):

    user_id = request.session.get('customer_id') or request.session.get('admin_id')

    if not user_id:
        return redirect('accounts:login_view')

    user = get_object_or_404(User, pk=user_id)
    return render(request, "profile.html", {"user": user})


def update_profile_view(request:HttpRequest):

    user_id = request.session.get('customer_id') or request.session.get('admin_id')

    if not user_id:
        return redirect('accounts:login_view')
    
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("accounts:profile_view")
    else:
        form = UpdateProfileForm(instance=user)
    
    return render(request, "update_user.html", {"user":user, "form":form})


def reset_password_view(request:HttpRequest):

    user_id = request.session.get('customer_id') or request.session.get('admin_id')
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        
        old_pass = request.POST.get("old-pass")
        new_pass = request.POST.get("new-pass")
        confirm_pass = request.POST.get("confirm-pass")


        if not check_password(old_pass, user.password):
            messages.error(request, "old password is incorrect.")
        elif new_pass != confirm_pass:
            messages.error(request, "New passwords do not match.")

        else:
            user.password = make_password(new_pass)
            user.save()
            messages.success(request, "Password updated successfully.")
        return redirect("accounts:update_profile_view")

