from django.shortcuts import render,redirect 
from django.contrib.auth import login 
from .models import UserModel ,Officer 
from django.contrib import messages
from .utils import genereate_otp, verify_otp as check_otp
from django.core.mail import send_mail 
from django.conf import settings 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .indexform import IndexForm

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
            return redirect('login')
        else :
            return render(request,'account/verify_otp.html',{'error':'Invalid OTP'})
    return render(request, 'account/verify_otp.html')    



def login1(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None :
            
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'account/login.html')

    return render(request,"account/login.html")



def officer(request):
    
    if request.method == "POST":

        user_id = request.POST.get('user_id')
        designation = request.POST.get('designation')
        lon = request.POST.get('lon')
        lat = request.POST.get('lat')
        landmark = request.POST.get('landmark')

        # get user object
        user = UserModel.objects.get(id=user_id)

        # create officer
        Officer.objects.create(
            user_id=user,
            designation=designation,
            lon=lon,
            lat=lat,
            landmark=landmark
        )
        return redirect('home')
    
    users = UserModel.objects.all() 
    return render(request,'account/officer_create.html',{'users':users})



@login_required(login_url='/login')
def home(request):
    return HttpResponse("This is homepage ")


def index(request):

    if request.method=="POST":
        person = request.POST.get('role') 
        if person == "citizen":
            return redirect('register')
    return render(request,"account/index.html")    




