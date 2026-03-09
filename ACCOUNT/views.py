from django.shortcuts import render,redirect 
from django.contrib.auth import login 
from .models import UserModel 
from django.contrib import messages
from .utils import genereate_otp, verify_otp as check_otp
from django.core.mail import send_mail 
from django.conf import settings 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']

        user = UserModel.objects.create_user(username=username,email=email,mobile_number=mobile_number,password=password)

        email_otp = genereate_otp() 
        mobile_otp = genereate_otp() 
        user.email_otp=email_otp
        user.mobile_otp=mobile_otp
        user.save() 

        send_mail(
         'Email Verification OTP',
         f'Your otp for email verification is :{email_otp}',
         settings.EMAIL_HOST_USER,
         [email],
         fail_silently=False,
        )
         # Send mobile OTP (you'll need to integrate with an SMS service)
        # For this example, we'll just print it
        print(f"Mobile OTP :{mobile_otp}")
        return redirect('verify_otp',user_id = user.id)
    return render(request,'account/register.html')
        


def verify_otp(request,user_id):
    user = UserModel.objects.get(id=user_id)
    if request.method == "POST":
        email_otp = request.POST['email_otp']
        # mobile_otp = request.POST['mobile_otp']

        if check_otp(email_otp,user.email_otp):
            user.is_email_verified = True 
            user.is_mobile_verified = True 
            user.email_otp = None 
            user.mobile_otp = None 
            user.save()
            return redirect('home')
        else :
            return render(request,'account/verify_otp.html',{'error':'Invalid OTP'})
    return render(request, 'account/verify_otp.html')    



def login(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,userame=username,password=password)
        print(user)
        if user is not None :
            
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'account/login.html')

    return render(request,"account/login.html")








def home(request):
    return HttpResponse("This is homepage ")