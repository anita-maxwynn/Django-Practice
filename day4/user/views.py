from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import Profile,Result
# Create your views here.
def registration(request):
    if request.method == 'POST':
        fm = RegistrationForm(request.POST)
        if fm.is_valid():
            # Save the form data to database
            profile = fm.save()
            messages.success(request, f'Profile for {profile.name} created successfully!')
            return redirect('registration')  # Redirect to same page or success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        fm = RegistrationForm()
    
    return render(request, 'ProfileRegistration.html', {'form': fm})

def all_profiles(request):
    profiles = Profile.objects.all()
    print(f"Number of profiles found: {profiles.count()}")  # Debug print
    for profile in profiles:
        print(f"Profile: {profile.name} - {profile.email}")  # Debug print
    return render(request, 'all_profiles.html', {'profiles': profiles})

def modify_profile(request, pk):
    try:
        profile = Profile.objects.get(roll=pk)
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('all_profiles')

    if request.method == 'POST':
        fm = RegistrationForm(request.POST)
        if fm.is_valid():
            new_name = fm.cleaned_data['name']
            new_email = fm.cleaned_data['email']
            new_roll = fm.cleaned_data['roll']
            new_city = fm.cleaned_data['city']

            email_conflict = Profile.objects.exclude(pk=profile.pk).filter(email=new_email).exists()
            roll_conflict = Profile.objects.exclude(pk=profile.pk).filter(roll=new_roll).exists()

            if email_conflict:
                messages.error(request, 'This email is already in use by another profile.')
            elif roll_conflict:
                messages.error(request, 'This roll number is already assigned to another profile.')
            else:
                profile.name = new_name
                profile.email = new_email
                profile.roll = new_roll
                profile.city = new_city
                profile.save()
                messages.success(request, f'Profile for {profile.name} updated successfully!')
                return redirect('all_profiles')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        fm = RegistrationForm(initial={
            'name': profile.name,
            'email': profile.email,
            'roll': profile.roll,
            'city': profile.city,
        })

    return render(request, 'modifyprofile.html', {'form': fm, 'profile': profile})

from django.contrib import messages

def get_result(request):
    if request.method == 'POST':
        stu_class = request.POST.get('stu_class')
        marks = request.POST.get('marks')

        print(f"DEBUG: stu_class={stu_class!r}, marks={marks!r}")

        if stu_class and marks:
            try:
                marks = int(marks)
                Result.objects.create(stu_class=stu_class, marks=marks)
                messages.success(request, 'Result saved successfully!')
            except ValueError:
                messages.error(request, 'Marks must be a valid integer.')
        else:
            messages.error(request, 'Please fill in all fields.')

    results = Result.objects.all()
    return render(request, 'result.html', {'results': results})


