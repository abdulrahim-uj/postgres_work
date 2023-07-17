import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from basics.functions import generate_form_errors
from .forms import UserForm, UserProfileForm
from .models import User, UserProfile
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


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

            # SEND VERIFICATION EMAIL
            email_subject = "Activate Your Account"
            email_template = "accounts/emails/account-verification-email.html"
            send_verification_email(request, user, email_subject, email_template)

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


def activate(request, uidb64, token):
    # ACTIVATE THE USER BY SETTING THE is_activate = True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('accounts:my_dashboard')
    else:
        return redirect('accounts:existing_user')


def profile(request):
    form = UserProfileForm()
    instance = UserProfile.objects.get(user=request.user)
    if instance:
        form = UserProfileForm(instance=instance)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=instance)
        contact_number = request.POST.get('phone_number')
        if form.is_valid():
            if contact_number:
                user = User.objects.get(pk=request.user.pk)
                user.phone_number = contact_number
                user.save()
            data = form.save(commit=False)
            data.country_code = form.cleaned_data['country']
            data.updater = request.user
            data.save()
            response_data = {
                "status": "true",
                "title": "New User",
                "message": "New user Successfully Created.",
                "redirect": 'true',
                "redirect_url": reverse('accounts:my_dashboard')
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
    else:
        context = {
            'title': "Profile",
            'form': form,
            'is_bootstrap': True,
            "redirect": True,
        }
        return render(request, 'accounts/profile.html', context)
