from django.shortcuts import render, redirect
from . forms import RegistrationForms
from . models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


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
            messages.success(request, 'Your account is creates successfully.')
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
            auth.login(request, user)
            messages.success(request, 'you are logged in Now')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login Credentials')
            return redirect('account:login')

    return render(request, 'account/login.html')


login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logout Now!!')
    return redirect('login')


def dashboard(request):
    return render(request, 'account/dashboard.html')