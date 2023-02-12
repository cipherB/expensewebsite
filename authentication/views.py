"""Authentication Views
"""
from django.shortcuts import render
from django.views import View

# Create your views here.

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
