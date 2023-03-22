from django.db import models
from multiselectfield import MultiSelectField


# Create your models here.
class Candidate(models.Model):

    JOB = [
        ('', 'Select a job'),
        ('Full-Stack', 'Full-Stack'),
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend')
    ]

    SITUATION = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    PERSONALITY = [
        ('','Select a personality'),
        ('I am outgoing', 'I am outgoing'),
        ('I am sociable', 'I am sociable'),
        ('I am antisocial', 'I am antisocial'),
        ('I am serious', 'I am serious')
    ]

    SMOKER = [
        ('1', 'Yes'),
        ('2', 'No'),
    ]

    FRAMEWORKS = [
        ('Laravel', 'Laravel'),
        ('Angular', 'Angular'),
        ('Django', 'Django'),
        ('Flask', 'Flask'),
        ('Vue', 'Vue'),
        ('Others', 'Others'),
    ]

    LANGUAGES = [
        ('Python', 'Python'),
        ('Javascript', 'Javascript'),
        ('Java', 'Java'),
        ('C++', 'C++'),
        ('Ruby', 'Ruby'),
        ('Others', 'Others'),
    ]

    DATABASES = [
        ('MySql', 'MySql'),
        ('Postgre', 'Postgre'),
        ('MongoDB', 'MongoDB'),
        ('SqLite3', 'SqLite3'),
        ('Oracle', 'Oracle'),
        ('Others', 'Others'),
    ]
    LIBRARIES = [
        ('Ajax', 'Ajax'),
        ('Jquery', 'Jquery'),
        ('React.js', 'React.js'),
        ('Chart.js', 'Chart.js'),
        ('Gsap', 'Gsap'),
        ('Others', 'Others'),
    ]

    MOBILE = [
        ('React native', 'React native'),
        ('Kivy', 'Kivy'),
        ('Flutter', 'Flutter'),
        ('Ionic', 'Ionic'),
        ('Xamarin', 'Xamarin'),
        ('Others', 'Others'),
    ]

    OTHERS = [
        ('UML', 'UML'),
        ('SQL', 'SQL'),
        ('Docker', 'Docker'),
        ('GIT', 'GIT'),
        ('GraphQL', 'GraphQL'),
        ('Others', 'Others'),
    ]

    # EDUCATION
    STATUS_COURSE = [
        ('', 'Select your status'),
        ("I'm studying", "I'm studying"),
        ('I took a break', 'I took a break'),
        ('Completed', 'Completed'),
    ]

    # SALARY
    SALARY = [
        ('', 'Salary expectation (month)'),
        ('Between (3 Lakhs and 4 Lakhs)', 'Between (3 Lakhs and 4 Lakhs)'),
        ('Between (4 Lakhs and 5 Lakhs)', 'Between (4 Lakhs and 5 Lakhs)'),
        ('Between (5 Lakhs and 7 Lakhs)', 'Between (5 Lakhs and 7 Lakhs)'),
        ('Between (7 Lakhs and 10 Lakhs)', 'Between (7 Lakhs and 10 Lakhs)')
    ]

    # GENDER
    GENDER = [('M', 'Male'), ('F', 'Female')]


    # PERSONAL (Card1)
    firstname= models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    job =  models.CharField(max_length=50, verbose_name='Job type', null=True, choices=JOB)
    #age = models.CharField(max_length=3)
    birth = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Birthday")
    phone = models.CharField(max_length=25)
    personality = models.CharField(max_length=50, null=True, choices=PERSONALITY)
    salary = models.CharField(max_length=50, choices=SALARY, verbose_name='Salary expectation')
    gender = models.CharField(max_length=6, choices=GENDER, default='')
    experience = models.BooleanField(null=True)
    smoker = models.CharField(max_length=10, null=True, choices=SMOKER, default='')
    email = models.EmailField(max_length=254) 
    message = models.TextField(verbose_name='Presentation')
    files = models.FileField(upload_to='resume', blank=True, verbose_name='Resume')
    # 'upload_to' to make folder in Media folder 
    image = models.ImageField(upload_to='photo', blank=True, verbose_name='Photo')
    created_at = models.DateTimeField(auto_now_add=True)
    Situation = models.CharField(max_length=50, null=True, choices=SITUATION, default='Pending')
    company_note = models.TextField(blank=True)
    
    # Skills (Card2)
    frameworks = MultiSelectField(max_length=50, choices=FRAMEWORKS, default="")
    languages = MultiSelectField(max_length=50, choices=LANGUAGES, default="")
    databases = MultiSelectField(max_length=50, choices=DATABASES, default="")
    libraries = MultiSelectField(max_length=50, choices=LIBRARIES, default="")
    mobile = MultiSelectField(max_length=50, choices=MOBILE, default="")
    others = MultiSelectField(max_length=50, choices=OTHERS, default="")

    # EDUCATION (Card3)
    institution = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    started_course = models.DateField(null=True, blank=True, auto_now_add=False)
    finished_course = models.DateField(null=True, blank=True, auto_now_add=False)
    about_course = models.TextField()
    status_course = models.CharField(max_length=50, null=True, choices=STATUS_COURSE)

    # PROFESSIONAL (Card4)
    company = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    started_job = models.DateField(null=True, blank=True, auto_now_add=False)
    finished_job = models.DateField(null=True, blank=True,auto_now_add=False)
    about_job = models.TextField()
    employed = models.BooleanField(null=True, verbose_name="I'm employed")
    remote = models.BooleanField(null=True, verbose_name="I agree to work remotely")
    travel = models.BooleanField(null=True, verbose_name="I'm available for travel")

    #Capitalize (F-name and L-name)
    def clean(self):
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        self.email = self.email.lower()


    # Concatenate F-name and L-name (Admin Table)
    def name(obj):
        return "%s %s" % (obj.firstname, obj.lastname)

    # Concatenate (when clicking over the candidates)
    def __str__(self):
        # return self.firstname + ' ' + self.lastname
        return f"{self.firstname} {self.lastname}" 


# ================= Send Email ========================
class Email(models.Model):
    #hidden
    employee = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    status = models.CharField(max_length=50)
    # Not hidden
    subject = models.CharField(max_length=50)
    message = models.TextField()
     # Get Datetime the email was send
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
