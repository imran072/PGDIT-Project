from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'email is not valid'}, status=400)
        if User.objects.filter(email=email):
            return JsonResponse({'username_error':'email is already taken'}, status=409)
        return JsonResponse({'email':True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'name should be alphanumeric.'}, status=400)
        if User.objects.filter(username=username):
            return JsonResponse({'username_error':'name already exits. try again.'}, status=409)
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
