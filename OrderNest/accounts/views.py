from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password, make_password

from OrderNest import settings
from .models import User, Address
from .forms import LoginForm, SignUpForm, UpdateProfileForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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
            address_text = form.cleaned_data['address'] 

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                error_message = "Username or Email already exists."
            else:
                user = User.objects.create(
                    username=username,
                    password=password,
                    full_name=full_name,
                    email=email,
                    role='customer',
                    phone=phone
                )
                Address.objects.create(
                    user=user,
                    title="Default",
                    address=address_text,
                    latitude=0.0,
                    longitude=0.0
                )
                return redirect("main:home_view")
    else:
        form = SignUpForm()

    return render(request, "sign_up.html", {"form": form, "error_message": error_message})



def logout_view(request):
    cart_backup = request.session.get('cart')  # save cart
    logout(request)
    request.session.flush() 

    # restore cart after flush (start a new session first)
    request.session['cart'] = cart_backup
    request.session.modified = True

    return redirect('main:home_view')  # or wherever you redirect


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
    return render(request, "profile.html", {"user": user, "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY})


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

@require_POST
def add_address_view(request):
    user_id = request.session.get('customer_id') or request.session.get('admin_id')
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, pk=user_id)

    lat = request.POST.get("latitude")
    lng = request.POST.get("longitude")
    if not lat or not lng:
        messages.error(request, "Please select a location on the map before saving the address.")
        return redirect("accounts:profile_view")

    Address.objects.create(
        user=user,
        title=request.POST.get("title", ""),
        address=request.POST.get("address"),
        latitude=float(lat),
        longitude=float(lng),
    )
    messages.success(request, "Address added successfully.")
    return redirect("accounts:profile_view")

@require_POST
def delete_address_view(request, address_id):
    user_id = request.session.get('customer_id') or request.session.get('admin_id')
    address = get_object_or_404(Address, id=address_id, user_id=user_id)
    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect("accounts:profile_view")

@require_POST
def update_address_view(request, address_id):
    user_id = request.session.get('customer_id') or request.session.get('admin_id')
    address = get_object_or_404(Address, id=address_id, user_id=user_id)

    lat = request.POST.get("latitude")
    lng = request.POST.get("longitude")
    if not lat or not lng:
        messages.error(request, "Please select a location on the map.")
        return redirect("accounts:profile_view")

    address.title = request.POST.get("title", "")
    address.address = request.POST.get("address")
    address.latitude = float(lat)
    address.longitude = float(lng)
    address.save()
    messages.success(request, "Address updated successfully.")
    return redirect("accounts:profile_view")
