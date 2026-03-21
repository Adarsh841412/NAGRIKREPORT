from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Complaint
from ACCOUNT.models import Officer
from .models import Complaint, ComplaintMedia
from DEPARTMENT.models import Category
from django.shortcuts import get_object_or_404, redirect



@login_required(login_url='login')
def create_complaint(request):

    if request.user.role != "citizen":
        return redirect("officer_login")

    errors = {}
    categories = Category.objects.filter(is_active=True)

    if request.method == "POST":
        category_id = request.POST.get("category")
        title = request.POST.get("title")
        description = request.POST.get("description")
        location_address = request.POST.get("location_address")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        priority = request.POST.get("priority")

        uploaded_files = request.FILES.getlist("media_files")

        category = None

        if not category_id:
            errors["category"] = "Category is required."
        else:
            try:
                category = Category.objects.get(id=category_id, is_active=True)
            except Category.DoesNotExist:
                errors["category"] = "Invalid category selected."

        if not title or len(title.strip()) < 5:
            errors["title"] = "Title must contain at least 5 characters."

        if not description or len(description.strip()) < 20:
            errors["description"] = "Description must contain at least 20 characters."

        if not location_address or len(location_address.strip()) == 0:
            errors["location_address"] = "Address cannot be empty."

        try:
            latitude = float(latitude)
            if latitude < -90 or latitude > 90:
                errors["latitude"] = "Latitude must be between -90 and 90."
        except (TypeError, ValueError):
            errors["latitude"] = "Enter a valid latitude."

        try:
            longitude = float(longitude)
            if longitude < -180 or longitude > 180:
                errors["longitude"] = "Longitude must be between -180 and 180."
        except (TypeError, ValueError):
            errors["longitude"] = "Enter a valid longitude."

        if priority not in ["low", "medium", "high"]:
            errors["priority"] = "Select a valid priority."

        # optional media validation
        allowed_image_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        allowed_video_types = ["video/mp4", "video/webm", "video/ogg", "video/quicktime"]

        for file in uploaded_files:
            if file.content_type not in allowed_image_types + allowed_video_types:
                errors["media_files"] = "Only image or video files are allowed."
                break

        if errors:
            return render(
                request,
                "complaint/create_complaint.html",
                {
                    "errors": errors,
                    "categories": categories
                }
            )

        try:
            complaint = Complaint.objects.create(
                user=request.user,
                category=category,
                title=title,
                description=description,
                location_address=location_address,
                latitude=latitude,
                longitude=longitude,
                priority=priority
            )

            for file in uploaded_files:
                if file.content_type in allowed_image_types:
                    media_type = "image"
                elif file.content_type in allowed_video_types:
                    media_type = "video"
                else:
                    continue

                ComplaintMedia.objects.create(
                    complaint=complaint,
                    media_file=file,
                    media_type=media_type
                )

            messages.success(request, "Complaint submitted successfully.")
            return redirect("my_complaints")

        except ValidationError as e:
            if hasattr(e, "message_dict"):
                errors = e.message_dict
            else:
                errors["general"] = "Something went wrong."

    return render(
        request,
        "complaint/create_complaint.html",
        {
            "errors": errors,
            "categories": categories
        }
    )




@login_required(login_url='login')
def my_complaints(request):

    if request.user.role != "citizen":
        return redirect("officer_login")

    complaints = Complaint.objects.filter(
        user=request.user
    ).select_related("category").prefetch_related("media_files").order_by("-created_at")

    return render(
        request,
        "complaint/my_complaints.html",
        {
            "complaints": complaints
        }
    )


@login_required(login_url="login")
def view_complaint_officer(request):

    if request.user.role != "officer":
        messages.error(request, "You are not authorized to view this page.")
        return redirect("home")

    try:
        officer = Officer.objects.get(user_id=request.user)
        # print(officer,"AFSssdfsdfsdsfd")
    except Officer.DoesNotExist:
        messages.error(request, "Officer profile not found.")
        return redirect("home")

    complaints = Complaint.objects.filter(
        assigned_officer=officer
    ).order_by("-created_at")
    return render(
        request,
        "complaint/view_complaints.html",
        {"complaints": complaints}
    )


@login_required(login_url="login")
def start_complaint_work(request, complaint_id):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("view_complaint_officer")

    if request.user.role != "officer":
        messages.error(request, "You are not authorized to perform this action.")
        return redirect("home")

    try:
        officer = Officer.objects.get(user_id=request.user)
    except Officer.DoesNotExist:
        messages.error(request, "Officer profile not found.")
        return redirect("home")

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        assigned_officer=officer
    )

    if complaint.status != "pending":
        messages.error(request, "Only pending complaints can be started.")
        return redirect("view_complaint_officer")

    complaint.status = "in_progress"
    complaint.save()

    messages.success(request, "Complaint marked as In Progress.")
    return redirect("view_complaint_officer")



@login_required(login_url='login')
def resolve_complaint_work(request, complaint_id):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('view_complaint_officer')

    if request.user.role != "officer":
        messages.error(request, "You are not an authorized person.")
        return redirect("home")

    try:
        officer = Officer.objects.get(user_id=request.user)
    except Officer.DoesNotExist:
        messages.error(request, "Officer profile not found.")
        return redirect("home")

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        assigned_officer=officer
    )

    if complaint.status != "in_progress":
        messages.error(request, "Only in-progress complaints can be resolved.")
        return redirect("view_complaint_officer")

    complaint.status = "resolved"
    complaint.save()

    messages.success(request, "Complaint resolved successfully.")
    return redirect("view_complaint_officer")





@login_required(login_url='login')
def reject_complaint_work(request, complaint_id):
    print("i am adarsh")
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('view_complaint_officer')

    if request.user.role != "officer":
        messages.error(request, "You are not an authorized person.")
        return redirect("home")

    try:
        officer = Officer.objects.get(user_id=request.user)
    except Officer.DoesNotExist:
        messages.error(request, "Officer profile not found.")
        return redirect("home")

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        assigned_officer=officer
    )

    if complaint.status == "resolved":
        messages.error(request, "Only progress or not start complaints can be reject.")
        return redirect("view_complaint_officer")

    complaint.status = "invalid"
    complaint.save()

    messages.success(request, "Complaint reject successfully.")
    return redirect("view_complaint_officer")    





@login_required(login_url='login')
def complaint_detail(request, id):

    try:
        complaint = Complaint.objects.get(id=id, user=request.user)
    except Complaint.DoesNotExist:
        return redirect("my_complaints")

    return render(
        request,
        "complaint/complaint_detail.html",
        {
            "complaint": complaint
        }
    )