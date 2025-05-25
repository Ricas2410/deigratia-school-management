from django import forms
from django.core.validators import RegexValidator
from .models import Application


class ApplicationForm(forms.ModelForm):
    """Student application form"""
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    parent_phone = forms.CharField(validators=[phone_regex], max_length=17)
    
    class Meta:
        model = Application
        fields = [
            'student_name', 'date_of_birth', 'grade_applying_for',
            'parent_name', 'parent_email', 'parent_phone', 'address',
            'previous_school', 'special_needs', 'additional_info',
            'birth_certificate', 'previous_report'
        ]
        
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student full name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'grade_applying_for': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Select Grade'),
                ('nursery', 'Nursery'),
                ('pre-k', 'Pre-K'),
                ('kindergarten', 'Kindergarten'),
                ('grade-1', 'Grade 1'),
                ('grade-2', 'Grade 2'),
                ('grade-3', 'Grade 3'),
                ('grade-4', 'Grade 4'),
                ('grade-5', 'Grade 5'),
                ('grade-6', 'Grade 6'),
            ]),
            'parent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter parent/guardian full name'
            }),
            'parent_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'previous_school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter previous school name (if any)'
            }),
            'special_needs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Please describe any special needs or accommodations required'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional information you would like to share'
            }),
            'birth_certificate': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'previous_report': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }
        
        labels = {
            'student_name': 'Student Full Name',
            'date_of_birth': 'Date of Birth',
            'grade_applying_for': 'Grade Applying For',
            'parent_name': 'Parent/Guardian Name',
            'parent_email': 'Email Address',
            'parent_phone': 'Phone Number',
            'address': 'Home Address',
            'previous_school': 'Previous School (Optional)',
            'special_needs': 'Special Needs/Accommodations (Optional)',
            'additional_info': 'Additional Information (Optional)',
            'birth_certificate': 'Birth Certificate (Optional)',
            'previous_report': 'Previous School Report (Optional)',
        }


class ContactForm(forms.Form):
    """Contact form"""
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number (optional)'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject of your message'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message'
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.split()) < 2:
            raise forms.ValidationError('Please enter your full name.')
        return name
