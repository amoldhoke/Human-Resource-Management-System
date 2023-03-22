from rest_framework import serializers
from Management.models import Candidate, Email
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from datetime import date
import datetime # Used to prevent future date
from django.utils import timezone


# Candidate List
class CandidateFilterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id','email', 'phone', 'gender', 'job', 'experience', 'created_at']

# --------------------------------------------------------------------------------------------
# FOR Detail List and Control
class CandidateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        exclude = ['created_at','Situation'] 

# --------------------------------------------------------------------------------------------

# Email
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id','Situation']

    def to_representation(self, instance):
        if instance.Situation == 'Approved':
            return super().to_representation(instance)
        else:
            return {}

# ---------------------------------------------------------------------------------
# Validation for job, personality, salary, status_course
def empty_field(value):
    if value == '':
        raise serializers.ValidationError('Please select an option.')

# Candidate (Create, Retrieve, Destroy)
class RegisterSerializer(serializers.ModelSerializer):
# PERSONAL
    # First name
    firstname = serializers.CharField(
        min_length=3, 
        max_length=50, 
        label='First name',
        required=True,
        validators=[RegexValidator(
            regex=r'^[A-Za-z]+$',
            message="First name can only contain letters."
            )], 
        error_messages={'blank': 'Please enter your first name.'},      
    )

    # Last name
    lastname = serializers.CharField(
        min_length=3, 
        max_length=50, 
        label='Last name',
        required=True,
        validators=[RegexValidator(
            regex=r'^[A-Za-z]+$',
            message="Last name can only contain letters."
            )], 
        error_messages={'blank': 'Please enter your last name.'},      
    )

    # Job
    job = serializers.ChoiceField(
        label='Job type',
        choices=Candidate.JOB,
        validators=[empty_field],
        required=True,
    )

    # Email
    email = serializers.EmailField(
        label='Email address',
        min_length=3, 
        max_length=50, 
        required=True,
        validators=[UniqueValidator(queryset=Candidate.objects.only('email'), 
                    message='A user with this email already exists!')],
        error_messages={'blank': 'Email cannot be empty !'},
    )

    # Birthday
    birth = serializers.DateField(
        label='Birthdate',
        error_messages={
            'invalid': 'Please enter your birth date.'
        }
    )

    # Phone number
    phone = serializers.CharField(
        min_length=10, 
        max_length=12, 
        required=True,
        error_messages={'blank': 'Please enter your phone number.', 
                        'min_length': 'Phone field is incomplete'},
    )

    # Personality
    personality = serializers.ChoiceField(
        choices=Candidate.PERSONALITY,
        validators=[empty_field],
        required=True,
    )

    # Salary expectation
    salary = serializers.ChoiceField(
        label = 'Salary expectation',
        choices=Candidate.SALARY,
        validators=[empty_field],
        required=True,
    )

    # Gender
    gender = serializers.ChoiceField(
        choices=Candidate.GENDER,
        style={'base_template': 'radio.html'},
        required=True,
        error_messages={'required': 'Please select a gender.'},
    )

    # If candidate is smoker
    smoker = serializers.ChoiceField(
        choices=Candidate.SMOKER,
        style={'base_template': 'radio.html'},
        required=True,
        error_messages={'required': 'Please select an option.'},
    )

    # Experience
    experience = serializers.BooleanField(
        label='I have experience', 
        required= False,
    )

    # Message
    message = serializers.CharField(
        label="About you", 
        min_length=5, 
        max_length=5000, 
        required=False,
    )

    # File (Upload resume)
    files = serializers.FileField(
        label='Resume',
        allow_empty_file=False,
        error_messages={'invalid':'Please select a file to upload.'},
        required=True,
    )

    # Image (Upload Photo)
    image = serializers.ImageField(
        label='Photo', 
        allow_empty_file=False,
        error_messages={'invalid':'Please select a image to upload.', 'invalid_image':'Only: .png - .jpeg - .jpg'},
        required=True,
    )

#----------------------------------------------------------------------------------------------
# SKILLS
  
    frameworks = serializers.MultipleChoiceField(
        label='frameworks', 
        choices=Candidate.FRAMEWORKS,
        required= True,
    )

    languages = serializers.MultipleChoiceField(
        label='languages',
        choices=Candidate.LANGUAGES,
        required= True,
    )

    databases = serializers.MultipleChoiceField(
        label='databases', 
        choices=Candidate.DATABASES,
        required= True,
    )

    libraries = serializers.MultipleChoiceField(
        label='libraries', 
        choices=Candidate.LIBRARIES,
        required= True,
    )

    mobile = serializers.MultipleChoiceField(
        label='mobile', 
        choices=Candidate.MOBILE,
        required= True,
    )

    others = serializers.MultipleChoiceField(
        label='others', 
        choices=Candidate.OTHERS,
        error_messages={'invalid_choice': 'Please enter your phone number.'},
        required= True,
    )

