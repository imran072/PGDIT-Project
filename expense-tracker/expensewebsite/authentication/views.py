from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'email is not valid'}, status=400)
        if User.objects.filter(email=email):
            return JsonResponse({'email_error':'email is already taken'}, status=409)
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
    def post(self,request):
        #get user data
        #validate the data
        #create account and save the user
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValue' : request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request,'Password should be at least 8 characters')
                    return render(request,'authentication/register.html',context)
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request,'Account creation is successful!')
                return render(request,'authentication/login.html')
        return render(request,'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user=auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, 'Welcome, ' +user.username)
                    return redirect('expense')
            messages.error(request,'Invalid credentials. Please try again.')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request,'You have been logout from your account')
        return redirect('login')