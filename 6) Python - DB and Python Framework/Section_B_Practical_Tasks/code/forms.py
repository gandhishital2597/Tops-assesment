"""
Section B - Task 2: Create ModelForm & Validation

UserProfileForm extends forms.ModelForm, which auto-generates form fields
directly from UserProfile's model fields (Section A, Q3: this is how Django
Forms give "automated" validation for free — CharField already rejects
overly long strings, IntegerField already rejects non-numeric input, etc.).

clean_age() adds a CUSTOM constraint on top of that automatic validation:
the model only knows age is an integer, but the business rule "must be over
13" is enforced here, at the form layer.
"""

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
        Custom field-level validator.

        Django automatically calls clean_<fieldname>() for any field that
        has one defined, after the field's default validation has already
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
        Extra validation for usernames (Section A, Q3) - reject blank or
        whitespace-only usernames even though CharField alone wouldn't
        catch a string of just spaces.
        """
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError("Username cannot be blank.")
        return username
