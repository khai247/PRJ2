from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class StudentImageForm(forms.ModelForm):
    images = MultipleFileField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = StudentImage
        fields = ['images']

class FormSettings(forms.ModelForm):
    # Define a custom form class named FormSettings that inherits from forms.ModelForm.

    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Initialize the form class and handle any parent class initialization.

        for field in self.visible_fields():
            # Iterate over all visible fields in the form.
            field.field.widget.attrs['class'] = 'custom-input'
            # Add the CSS class 'custom-input' to the widget's attributes.

class CustomUserForm(FormSettings):
    # Define a custom form class named CustomUserForm that inherits from FormSettings.
    email = forms.EmailField(required=True)
    # Define an email field that is required.
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    # Define a choice field for gender with options 'Male' and 'Female'.
    first_name = forms.CharField(required=True)
    # Define a required field for the user's first name.
    last_name = forms.CharField(required=True)
    # Define a required field for the user's last name.
    password = forms.CharField(widget=forms.PasswordInput)
    # Define a password field with a PasswordInput widget for secure input.
    widget = {
        'password': forms.PasswordInput(),
    }
    # Customize the widget for the password field to use PasswordInput.


    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        # Initialize the form class and handle any parent class initialization.

        if kwargs.get('instance'):
            # Check if an instance (user) is provided for updating existing user data.
            instance = kwargs.get('instance').admin.__dict__
            # Get the instance's data as a dictionary.
            self.fields['password'].required = False
            # Mark the password field as not required for updating existing users.
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
                # Set the initial values for specified fields based on the instance data.
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
                # Add a placeholder text to the password field for updating the password.

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        # Get the cleaned and lowercased value of the email field.
        if self.instance.pk is None:  # Insert
            # If it's a new user being inserted:
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError("The given email is already registered")
                # Check if the email already exists in the database and raise a validation error if it does.
        else:  # Update
            # If it's an existing user being updated:
            dbEmail = self.Meta.model.objects.get(id=self.instance.pk).admin.email.lower()
            # Get the existing user's email from the database.
            if dbEmail != formEmail:  # There has been changes
                # If the email has been changed:
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")
                    # Check if the new email already exists in the database and raise a validation error if it does.

        return formEmail
        # Return the cleaned and lowercased email value.

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password']
        # Define the model (presumably a CustomUser model) and specify the fields to include in the form.

class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + ['student_id']
            
class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields 

class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['staff_id']

class ClazzForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(ClazzForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Clazz
        fields = ['name', 'clazz_id', 'semester', 'teacher', 'place', 'schedule']

# class SessionForm(FormSettings):
#     def __init__(self, *args, **kwargs):
#         super(SessionForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = Session
#         fields = '__all__'
#         widgets = {
#             'start_year': DateInput(attrs={'type': 'date'}),
#             'end_year': DateInput(attrs={'type': 'date'})
#         }

class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields 


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields
