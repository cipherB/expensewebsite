"""Authentication Views
"""
import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from validate_email import validate_email
from .utils import token_generator

# Create your views here.


class UsernameValidationView(View):
    """Username validation view

    Args:
        View (Django function): return requests
    """

    def post(self, request):
        """Get post request from registration page

        Args:
            request (Json): Get Json and convert it to python readable format and store
            the username in a variable

        Returns:
            Object: returns a message after validating username
        """
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse(
                {'username_error': 'Username should only contain alpha-numeric characters.'},
                status=400
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {'username_error': 'Username already exists, enter another one.'},
                status=409
            )
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    """Email validation view

    Args:
        View (Django function): return requests
    """

    def post(self, request):
        """Get post request from registration page

        Args:
            request (Json): Get Json and convert it to python readable format and 
            store the email in a variable

        Returns:
            Object: returns a message after validating username
        """
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse(
                {'email_error': 'Email is invalid.'},
                status=400
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {'email_error': 'Email already exists, enter another one.'},
                status=409
            )
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    """Registration Page View

    Args:
        View (Django function): return requests
    """

    def get(self, request):
        """Get Request

        Args:
            request (object): url page request

        Returns:
            html synthax: returns html page for register
        """
        return render(request, 'authentication/register.html')

    def post(self, request):
        """Registration Endpoint post request

        Args:
            request (JSOn): Recieves a JSON object from registration form,
            *Get user data
            *validate the fetched data
            *create a user account

        Returns:
            String: returns a status code message
        """
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                # connection = get_connection()
                # connection.open()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                email_subject = "Activate your account"
                activate_url = "http://"+domain+link
                email_body = f"""
                Hi 
                {user.username}  
                Please use this link to verify your account\n {activate_url}"""
                email_msg = EmailMessage(
                    email_subject,
                    email_body,
                    'dummymail1005@gmail.com',
                    [email, ],
                    ['bcc@example.com'],
                    reply_to=['another@example.com'],
                    headers={'Message-ID': 'foo'},
                )
                email_msg.send(fail_silently=False)
                #
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')


class VerificationView(View):
    """Verification of Email account to activate user status

    Args:
        View (class): View class
    """

    def get(self, request, uidb64, token):
        """validate and redirect user to login

        Args:
            request (string): url request
            uidb64 (string): unique id
            token (string): user token

        Returns:
            redirect: redirects user to login page
        """
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not token_generator.check_token(user, token):
                return redirect('login'+'user already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect("login")
        #pylint: disable=W0612
        #pylint: disable=W0718
        except Exception as ex:
            pass
        return redirect('login')

class LoginView(View):
    """Login Class 

    Args:
        View (class): django class library
    """
    def get(self, request):
        """login function

        Args:
            request (object): url request

        Returns:
            render: redirects user to login page
        """
        return render(request, 'authentication/login.html')
    