# ---------------------------------------------------------------------------------------------
# EDUCATION

    # Institution
    institution = serializers.CharField(
        min_length=3, 
        max_length=50,       
        label='Institution', 
        error_messages={'blank':'Please enter the name of your institution.'},
        required=True,
    )

    # About course
    course = serializers.CharField(
        min_length=3, 
        max_length=50,   
        error_messages={'blank':'Please enter your course.'},
        required=True,
    )

    # Course started
    started_course = serializers.DateField(
        error_messages={
            'invalid': 'Please enter a valid date.'
        },
        required=True,
    )

    # About college course
    about_course = serializers.CharField(
        label="About you college course", 
        min_length=5, 
        max_length=5000,
        error_messages={'blank':'Please provide information about your college course.'},
        required=True,
    )

    # Status course
    status_course = serializers.ChoiceField(
        label='Status course',
        choices=Candidate.STATUS_COURSE,
        validators=[empty_field],
        required=True,
    )

# ---------------------------------------------------------------------------------------------
# PROFESSIONAL

    # Company (Last company)
    company = serializers.CharField(
        label= 'Last company',
        min_length=3,
        max_length=50,
        required=False,
    )

    # Position (Occupation)
    position = serializers.CharField(
        min_length=3,
        max_length=50, 
        required=False,
    )


    # About job
    about_job = serializers.CharField(
        label="About your last job", 
        min_length=5, 
        max_length=5000,
        required=False,
    )

    # Employed
    employed = serializers.BooleanField(
        label="I'm employed", 
        required=False,
    )

    # Remote
    remote = serializers.BooleanField(label="I agree to work remotely", required=False)
    # Able to travel?
    travel = serializers.BooleanField(label="I'm available for travel", required=False)
     
    class Meta:
        model = Candidate
        fields = [
            "firstname",
            "lastname",
            "job",
            "email",
            "birth",
            "phone",
            "personality",
            "salary",
            "gender",
            "smoker",
            "experience",
            "message",
            "files",
            "image",
            "frameworks",
            "languages",
            "databases",
            "libraries",
            "mobile",
            "others",
            "institution",
            "course",
            "started_course",
            "finished_course",
            "about_course",
            "status_course",
            "company",
            "position",
            "started_job",
            "finished_job",
            "about_job",
            "employed",
            "remote",
            "travel"
            ]

    # 1) CONVERSION
    def create(self, validated_data):
        validated_data['firstname'] = validated_data['firstname'].capitalize()  # Convert to capitalize
        validated_data['lastname'] = validated_data['lastname'].capitalize()  # Convert to capitalize
        validated_data['email'] = validated_data['email'].lower()  # Convert email to lower case
        return super().create(validated_data)

    # 2) PHONE (Prevent incomplete values)
    def validate_phone(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError('Please provide a valid phone number.')
        return value

    # 3) RESTRICTION (file extensions- if statement + upload size control)
    def validate_files(self, value):
        # Variable
        EXT = ['pdf', 'doc', 'docx', 'csv', 'xlsx']
        ext = str(value).split('.')[-1]
        type = ext.lower()
        # Statement
        # a) Accept only pdf - doc - docx
        if type not in EXT:
            raise serializers.ValidationError('Only: PDF - DOC - DOCX')
        # b) Prevent upload more than 2mb
        if value.size > 2 * 1048476:
            raise serializers.ValidationError('Denied ! Maximum allowed is 2mb.')
        return value

    # 4) IMAGE (Maximum upload size = 2mb)
    def validate_image(self, value):
        if value.size > 2 * 1048476:
            raise serializers.ValidationError('Denied ! Maximum allowed is 2mb.')
        return value

    # 5) BIRTHDAY (Range: 18 and 65)
    def validate_birth(self, value):
        #Variable
        b = value
        now = date.today()
        age = (now.year - b.year) - ((now.month, now.day) < (b.month, b.day))
        # Statement
        if age < 18 or age > 65:
            raise serializers.ValidationError('Denied ! Age must be between 18 and 65.')
        return value

    # 6) PREVENT FUTURE DATES
    # a) Started course
    def validate_started_course(self, value):
        if value != None and value > datetime.date.today():
            raise serializers.ValidationError('Future dates is invalid.')
        return value

    # b) Started job
    def validate_started_job(self, value):
        if value != None and value > timezone.now().date():
            raise serializers.ValidationError('Future dates is invalid.')
        else:
            return value

