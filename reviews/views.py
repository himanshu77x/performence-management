from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Review, Profile
from .forms import ReviewForm
from django.contrib.auth.models import User


def dashboard(request):
    reviews = Review.objects.none()  # Empty initially
    profile = None  # Default profile
    
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Or handle error gracefully

        reviews = Review.objects.all()

        # Manager/TL: Show reportees' reviews
        if profile and profile.role in ['Manager', 'TL']:
            reportees = User.objects.filter(profile__reporting_manager=request.user)
            reviews = reviews.filter(employee__in=reportees)

        # Employee: Show only their reviews
        elif profile and profile.role == 'Employee':
            reviews = reviews.filter(employee=request.user)

        # Admin: See all reviews (no filter)
    
    return render(request, 'reviews/dashboard.html', {
        'reviews': reviews,
        'profile': profile
    })

from django.shortcuts import redirect

from django.contrib import messages

def add_review(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Login required to add review!")
            return redirect('dashboard')

        title = request.POST.get('title')
        employee_id = request.POST.get('employee')
        review_date = request.POST.get('review_date')
        review_period = request.POST.get('review_period')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        employee = User.objects.get(id=employee_id)

        Review.objects.create(
            title=title,
            employee=employee,
            review_date=review_date,
            review_period=review_period,
            rating=rating,
            comment=comment,
            reviewer=request.user  # Save reviewer only if logged in
        )

        messages.success(request, "Review Added Successfully!")
        return redirect('dashboard')

    # --- GET Request ---
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.role in ['Manager', 'TL']:
            employees = User.objects.filter(profile__reporting_manager=request.user)
        elif profile.role == 'Admin':
            employees = User.objects.all()
        else:
            employees = User.objects.none()
    else:
        employees = User.objects.none()

    return render(request, 'reviews/add_review.html', {'employees': employees})
