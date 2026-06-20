"""
Section B - Task 3: Django Views for Persistence
Section B - Task 4: Render Profiles with DTL
Section C - Task 3: "Save to File" with Context Managers
"""

import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import UserProfile
from .forms import UserProfileForm


# ---------------------------------------------------------------------------
# Section B, Task 4 / Section C, Task 2: List View
# ---------------------------------------------------------------------------
def profile_list(request):
    """
    Retrieves all profiles via the ORM and renders them with DTL.

    UserProfile.objects.all() returns a QuerySet, not a Python list
    (Section A, Q5): it's a lazy, database-backed collection that only
    actually runs the SQL query when it's iterated over (e.g. in the
    {% for %} loop in the template) or otherwise evaluated. A plain Python
    list, by contrast, is already fully loaded in memory the moment it's
    created and has no idea where its data came from.
    """
    profiles = UserProfile.objects.all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})


# ---------------------------------------------------------------------------
# Section B, Task 3 / Section C, Task 1: Create View
# ---------------------------------------------------------------------------
def profile_create(request):
    """
    Handles both displaying a blank form (GET) and processing a submission
    (POST), using the same UserProfileForm built from the model.

    form.is_valid() runs:
      1. Each field's built-in validation (CharField, IntegerField, etc.)
      2. Any clean_<field>() methods we defined (e.g. clean_age)
      3. The form-wide clean() method, if defined

    form.save() then commits a new row directly to the database in one line,
    because ModelForm already knows which model and fields it maps to.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = UserProfileForm()

    return render(request, 'profiles/profile_form.html', {'form': form})


# ---------------------------------------------------------------------------
# Bonus: Edit view (mentioned in Section C Task 1: "Create/Edit via Django Forms")
# ---------------------------------------------------------------------------
def profile_edit(request, pk):
    """Edit an existing profile, reusing the same form and template as create."""
    profile = get_object_or_404(UserProfile, pk=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profiles/profile_form.html', {'form': form, 'profile': profile})


# ---------------------------------------------------------------------------
# Section C, Task 3: "Save to File" with Context Managers
# ---------------------------------------------------------------------------
def profile_export_csv(request):
    """
    Exports all profiles as a downloadable CSV.

    HttpResponse acts as a file-like object here, so csv.writer can write
    straight into it. We still use 'with' as a context manager around the
    *server-side temp handling* pattern Django recommends for larger/streamed
    exports -- but for a simple direct-to-response export like this, the
    safe-handling guarantee that a context manager gives (resources are
    always closed / flushed, even if an error occurs partway through) is
    demonstrated by writing to a local temp file first, then streaming it
    back as the response body. This keeps the actual file I/O wrapped in
    a 'with open(...) as file:' block as the assessment specifies.
    """
    import io
    import tempfile
    import os

    profiles = UserProfile.objects.all()

    # Write to a temporary file using a context manager, exactly as
    # specified: "Use a Context Manager (with open(...) as file:) to
    # ensure proper file handling".
    fd, temp_path = tempfile.mkstemp(suffix='.csv')
    os.close(fd)

    with open(temp_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Age', 'Is Public', 'Bio', 'Created At'])
        for profile in profiles:
            writer.writerow([
                profile.username,
                profile.age,
                profile.is_public,
                profile.bio,
                profile.created_at,
            ])
    # The 'with' block above guarantees the file is flushed and closed
    # here, even if writing raised an exception midway.

    with open(temp_path, mode='r', encoding='utf-8') as file:
        csv_content = file.read()

    os.remove(temp_path)  # clean up the temp file once we've read it back

    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_profiles.csv"'
    return response
