from django import forms
from Management.models import Candidate, Email
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
import datetime # Used to prevent future date
from django.utils import timezone

#---------------------------------------------------------------------------------------------

# Capitalize using form.py
# Every Letters to Lowercase
class Lowercase(forms.CharField):
    def to_python(self, value):
        return value.lower()

#---------------------------------------------------------------------------------------------

class CandidateForm(forms.ModelForm):

    # Static files
    class Media:
        js = ('js/script.js',)

    # First name
    firstname = forms.CharField(
        label="First Name",
        min_length=3, 
        max_length=50, 
        validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', 
        message="Only letters is allowed !")],
        error_messages={'required':'Please enter your first name.'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'style': 'font-size: 13px; text-transform: capitalize',
                }
            )
        )

    # Last name
    lastname = forms.CharField(
        label="Last Name", 
        min_length=3, 
        max_length=50, 
        validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', 
        message="Only letters is allowed !")],
        error_messages={'required':'Please enter your last name.'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'style': 'font-size: 13px; text-transform: capitalize',
                }
            )
        )


    # Created Function at starting name Lowercase
    # Email always in Lowercase
    email = Lowercase(
        label="Email address", 
        min_length=3, 
        max_length=50, 
        validators=[RegexValidator(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', 
        message="Please enter a valid email address !")],
        error_messages={'required':'Email cannot be empty !'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'style': 'font-size: 13px; text-transform: lowercase',
                #'autocomplete':'off',
                }
            )
        )


     # Experience
    experience = forms.BooleanField(
        label='I have experience', 
        required= False,
        widget=forms.CheckboxInput(
            attrs={
                'id':'emp'
            }
        )
    )

    # Message
    message = forms.CharField(
        label="About you", 
        min_length=5, 
        max_length=5000, 
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Talk a little about you', 
                'rows':3,
                'style': 'font-size: 13px',
                }
            )
        )
    
    # File (Upload resume)
    files = forms.FileField(
        error_messages={'required':'Please select a file to upload.'},
        label='Resume',
        widget=forms.ClearableFileInput(
            attrs={
                'style':'font-size: 13px',
            }
        )
    )

    # Image (Upload Photo)
    image = forms.ImageField(
        error_messages={'required':'Please select a image to upload.'},
        label='Photo',
        widget=forms.ClearableFileInput(
            attrs={
                'style':'font-size: 13px',
                'accept': 'image/png, image/jpeg',
            }
        )
    )

    # Institution
    institution = forms.CharField(
        error_messages={'required':'Please enter the name of your institution.'},
        label='Institution', 
        min_length=3, 
        max_length=50, 
        widget=forms.TextInput(
            attrs={
                'style':'font-size: 13px', 
                'placeholder':'Institution name'
                }
            )
        )

    # About course
    course = forms.CharField(
        error_messages={'required':'Please enter your course.'},
        min_length=3, 
        max_length=50, 
        widget=forms.TextInput(
            attrs={
                'style':'font-size: 13px', 
                'placeholder':'Your college course'
                }
            )
        )

    # Finished Course
    finished_course = forms.DateTimeField(
        required=False,
        disabled=True,
        widget=forms.DateTimeInput(attrs={
            'style':'font-size: 13px; cursor:pointer',
            'type':'date',
            'min': '1950-01-01',
            'max': '2050-01-01',
        })
    )

    # About college course
    about_course = forms.CharField(
        error_messages={'required':'Please provide information about your college course.'},
        label="About you college course", 
        min_length=5, 
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us about your college course...', 
                'rows':3,
                'style': 'font-size: 13px',
                }
            )
        )

    # About job
    about_job = forms.CharField(
        required=False,
        label="About your last job", 
        min_length=5, 
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us a little about what you did at the company...', 
                'rows':3,
                'style': 'font-size: 13px',
                'class':'emp'  # script in script.js
                }
            )
        )

    # Company (Last company)
    company = forms.CharField(
        required=False,
        label= 'Last company',
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder':'Company name',
            'style': 'font-size: 13px',
            'class':'emp'  # script in script.js
            }
        )
    )
    # Position (Occupation)
    position = forms.CharField(
        required=False,
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder':'Your occupation',
            'style': 'font-size: 13px',
            'class':'emp'  # script in script.js
            }
        )
    )

    # Started job
    started_job = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'style':'font-size: 13px; cursor:pointer',
            'type':'date',
            'min': '1950-01-01',
            'max': '2050-01-01',
            'class':'emp',  # script in script.js
        })
    )

    # Finished job
    finished_job = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'style':'font-size: 13px; cursor:pointer',
            'type':'date',
            'min': '1950-01-01',
            'max': '2050-01-01',
            'class':'emp',  # script in script.js
            'id':'go'
        })
    )

    # Employed
    employed = forms.BooleanField(
        label="I'm employed", 
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id':'exp',
            'class':'emp'
        })
    )

    # Remote
    remote = forms.BooleanField(label="I agree to work remotely", required=False)
    # Able to travel?
    travel = forms.BooleanField(label="I'm available for travel", required=False)


    class Meta:
        model = Candidate
        exclude = ['created_at', 'Situation'] 

        SALARY = (
            ('', 'Salary expectation (month)'),
            ('Between (3 Lakhs and 4 Lakhs)', 'Between (3 Lakhs and 4 Lakhs)'),
            ('Between (4 Lakhs and 5 Lakhs)', 'Between (4 Lakhs and 5 Lakhs)'),
            ('Between (5 Lakhs and 7 Lakhs)', 'Between (5 Lakhs and 7 Lakhs)'),
            ('Between (7 Lakhs and 10 Lakhs)', 'Between (7 Lakhs and 10 Lakhs)')
        )

        # GENDER
        GENDER = [('M', 'Male'), ('F', 'Female')]

