"""Authentication Views
"""
import json
import threading
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from validate_email import validate_email
from .utils import account_activation_token
#pylint: disable=E1101

# Create your views here.

class EmailThread(threading.Thread):
    """Optimize send email speed"""
    def __init__(self, subject, html_content, from_email, recipient_list):
        """Define email variables

        Args:
            subject (str): email subject
            html_content (str): email description
            from_email (str): email sender
            recipient_list (list): list of recipients
        """
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.from_email = from_email
        threading.Thread.__init__(self)

    def run(self):
        """Run send email"""
        send_mail(message=self.html_content,
                  from_email=settings.EMAIL_HOST_USER, subject=self.subject,
                  recipient_list=[self.recipient_list]
                )

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
                current_site = get_current_site(request)
                email_subject = 'Activate Your Account'
                message = render_to_string('authentication/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                EmailThread(subject=email_subject, from_email=settings.EMAIL_HOST_USER,
                            html_content=message, recipient_list=user.email).start()
                messages.add_message(request, messages.SUCCESS,
                                     'Account created successfully,please visit your email to '
                                                                'verify your Account')
                return redirect("login")
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
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO,
                                 "Account has been activated,you may login now")
            return redirect('login')
        messages.add_message(request, messages.WARNING,
                             "verification Link was used before,please login")
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

    def post(self, request):
        """login post request
        Args:
            request (JSON): data is fetched in JSON format

        Returns:
            object: returns user credentials for login
        """
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome '+user.username+', you are now logged in')
                    return redirect("expenses")
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')
        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'authentication/login.html')

class LogoutView(View):
    """Logout class

    Args:
        View (Class): Django class library
    """
    def post(self, request):
        """logout 

        Args:
            request (JSON): url request

        Returns:
            null: log user out and navigate user to login page
        """
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')

class RequestPasswordResetEmail(View):
    """Class to request for an email to reset password
    """
    def get(self, request):
        """request for password 

        Args:
            request (JSON): url request

        Returns:
            Renders reset password page
        """
        return render(request, 'authentication/reset-password.html')
    def post(self, request) :
        """Send a post request
        """
        context = {
            'values': request.POST
        }
        email = request.POST.get('email')
        if not email:
            messages.add_message(request, messages.ERROR,
                                 'please provide a valid email')
            return render(request, 'authentication/reset-password.html', context, status=400)
        current_site = get_current_site(request)
        user = User.objects.filter(email=email).first()
        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Details not found,please consider a signup')
            return render(request, 'authentication/reset-password.html', context, status=404)

        email_subject = 'Reset your Password'
        message = render_to_string('authentication/set-new-password.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        EmailThread(subject=email_subject, from_email=settings.EMAIL_HOST_USER,
                    html_content=message, recipient_list=user.email).start()
        messages.add_message(
            request, messages.INFO, 'We have sent you an email with a link to reset your password')
        return render(request, 'authentication/reset-password.html', context)

class CompletePasswordChangeView(View):
    """User change password"""
    def get(self, request, uidb64, token):
        """Get details"""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None or not account_activation_token.check_token(user, token):
            messages.add_message(
                request, messages.WARNING, 'Link is no longer valid,please request a new one')
            return render(request, 'authentication/reset-password.html', status=401)
        return render(request,
                      'authentication/set-new-password.html', 
                      context={'uidb64': uidb64, 'token': token}
                    )

    def post(self, request, uidb64, token):
        """Update password"""
        context = {'uidb64': uidb64, 'token': token}
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if len(password) < 6:
                messages.add_message(
                    request, messages.ERROR, 'Password should be at least 6 characters long')
                return render(request, 'authentication/set-new-password.html', context, status=400)
            if password != password2:
                messages.add_message(
                    request, messages.ERROR, 'Passwords must match')
                return render(request, 'authentication/set-new-password.html', context, status=400)
            user.set_password(password)
            user.save()
            messages.add_message(
                request,
                messages.INFO,
                'Password changed successfully,login with your new password'
            )
            return redirect('login')
        except DjangoUnicodeDecodeError:
            messages.add_message(
                request, messages.ERROR, 'Something went wrong,you could not update your password')
            return render(request, 'authentication/set-new-password.html', context, status=401)
