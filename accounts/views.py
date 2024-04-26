from django.shortcuts import render, redirect
from carts.models import Cart, CartItem
from .forms import RegistrationForms
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
import requests
from django.http import HttpResponse
# Account verification import
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage


def register(request):
    if request.method == "POST":
        form = RegistrationForms(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # User Activation Process
            current_site = get_current_site(request)
            mail_subject = "Please Activated you account"
            message = render_to_string('account/account_verification_email.html', {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registration with us  we have send you  a verification email to your email address. please verify it.')
            return redirect("/account/login/?command=verification&email=" + email)
        else:
            print(form.errors)
            messages.error(
                request, 'your account was not created successfully!!')
    else:
        form = RegistrationForms()
    context = {
        "form": form
    }
    return render(request, 'account/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # get the product variation by cart -id

                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                # get the cart item from the user to access his product variation
                cart_item = CartItem.objects.filter(user=user)
                # existing variation in database
                # current variation
                # item id in databases should check
                ex_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                # product_variation = [1,2,3,4,5]
                # ex_var_list = [2,3,4]
                for pro in product_variation:
                    if pro in ex_var_list:
                        index = ex_var_list.index(pro)
                        item_id = id[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        cart_item = CartItem.objects.filter(cart=cart)
                        print(cart_item)
                        for item in cart_item:
                            item.user = user
                            item.save()
            except:
                print('entering inside except block')
                pass
            auth.login(request, user)
            messages.success(request, 'you are logged in Now')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('new url --------> query', query)
                params = dict(x.split('=') for x in query.split('&'))
                print('-------------->>>>>>>>>>', params)
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)

            except:
                return redirect('account:dashboard')

        else:
            messages.error(request, 'Invalid login Credentials')
            return redirect('account:login')

    return render(request, 'account/login.html')


login_required(login_url='login')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logout Now!!')
    return redirect('account:login')


def dashboard(request):
    return render(request, 'account/dashboard.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation Link')
        return redirect('register')
