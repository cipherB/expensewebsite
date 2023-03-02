"""Import Django libraries
"""
from django.shortcuts import render

# Create your views here.
def index(request):
    """test function
    """
    return render(request,'preferences/index.html')
