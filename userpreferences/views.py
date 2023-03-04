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
    currency_data = []
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    # get currencies json file path
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    # pdb.set_trace()
    # open currencies json file and append file data into python variable
    with open(file_path, 'r',encoding="utf-8") as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name':key, 'value':value})
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method=="GET":
        return render(request,'preferences/index.html',{'currencies':currency_data,
                                                          'user_preferences': user_preferences})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency=currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request,'preferences/index.html',{'currencies':currency_data,
                                                          'user_preferences': user_preferences})
