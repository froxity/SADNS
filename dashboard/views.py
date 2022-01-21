from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from .models import *
from .forms import *
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from textwrap import wrap
import json
import io
import datetime

# Libary for html to pdf
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
# Create your views here.

#  Render HTML to PDF using xhtml2pdf
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Generate a PDF file for dashboard
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        name = request.user.first_name
        
        # Getting all domains object from user (that login to system)
        domains = Domain.objects.filter(owner=profile)
        
        # Calculate Total DNS queries
        totalDNSquery = 0
        for x in domains:
            totalDNSquery = totalDNSquery + x.freq
        # end -- Calculate Total DNS queries

        # Activity Report process 
        top_five = Domain.objects.order_by('-freq').filter(owner=profile).values_list('freq', flat=True).distinct()
        top_activity = Domain.objects.order_by('-freq').filter(freq__in=top_five[:5], owner=profile)
        # End -- Activity Report process

        # Category Report process
        gambling, socialmed, security, adult, others = 0, 0, 0, 0, 0
        for x in domains:
            if (x.cat_id.name == 'Adult'):
                adult = adult + x.freq
            elif (x.cat_id.name == 'Gambling'):
                gambling = gambling + x.freq
            elif (x.cat_id.name == 'Social Media'):
                socialmed = socialmed + x.freq
            elif (x.cat_id.name == 'Security'):
                security = security + x.freq
            elif (x.cat_id.name == 'Others'):
                others = others + x.freq
                
        getTime = datetime.datetime.now()
        date = getTime.strftime("%x")
        time = getTime.strftime("%c")
        # End -- Category Report process

        context = {
            'name' : name,
            'totalDNSquery': totalDNSquery,
            'domains': domains,
            'top_activity': top_activity,
            'Adult': adult, 
            'Gambling': gambling, 
            'Social': socialmed, 
            'Security': security, 
            'Others': others,
            'date': date,
            'time': time,
        }
        pdf = render_to_pdf('dashboard/reportpdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

# Generate dashboard page
@login_required(login_url="login")
def dashboard(request):
    profile = request.user.profile
    name = request.user.first_name
    
    # Getting all domains object from user (that login to system)
    domains = Domain.objects.filter(owner=profile)
    
    # Calculate Total DNS queries
    totalDNSquery = 0
    for x in domains:
        totalDNSquery = totalDNSquery + x.freq
    # end -- Calculate Total DNS queries

    # Activity Report process 
    top_five = Domain.objects.order_by('-freq').filter(owner=profile).values_list('freq', flat=True).distinct()
    top_activity = Domain.objects.order_by('-freq').filter(freq__in=top_five[:5], owner=profile)
    datatop_five = []
    datatop_domain = []
    for x in top_activity:
        datatop_domain.append(x.domain)
        datatop_five.append(x.freq)
    # End -- Activity Report process

    # Category Report process
    gambling, socialmed, security, adult, others = 0, 0, 0, 0, 0
    for x in domains:
        if (x.cat_id.name == 'Adult'):
            adult = adult + x.freq
        elif (x.cat_id.name == 'Gambling'):
            gambling = gambling + x.freq
        elif (x.cat_id.name == 'Social Media'):
            socialmed = socialmed + x.freq
        elif (x.cat_id.name == 'Security'):
            security = security + x.freq
        elif (x.cat_id.name == 'Others'):
            others = others + x.freq
            
    data_category = [adult, gambling, socialmed, security, others]
    # End -- Category Report process

    context = {
        'name' : name,
        'totalDNSquery': totalDNSquery,
        'domains': domains,
        'datatop_five': json.dumps(datatop_five),
        'labels': json.dumps(datatop_domain),
        'data_category' : json.dumps(data_category),
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url="login")
def webfilter(request):
    profile = request.user.profile
    name = request.user.first_name
    cat = profileConfig.objects.all().filter(owner=profile)
    context = {
        'name' : name,
        'categorys': cat,
    }
    return render(request, 'dashboard/webfilter.html', context)

@login_required(login_url="login")
def setfilter_true(request, pk):
    profile = request.user.profile
    config = profile.profileconfig_set.get(id=pk)
    config.cat_status = True;
    config.save()
    messages.success(request, "Enable selected category")
    return redirect('webfilter')

@login_required(login_url="login")
def setfilter_false(request, pk):
    profile = request.user.profile
    config = profile.profileconfig_set.get(id=pk)
    config.cat_status = False;
    config.save()
    messages.error(request, "Disable selected category")
    return redirect('webfilter')

# CREATE AND RETRIEVE WHITELIST DOMAIN && BLACKLIST DOMAIN
@login_required(login_url="login")
def domains(request):
    profile = request.user.profile
    name = request.user.first_name
    form_whitelist = WhitelistForm(instance=profile)
    form_blacklist = BlacklistForm(instance=profile)
    
    # whitelist POST request
    if request.method=='POST' and 'button1' in request.POST:
        form_whitelist = WhitelistForm(request.POST)
        if form_whitelist.is_valid():
            whitelist = form_whitelist.save(commit=False)
            whitelist.owner = profile
            whitelist.save()
            messages.success(request, "Domain was added successfully!")
            return redirect('domains')

    # blacklist POST request
    if request.method=='POST' and 'button2' in request.POST:
        form_blacklist = BlacklistForm(request.POST)
        if form_blacklist.is_valid():
            blacklist = form_blacklist.save(commit=False)
            blacklist.owner = profile
            blacklist.save()
            messages.success(request, "Domain was added successfully!")
            return redirect('domains')

    # GET
    domain_whitelist = profile.whitelist_set.all()
    domain_blacklist = profile.blacklist_set.all()
    context = {
        'domain_whitelist' : domain_whitelist,
        'domain_blacklist' : domain_blacklist,
        'name' : name,
    }

    return render(request, 'dashboard/domains.html', context)

# UPDATE WHITELIST DOMAIN
@login_required(login_url="login")
def edit_wdomain(request, pk):
    profile = request.user.profile
    name = request.user.first_name
    whitelist = profile.whitelist_set.get(id=pk)
    form_whitelist = WhitelistForm(instance=whitelist)

    if request.method == "POST":
        form_whitelist = WhitelistForm(request.POST, instance=whitelist)
        if form_whitelist.is_valid():
            form_whitelist.save()
            messages.success(request, "Domain whitelist was update successfully!")
            return redirect('domains')
    
    context = {
        'form_whitelist': form_whitelist,
        'name' : name,
    }

    return render(request, 'dashboard/edit-w_domain.html', context)

# UPDATE BLACKLIST DOMAIN
@login_required(login_url="login")
def edit_bdomain(request, pk):
    profile = request.user.profile
    name = request.user.first_name
    blacklist = profile.blacklist_set.get(id=pk)
    form_blacklist = BlacklistForm(instance=blacklist)

    if request.method == "POST":
        form_blacklist = BlacklistForm(request.POST, instance=blacklist)
        if form_blacklist.is_valid():
            form_blacklist.save()
            messages.success(request, "Domain blacklist was update successfully!")
            return redirect('domains')
    
    context = {
        'form_blacklist': form_blacklist,
        'name' : name,
    }

    return render(request, 'dashboard/edit-b_domain.html', context)

# DELETE WHITELIST DOMAIN
@login_required(login_url="login")
def delete_wdomain(request, pk):
    profile = request.user.profile
    whitelist = profile.whitelist_set.get(id=pk)

    whitelist.delete()
    messages.success(request, "Domain whitelist has been deleted!")
    return redirect('domains')

# DELETE BLACKLIST DOMAIN
@login_required(login_url="login")
def delete_bdomain(request, pk):
    profile = request.user.profile
    blacklist = profile.blacklist_set.get(id=pk)

    blacklist.delete()
    messages.success(request, "Domain blacklist has been deleted!")
    return redirect('domains')


