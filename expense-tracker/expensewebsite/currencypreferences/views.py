from django.shortcuts import render
import os, json
from django.conf import settings
from .models import CurrencyPreferences
from django.contrib import messages


# Create your views here.

def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'currencies.json')
    #print(file_path)
    
    with open(file_path,'r') as currency_file:
        data = json.load(currency_file)
        for k,v in data.items():
            currency_data.append({'name': k,'value': v})
        #import pdb
        #pdb.set_trace()
    pref_exist = CurrencyPreferences.objects.filter(user=request.user).exists()
    cur_preference = None
    if pref_exist:
        cur_preference = CurrencyPreferences.objects.get(user=request.user)

    if request.method == 'POST':
        currency = request.POST['currency']
        cur_preference.currency = currency
        if pref_exist:
            cur_preference.save()
        else:
            CurrencyPreferences.objects.create(user=request.user,currency=currency)
        messages.success(request,"Currency preference has been saved")
        #return render(request,'preferences/index.html',{'currencies': currency_data,'cur_preference': cur_preference})    
    return render(request,'preferences/index.html',{'currencies': currency_data,'cur_preference': cur_preference})

'''
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = CurrencyPreferences.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = CurrencyPreferences.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})
    else:

        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            CurrencyPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
'''