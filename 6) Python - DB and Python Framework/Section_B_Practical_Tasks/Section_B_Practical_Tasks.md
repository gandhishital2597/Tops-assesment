# Section B: Practical Tasks
**Theme: Social Media Profile Manager — DB and Python Framework Assessment**

This section implements four core Django building blocks: the model, the
form with custom validation, the view that persists data, and the template
that renders it. These same files are reused (and extended) in Section C's
mini project — see `social_profile_manager/profiles/` for the integrated
version running inside the full app. Standalone copies of each file are
also included in `section_b_standalone/` alongside this document, so Task
1–4 can be reviewed independently of the rest of the project.

---

## Task 1: Define UserProfile Model

**File:** `models.py`

A class inheriting from `models.Model`, with `CharField` for the username,
`IntegerField` for age, and `BooleanField` for the `is_public` status.

```python
from django.db import models


class UserProfile(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text="Public display name for the profile."
    )
    age = models.IntegerField(
        help_text="User's age in years. Must be 13 or older (see UserProfileForm.clean_age)."
    )
    is_public = models.BooleanField(
        default=True,
        help_text="If True, the profile is visible to everyone; if False, it is private."
    )
    bio = models.TextField(
        max_length=300,
        blank=True,
        help_text="Optional short bio shown on the profile page."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest profiles first

    def __str__(self):
        return self.username
```

**Notes:**
- `username`, `age`, and `is_public` are the three fields explicitly
  required by the task. `bio` and `created_at` are added as reasonable
  extensions for a usable profile (a bio to display, and a timestamp to
  order profiles by recency) — easy to remove if the assessment wants the
  model kept to exactly three fields.
- `unique=True` on `username` prevents duplicate display names at the
  database level, not just in application code.
- `__str__` makes `UserProfile` objects print as their username (e.g. in
  the Django admin or shell) instead of an unhelpful `UserProfile object (1)`.

---

## Task 2: Create ModelForm & Validation

**File:** `forms.py`

`UserProfileForm` extends `forms.ModelForm`, which auto-generates form
fields directly from the model. A `clean_age()` method adds the custom
constraint that the user must be over 13.

```python
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'age', 'is_public', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

    def clean_age(self):
        """
        Django automatically calls clean_<fieldname>() for any field that
        has one defined, after that field's default validation has already
        run. Returning the cleaned value (or raising ValidationError) is
        required - this is the contract Django expects.
        """
        age = self.cleaned_data.get('age')
        if age is not None and age <= 13:
            raise forms.ValidationError(
                "You must be older than 13 years old to create a profile."
            )
        return age

    def clean_username(self):
        """
        Extra validation: reject blank or whitespace-only usernames even
        though CharField alone wouldn't catch a string of just spaces.
        """
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError("Username cannot be blank.")
        return username
```

**Notes:**
- `ModelForm` + `Meta.model` is what gives the "automatic" part: Django
  inspects `UserProfile` and builds matching form fields (a text input for
  `username`, a number input for `age`, a checkbox for `is_public`) without
  the fields being redeclared by hand.
- `clean_age()` is the task's required custom constraint. It runs *after*
  `IntegerField`'s own validation, so by the time this method executes,
  `age` is already guaranteed to be a valid integer — `clean_age()` only
  needs to check the business rule (`> 13`), not the type.
- `clean_username()` is an extra validator added on top of what was asked,
  demonstrating the same pattern applied to a second field. Safe to omit
  if the assessment expects only `clean_age()`.

---

## Task 3: Django Views for Persistence

**File:** `views.py` (relevant function only — full file also handles
Task 4 and the Section C export view)

A function-based view handling `POST` requests, using `form.is_valid()`
to check inputs and `form.save()` to commit the new profile to the database.

```python
from django.shortcuts import render, redirect
from .forms import UserProfileForm


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
```

**Notes:**
- This is a **function-based view** (the task allows either function- or
  class-based). It branches on `request.method`: `GET` shows an empty
  form, `POST` validates and saves submitted data.
- After a successful save, the view redirects to `profile_list` rather
  than re-rendering the same page — this is the standard
  "redirect-after-POST" pattern, which avoids accidental duplicate
  submissions if the user refreshes the page.
- If `form.is_valid()` returns `False`, the view falls through and
  re-renders `profile_form.html` with the same `form` object, which now
  carries its `.errors` — so the template can display what went wrong.

---

## Task 4: Render Profiles with DTL

**File:** `views.py` (view) + `profile_list.html` (template)

Retrieves all profiles using `UserProfile.objects.all()`, passes them to
a template, and uses a DTL `{% for %}` loop to display the username and
age in an HTML list.

**View:**
```python
from django.shortcuts import render
from .models import UserProfile


def profile_list(request):
    """
    UserProfile.objects.all() returns a QuerySet, not a Python list
    (see Section A, Q5): it's lazy and only actually runs the SQL query
    when iterated over — e.g. by the {% for %} loop in the template.
    """
    profiles = UserProfile.objects.all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})
```

**Template (`profile_list.html`):**
```html
{% if profiles %}
    <ul class="profile-list">
        {% for profile in profiles %}
            <li>
                <strong>{{ profile.username }}</strong> &mdash; Age: {{ profile.age }}
            </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No profiles yet.</p>
{% endif %}
```

**Notes:**
- The view's only job is to fetch data and hand it to the template via
  the context dictionary (`{'profiles': profiles}`) — it does not build
  any HTML itself. That separation of concerns (data in the view, markup
  in the template) is the core idea behind Django's MVT structure.
- `{% for profile in profiles %}` iterates the QuerySet exactly like a
  Python `for` loop would iterate a list, but the underlying SQL `SELECT`
  is only executed at this point (lazy evaluation — see Section A, Q5).
- The full version of this template (inside the Section C project) also
  adds an `{% if profile.is_public %}` branch to toggle visibility per
  profile — that conditional-logic piece is covered in **Section A, Q4**
  and demonstrated in `social_profile_manager/profiles/templates/profiles/profile_list.html`.

---

## Where This Connects to Section C

Section C's mini project doesn't reimplement these four tasks — it takes
this exact code and:
- Points it at a real PostgreSQL/MySQL database instead of treating it as
  an isolated snippet (`config/settings.py`)
- Adds a CSV export view using a context manager (`profile_export_csv`)
- Wires everything into named URL routes (`profiles/urls.py`)
- Extends the "Create" form into a reusable "Create/Edit" form (`profile_edit`)

See `Section_C_Mini_Project` (the `social_profile_manager.zip` project) for
the fully working, integrated version of all of the above.
