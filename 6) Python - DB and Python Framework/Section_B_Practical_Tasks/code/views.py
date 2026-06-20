"""
Section B - Task 3: Django Views for Persistence
Section B - Task 4: Render Profiles with DTL

(This is the Section-B-only excerpt. The full views.py inside the
social_profile_manager project also includes the Section C CSV export
view and an edit view — see profiles/views.py there.)
"""

from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm


# ---------------------------------------------------------------------------
# Task 4: List View
# ---------------------------------------------------------------------------
def profile_list(request):
    """
    Retrieves all profiles via the ORM and renders them with DTL.

    UserProfile.objects.all() returns a QuerySet, not a Python list
    (Section A, Q5): it's a lazy, database-backed collection that only
    actually runs the SQL query when it's iterated over (e.g. in the
    {% for %} loop in the template) or otherwise evaluated.
    """
    profiles = UserProfile.objects.all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})


# ---------------------------------------------------------------------------
# Task 3: Create View (handles POST + form.is_valid() + form.save())
# ---------------------------------------------------------------------------
def profile_create(request):
    """
    Handles both displaying a blank form (GET) and processing a submission
    (POST), using the same UserProfileForm built from the model.

    form.is_valid() runs:
      1. Each field's built-in validation (CharField, IntegerField, etc.)
      2. Any clean_<field>() methods we defined (e.g. clean_age)
      3. The form-wide clean() method, if defined

    form.save() then commits a new row directly to the database in one
    line, because ModelForm already knows which model and fields it maps to.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = UserProfileForm()

    return render(request, 'profiles/profile_form.html', {'form': form})
