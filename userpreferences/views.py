"""Import Django libraries
"""
import os
import json
# import pdb
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from .models import UserPreference

# Create your views here.
def index(request):
    """test function
    """
    #pylint: disable=E1101
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method=="GET":
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        # pdb.set_trace()
        with open(file_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                currency_data.append({'name':key, 'value':value})
        return render(request,'preferences/index.html',{'currencies':currency_data})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency=currency
            user_preferences.save()
        UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request,'preferences/index.html',{'currencies':currency_data})
