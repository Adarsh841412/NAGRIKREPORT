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
from django.core.exceptions import ValidationError
from django.utils import timezone

def register(request):

    errors = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        role = request.POST.get('role')
        profile_picture = request.FILES.get('profile_picture')
        # Username exists check
        if UserModel.objects.filter(username=username).exists():
            errors['username'] = ["Username already exists"]

        # Email exists check
        if UserModel.objects.filter(email=email).exists():
            errors['email'] = ["Email already registered"]

        # Mobile exists check
        if UserModel.objects.filter(mobile_number=mobile_number).exists():
            errors['mobile_number'] = ["Mobile already registered"]

        # Password strength
        if password and len(password) < 6:
            errors['password'] = ["Password must be 6 characters"]

        # Mobile validation
        if not mobile_number.isdigit():
            errors['mobile_number'] = ["Only digits allowed"]

        if len(mobile_number) != 10:
            errors['mobile_number'] = ["Mobile must be 10 digits"]

        if errors:
            return render(
                request,
                'account/register.html',
                {"errors":errors}
            )

        try:

            user = UserModel.objects.create_user(
                username=username,
                email=email,
                mobile_number=mobile_number,
                password=password,
                role=role,
                profile_picture = profile_picture
            )

            email_otp = genereate_otp()
            mobile_otp = genereate_otp()

            user.email_otp = email_otp
            user.mobile_otp = mobile_otp

            user.otp_created_at = timezone.now()

            user.save()

        except ValidationError as e:

            errors = e.message_dict

            return render(
                request,
                'account/register.html',
                {"errors":errors}
            )

        send_mail(

            'Email Verification OTP',

            f'Your OTP is {email_otp}',

            settings.EMAIL_HOST_USER,

            [email],

            fail_silently=False,

        )

        print("Mobile OTP:",mobile_otp)

        return redirect('verify_otp',user_id=user.id)

    return render(
        request,
        'account/register.html',
        {"errors":errors}
    )


from django.utils import timezone
from datetime import timedelta

def verify_otp(request,user_id):

    user = UserModel.objects.get(id=user_id)

    error = None

    if request.method == "POST":

        email_otp = request.POST.get('email_otp')

        # OTP expiry check (5 min)
        if user.otp_created_at:

            if timezone.now() > user.otp_created_at + timedelta(minutes=5):

                error = "OTP expired"

                return render(
                    request,
                    'account/verify_otp.html',
                    {'error':error}
                )

        if check_otp(email_otp,user.email_otp):

            user.is_email_verified = True
            user.is_mobile_verified = True

            user.email_otp = None
            user.mobile_otp = None

            user.save()

            return redirect('select_role')

        else:

            error = "Invalid OTP"

    return render(
        request,
        'account/verify_otp.html',
        {'error':error}
    )


