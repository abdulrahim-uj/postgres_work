import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from basics.functions import generate_form_errors
from .forms import UserForm
from .models import User


def signup(request):
    # Check user is already signed in or not
    if request.user.is_authenticated:
        return redirect('accounts:my_dashboard')
    # Check the request method is POST --> Then
    elif request.method == 'POST':
        form = UserForm(request.POST)
        # If form is valid --> Then
        if form.is_valid():
            # CREATE USER USING THE FORM
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # CREATE USER USING create_user METHOD [from .models UserManager.create_user]
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email_id = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=firstname, last_name=lastname,
                                            username=username, email=email_id,
                                            password=password)
            user.save()
            response_data = {
                "status": "true",
                "title": "New User",
                "message": "New user Successfully Created.",
                "redirect": 'true',
                "redirect_url": reverse('accounts:existing_user')
            }
        # form is not valid --> Then
        else:
            # generating form errors
            message = generate_form_errors(UserForm, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message[0].messages[0]
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    # Request.method is GET --> Then
    else:
        form = UserForm()
        context = {
            'title': "Registration",
            'is_bootstrap': True,
            'form': form,
            "redirect": True,
        }
        return render(request, 'accounts/registration.html', context)


# login existing user
def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            response_data = {
                "status": "true",
                "title": "User",
                "message": "User successfully login.",
                "redirect": 'true',
                "redirect_url": reverse('accounts:my_dashboard')
            }
        else:
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": "Invalid credentials."
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        context = {
            'title': "Sign in",
            'is_bootstrap': True,
            "redirect": True,
        }
    return render(request, 'accounts/signin.html', context)


@login_required(login_url='accounts:existing_user')
def signout(request):
    auth.logout(request)
    response_data = {
        "status": "true",
        "title": "User",
        "message": "User successfully logout.",
        "redirect": 'true',
        "redirect_url": reverse('index')
    }
    return redirect('/')


@login_required(login_url='accounts:existing_user')
def dashboard(request):
    username = request.user.username
    context = {
        'title': username + "\'s home",
        'is_bootstrap': True,
        "redirect": True,
    }
    return render(request, 'dashboard/user-home.html', context)