#----------------------------------------------------------------------------------------------
        # Outside Widget
        widgets = {
            # Birth date
            'birth':forms.DateInput(
                attrs={
                    'style':'font-size: 13px; cursor:pointer',
                    'type':'date',
                    'min': '1950-01-01',
                    'max': '2050-01-01'
                }    
            ),

            # Stated course
            'started_course':forms.DateInput(
                attrs={
                    'style':'font-size: 13px; cursor:pointer',
                    'type':'date',
                    'min': '1950-01-01',
                    'max': '2050-01-01'
                }    
            ),

            # PHONE
            'phone': forms.TextInput(
                attrs={
                    'style':'font-size: 13px', 
                    'placeholder':'Phone',
                    'data-mask': '00000-00000'  # Jquery masking
                }
            ),

            # SALARY
            'salary': forms.Select(
                choices=SALARY,
                attrs={
                    'class':'form-control',  
                    'style': 'font-size: 13px',
                }
            ),

            # JOB Code
            'job': forms.Select(attrs={'style': 'font-size: 13px'}),
            
            # GENDER
            'gender': forms.RadioSelect(choices=GENDER, attrs={'class': 'btn-check'}),

            # SMOKER
            'smoker': forms.RadioSelect(attrs={'class': 'btn-check'}),

            # PERSONALITY
            'personality': forms.Select(attrs={'style': 'font-size: 13px'}),

            # Status Course
            'status_course': forms.Select(attrs={
                'style': 'font-size: 13px',
                'onChange':'statusCourse(this)'
                }),
    }

#----------------------------------------------------------------------------------------------
        error_messages = {
            # Job Code
            'job': {'required': 'Please select an option.'},
            # Birth Date
            'birth': {'required': 'Please enter your birth date.'},
            # Phone
            'phone': {'required': 'Please enter a valid phone number.'},
            # Personality
            'personality': {'required': 'Please select an option.'},
            # Salary
            'salary': {'required': 'Please select an option.'},
            # Gender
            'gender': {'required': 'Please select a gender.'},
            # Status Course
            'status_course': {'required': 'Please select an option.'},
            
    }

#----------------------------------------------------------------------------------------------
    # SUPER FUNCTION (AKA Global Function)
    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs) 

    # ========== FUNCTION TO PREVENT DUPLICATED ENTRIES ==============|

    # 1) Email (if statement w/ filter)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Candidate.objects.filter(email = email).exists():
            raise forms.ValidationError(f'Denied ! {email} is already registerd')
        return email


    # 2) AGE (Range: 18 - 65)
    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < '18' or age > '65':
            raise forms.ValidationError('Denied ! Age must be between 18 and 65.')
        return age

    # 3) PHONE (Prevent incomplete values)
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11:
            raise forms.ValidationError('Phone field is incomplete')
        return phone


    # 4) RESTRICTION (file extensions- if statement + upload size control)
    def clean_files(self):
        # Get date
        files = self.cleaned_data.get('files', False)
        # Variable
        EXT = ['pdf', 'doc', 'docx', 'csv', 'xlsx']
        ext = str(files).split('.')[-1]
        type = ext.lower()
        # Statement
        # a) Accept only pdf - doc - docx
        if type not in EXT:
            raise forms.ValidationError('Only: PDF - DOC - DOCX')
        # b) Prevent upload more than 2mb
        if files.size > 2 * 1048476:
            raise forms.ValidationError('Denied ! Maximum allowed is 2mb.')
        return files

    # 5) IMAGE (Maximum upload size = 2mb)
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image.size > 2 * 1048476:
            raise forms.ValidationError('Denied ! Maximum allowed is 2mb.')
        return image

    # 6) BIRTHDAY (Range: 18 and 65)
    def clean_birth(self):
        birth = self.cleaned_data.get('birth')
        #Variable
        b = birth
        now = date.today()
        age = (now.year - b.year) - ((now.month, now.day) < (b.month, b.day))
        # Statement
        if age < 18 or age > 65:
            raise forms.ValidationError('Denied ! Age must be between 18 and 65.')
        return birth

    # 7) PREVENT FUTURE DATES
    # a) Started course
    def clean_started_course(self):
        started_course = self.cleaned_data.get('started_course')
        if started_course == None:
            raise forms.ValidationError('Please enter a valid date.')
        elif started_course != None and started_course > datetime.date.today():
            raise forms.ValidationError('Future dates is invalid.')
        return started_course

    # b) Started job
    def clean_started_job(self):
        started_job = self.cleaned_data['started_job']
        if started_job != None and started_job.date() > timezone.now().date():
            raise forms.ValidationError('Future dates is invalid.')
        else:
            return started_job


# ======================== SEND EMAIL TO CANDIDATES ======================

class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget= forms.Textarea)
    class Meta:
        fields = "__all__"




    





    
    