# * citizen login view 
def login1(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None :
            
            login(request,user)
            # here i decide agr user login kre reha hia to kis page pais jauega 
            # citizen to kis page pai jayega 
            return redirect('home')  
        
        
        else:
            print("all set ")
            messages.error(request, 'Invalid username or password.')
            return render(request, 'account/login.html')

    return render(request,"account/login.html")

from django.core.exceptions import ValidationError






def officer(request):

    errors = {}

    if request.method == "POST":

        user_id = request.POST.get('user_id')
        designation = request.POST.get('designation')
        lon = request.POST.get('lon')
        lat = request.POST.get('lat')
        landmark = request.POST.get('landmark')

        # Required validation
        if not user_id:
            errors['user'] = "User required"

        if not designation:
            errors['designation'] = "Designation required"

        if not lon or not lat:
            errors['location'] = "Location required"

        if not landmark:
            errors['landmark'] = "Landmark required"

        # User validation
        try:
            user = UserModel.objects.get(id=user_id)

            if user.role != "officer":
                errors['user'] = "User must have officer role"

        except UserModel.DoesNotExist:
            errors['user'] = "User not found"

        # Duplicate officer check
        if Officer.objects.filter(user_id=user_id).exists():
            errors['user'] = "Officer already assigned"

        # Latitude validation
        try:

            lat = float(lat)

            if lat < -90 or lat > 90:
                errors['lat'] = "Invalid latitude"

        except:
            errors['lat'] = "Latitude must be number"

        # Longitude validation
        try:

            lon = float(lon)

            if lon < -180 or lon > 180:
                errors['lon'] = "Invalid longitude"

        except:
            errors['lon'] = "Longitude must be number"

        # If errors exist
        if errors:

            users = UserModel.objects.all()

            return render(

                request,
                'account/officer_create.html',
                {
                    'errors':errors,
                    'users':users
                }
            )

        # Create officer safely
        try:

            Officer.objects.create(

                user_id=user,
                designation=designation,
                lon=lon,
                lat=lat,
                landmark=landmark
                

            )

        except ValidationError as e:

            errors = e.message_dict

            users = UserModel.objects.all()

            return render(

                request,
                'account/officer_create.html',

                {
                    'errors':errors,
                    'users':users
                }
            )

        return redirect('officer_login')

    users = UserModel.objects.filter(role='officer')

    return render(

        request,
        'account/officer_create.html',

        {
            'users':users
        }
    )



# here i decide registration of user or officer 
def index(request):

    if request.method=="POST":
        person = request.POST.get('role') 
        if person == "citizen":
            return redirect('register')
        elif person == 'officer':
            return redirect('officer')
    return render(request,"account/index.html")    



#* here i select role for login 
def select_role(request):
    return render(request,"account/index1.html")


#* this is a page where officer will login 
def Officerlogin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:

            if user.role == "officer":

                login(request,user)

                return redirect("officer_page")

            else:

                messages.error(request,"You are not authorized as officer")

        else:
            print("Afsdfdfsd")
            messages.error(request,"Invalid Username or Password")
            return redirect('officer_login')

    
    return render(request,"account/officer_login.html")



# * officer login come to this dashboard 
@login_required(login_url='officer_login')
def OfficerPage(request):

    if request.user.role != "officer":
        return redirect("login")

    return render(request,"account/officer_dashboard.html")



# here citizen login  after come to this dasboard 

@login_required(login_url='login')
def citizen_dashboard(request):

    if request.user.role != "citizen":
        return redirect("officer_login")

    return render(request,"account/citizen_dashboard.html")





# * add logout views 

def logout_view(request):

    role = None

    if request.user.is_authenticated:
        role = request.user.role
        print(role)

    logout(request)

    if role == "officer":
        return redirect("officer_login")

    return redirect("login")







# * making user profile page 

def user_profile(request):
   if request.user.is_authenticated:
    # user = UserModel.objects.get(id=request.user.id)
    # print("jlkfdsasd",user.profile_picture.url)
    return render(request,'account/user_profile.html',{'user_data':request.user})


# * edit profile citizen 


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserModel


@login_required(login_url='login')
def edit_profile_citizen(request):

    errors = {}
    user = request.user

    if request.method == "POST":

        profile_picture = request.FILES.get('profile_picture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        # address = request.POST.get('address')

        # Username validation
        if not username or len(username.strip()) < 3:
            errors['username'] = ["Username must be at least 3 characters long."]
        elif UserModel.objects.exclude(id=user.id).filter(username=username).exists():
            errors['username'] = ["Username already exists."]

        # Email validation
        if not email:
            errors['email'] = ["Email is required."]
        elif UserModel.objects.exclude(id=user.id).filter(email=email).exists():
            errors['email'] = ["Email already registered."]

        # Mobile validation
        if not mobile_number:
            errors['mobile_number'] = ["Mobile number is required."]
        elif not mobile_number.isdigit():
            errors['mobile_number'] = ["Mobile number must contain digits only."]
        elif len(mobile_number) != 10:
            errors['mobile_number'] = ["Mobile number must be exactly 10 digits."]
        elif UserModel.objects.exclude(id=user.id).filter(mobile_number=mobile_number).exists():
            errors['mobile_number'] = ["Mobile number already registered."]

        # # Address validation
        # if address and len(address.strip()) < 5:
        #     errors['address'] = ["Address must be at least 5 characters long."]

        if errors:
            return render(
                request,
                "account/edit_profile_citizen.html",
                {
                    "errors": errors
                }
            )

        user.username = username.strip()
        user.email = email.strip()
        user.mobile_number = mobile_number.strip()
        # user.address = address.strip() if address else ""

        if profile_picture:
            user.profile_picture = profile_picture

        user.save()
        return redirect('user_profile')

    return render(
        request,
        "account/edit_profile_citizen.html",
        {
            "errors": errors
        }
    )







# * handle 404 error 


def custom_page_not_found_view(request, exception=None):


    return render(request, "account/404.html", {}, status=404)



