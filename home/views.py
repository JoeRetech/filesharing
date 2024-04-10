from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from rest_framework.parsers import MultiPartParser


from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import EmailForm
from django.core.mail import send_mail


def index(request):
    return render(request,'landingpage.html')

def admin(request):
    return redirect('/admin/')

def register(request):
  
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "Email already taken")
            return redirect('/register/')
        
        user =User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email=username,
            password = password
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created Successfully")
        return redirect('/login/')
    return render(request, 'register.html')
        
    

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username = username,password = password )
        
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('/login/')
        
        else:
            login(request,user)
            return redirect('/home/')
    
    return render(request,'login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def home(request):
    return render(request ,'home.html')

def download(request , uid):
    return render(request , 'download.html' , context = {'uid' : uid})

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self , request):
        try:
            data = request.data

            serializer = FileListSerializer(data = data)
        
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'files uploaded successfully',
                    'data' : serializer.data
                })
            
            return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data'  : serializer.errors
            })
        except Exception as e:
            print(e)



def send_email(request):
    form = EmailForm()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            share_to = form.cleaned_data['share_to']
            message = form.cleaned_data['message']

            subject =  f'Message from {request.user.username}'
            from_email = 'amlananshu6a@gmail.com'
            recipient_list = [share_to.email]

            send_mail(subject, message, from_email, recipient_list)

            Shared.objects.create(sender=request.user,message=message,recipient_list=recipient_list)
            
            return redirect('/home/')  # Redirect to a thank-you page or any other desired page

    return render(request, 'share_to.html', {'form': form})

def shared(request):
    shares=Shared.objects.all()
    return render(request,'shared.html',{'shares':shares})

