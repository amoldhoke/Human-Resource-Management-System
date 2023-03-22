from django.shortcuts import render
from .forms import CandidateForm, EmailForm
from .models import Candidate, Email
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Login required to access private pages.
from django.views.decorators.cache import cache_control # Destroy the section after log out
from django.core.paginator import Paginator
from django.db.models import Q
# Concatenate (F-name and L-name)
from django.db.models.functions import Concat 
from django.db.models import Value as P #(P = Plus)
# Export to PDF
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
import os
# Send email
from django.core.mail import EmailMessage

# ============================== FRONTEND ================================|
# HOME
def home(request):
    return render(request, "home.html")

# Candidate registration
def register(request):
    if request.method =='POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Form sent Successfully !")
            return HttpResponseRedirect('/')
        else:
            return render(request, "register.html", {'form':form})
    else:
        form = CandidateForm()
    return render(request, "register.html", {'form':form})

#==================================== BACKEND ==============================|
# HR - Home page (backend)
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    # Filter
    if 'f' in request.GET:
        f = request.GET['f']
        all_candidate_list = Candidate.objects.filter(Q(job__iexact=f) | Q(gender__iexact=f)).order_by('-created_at')
        
    # Filter
    elif 'q' in request.GET:
        q = request.GET['q']
        all_candidate_list = Candidate.objects.annotate(
            name=Concat('firstname', P(' '), 'lastname')).\
        filter(Q(name__icontains=q) | Q(firstname__icontains=q) | Q(lastname__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q)).order_by('-created_at')
    # Else
    else:
        all_candidate_list = Candidate.objects.all().order_by('-created_at')
    # Pagination
    paginator = Paginator(all_candidate_list, 10)
    page = request.GET.get('page')
    all_candidate = paginator.get_page(page)
    # Counters
    total = all_candidate_list.all().count()
    frontend = all_candidate_list.filter(job='Frontend')
    backend = all_candidate_list.filter(job='Backend').count()
    fullstack = all_candidate_list.filter(job='Full-Stack').count()
    # Context
    context = {
        'candidates':all_candidate,
        'total':total,
        'frontend':frontend,
        'backend':backend,
        'fullstack':fullstack,
        }
    return render(request, "backend.html", context)

# Access candidate (individually)
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def candidate(request, id):
    candidate = Candidate.objects.get(pk=id)
    return render(request, 'candidate.html',{'candidate':candidate})

# Delete
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete(request, id):
    candidate = Candidate.objects.get(pk = id)
    candidate.delete()
    messages.success(request, "Candidate deleted successfully !")
    return HttpResponseRedirect('/backend')


#=============================Export to PDF ==============================|
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request, id):
    candidate = Candidate.objects.get(id=id)
    pdf_name =candidate.firstname + ' ' + candidate.lastname + '.pdf'

    # get the current user
    user = request.user

    # create the context dictionary with the candidate object
    context = {'candidate': candidate, 'user': user}

    # get the template and render it with the context
    template = get_template('pdf.html')
    html = template.render(context)

    # create the PDF file with CSS included
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8', link_callback=fetch_resources)

 # check if the PDF file was created successfully
    if not pdf.err:
        # return the PDF file
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(pdf_name)
        return response

    # return an error message if the PDF file could not be created
    return HttpResponse('Error generating PDF file')

# function to fetch external resources such as CSS files
def fetch_resources(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):    
        raise Exception( 'media URI must start with %s or %s' % (sUrl, mUrl))

    return path

# Template PDF
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pdf(request, id):
    candidate = Candidate.objects.get(pk=id)
    return render(request, "pdf.html", {'candidate':candidate})

# ============================ Send Email =======================================
def email(request):
    if request.method == "POST":
        # Save the message in DB (No ModelForm)
        to_db = Email(
            employee = request.POST.get('employee'),
            status = request.POST.get('status'),
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        to_db.save()

        # ModelForm
        form = EmailForm(request.POST)
        # Company subject
        company = "PINNACA A.I. Solutions"
        # Send email via Form.py (ModelForm)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            mail = EmailMessage(subject, message, company, [email])
            mail.send()

            messages.success(request, "Email sent successfully !")
            return HttpResponseRedirect('/backend')

    else:
        form =EmailForm()
        return render(request, {'form':form})
