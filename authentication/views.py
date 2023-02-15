"""Authentication Views
"""
import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email

# Create your views here.

class UsernameValidationView(View):
    """Username validation view

    Args:
        View (Django function): return requests
    """
    def post(self,request):
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
                {'username_error':'Username should only contain alpha-numeric characters.'},
                status=400
                )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {'username_error':'Username already exists, enter another one.'},
                status=409
                )
        return JsonResponse({'username_valid':True})
    
class EmailValidationView(View):
    """Email validation view

    Args:
        View (Django function): return requests
    """
    def post(self,request):
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
                {'email_error':'Email is invalid.'},
                status=400
                )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {'email_error':'Email already exists, enter another one.'},
                status=409
                )
        return JsonResponse({'email_valid':True})

class RegistrationView(View):
    """Registration Page View

    Args:
        View (Django function): return requests
    """
    def get(self,request):
        """Get Request

        Args:
            request (object): url page request

        Returns:
            html synthax: returns html page for register
        """
        return render(request, 'authentication/register.html')
