from django.contrib import admin
from Management.models import Candidate, Email
from Management.forms import CandidateForm
from django.utils.html import format_html

# Register your models here

class CandidateAdmin(admin.ModelAdmin):
    # 1) Make adio button Horizontal or Vertical(when clicking over the candidates)
    radio_fields = {'smoker': admin.HORIZONTAL}

#---------------------------------------------------------------------------------------------

    # 2) Change admin panel into form.py
    form = CandidateForm 

#---------------------------------------------------------------------------------------------                            
    # 3) Change admin panel into readonly field
    readonly_fields = ['experience', 'gender', 'firstname', 'lastname', 'job', 'email', 'phone', 'salary', 'birth', 'personality', 'smoker', 'files', 'image', 'frameworks', 'languages', 'databases', 'libraries', 'mobile', 'others', 'message', 'status_course', 'started_course', 'finished_course', 'course', 'institution', 'about_course', 'started_job', 'finished_job', 'company', 'position', 'about_job', 'employed', 'remote', 'travel', ]

#---------------------------------------------------------------------------------------------

    # 4) Add if readonly addes to admin panel 
    exclude = ['status']  

#---------------------------------------------------------------------------------------------

    # 5) Add filter to Admin panel
    list_filter = ['Situation']

#---------------------------------------------------------------------------------------------

    # 6) Display what field is to show
    # 'name' concatenate added, check model.py
    list_display = ['name', 'job', 'email',  'created_at', 'status', '_' ]

#---------------------------------------------------------------------------------------------

    # 7) Add search field to admin panel
    search_fields = ['firstname', 'lastname', 'email','Situation']

#---------------------------------------------------------------------------------------------

    # 8) Set how many fields per page
    list_per_page = 10

#---------------------------------------------------------------------------------------------

    # 9) FIELDSET
    fieldsets = [
        # HR Operations
        ("HR OPERATIONS", {"fields": ['Situation', 'company_note']}),
        # Personal
        ("PERSONAL", {"fields": ['experience', 'gender', 'job', 'email', 'phone', 'salary', 'birth', 'personality', 'smoker', 'files', 'image', 'message']}),
        # Skills
        ("SKILLS", {"fields": ['frameworks', 'languages', 'databases', 'libraries', 'mobile', 'others']}),
        # Educational
        ("EDUCATIONAL", {"fields": ['status_course', 'started_course', 'finished_course', 'institution', 'course', 'about_course']}),
        # Professional
        ("PROFESSIONAL", {"fields": ['started_job', 'finished_job', 'company', 'position', 'about_job']}),
        # Note
        ("NOTE", {"fields": ['employed', 'remote', 'travel']}),
    ]

#---------------------------------------------------------------------------------------------

    # 10) Function to change the icons
    # Note:Argument cannot be empty, that's the reason I put this ->(_)
    def _(self, obj):
        if obj.Situation == 'Approved':
            return True
        elif obj.Situation == 'Pending':
            return None
        else:
            return False
    _.boolean = True

#---------------------------------------------------------------------------------------------

    # 11) Function to color the text
    def status(self, obj):
        if obj.Situation == 'Approved':
            color = '#28a745'
        elif obj.Situation == 'Pending':
            color = '#fea95e'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}<p><strong>'.format(color, obj.Situation))
    status.allow_tags = True

#---------------------------------------------------------------------------------------------

admin.site.register(Candidate, CandidateAdmin)

# ============================= SEND EMAIL ===============================

class EmailAdmin(admin.ModelAdmin):
    readonly_fields = ('employee', 'sent_on','status', 'name', 'email', 'subject', 'message')
    list_display = ['name', 'email', 'subject', '_status', 'sent_on']
    search_fields = ['name', 'email', 'subject']
    list_filter = ['status']
    list_per_page = 10

    # 9) FIELDSET
    fieldsets = [
        # Informative 
        ("INFORMATIVE DATA", {"fields": ['email', 'status']}),
        # Email content
        ("EMAIL CONTENT", {"fields": ['subject', 'message']}),
        # Registration
        ("REGISTRATION", {"fields": ['employee', 'sent_on']}),
    ]

    # Due to same status in above field there is confilt so i add '_status'
    def _status(self, obj):
        if obj.status == 'Approved':
            color = '#28a745'
        elif obj.status == 'Pending':
            color = '#fea95e'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}<p><strong>'.format(color, obj.status))
    _status.allow_tags = True

admin.site.register(Email, EmailAdmin)

