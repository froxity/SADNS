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

# Create your views here.

# Generate a PDF file for dashboard
@login_required(login_url="login")
def generateReport(request):
    profile = request.user.profile
    name = request.user.first_name
    """Getting Data process"""
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
    """End Data process"""
    
    """Drawing PDF process"""
    # Create bytestream buffer
    buffer = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    
    # Create a text object
    textObj = c.beginText()
    textObj.setTextOrigin(inch, inch)
    textObj.setFont('Helvetica', 14)
    
    # Create textline "TITLE"
    textObj.textLine("SA DNS Dashboard Report")
    
    # Get current datetime
    getTime = datetime.datetime.now()
    date = getTime.strftime("%x")
    time = getTime.strftime("%c")
    textObj.textLine(time + " | " + date)
    
    textObj.textLine()
    textObj.textLine()
    textObj.textLine("Total DNS queries: " + str(totalDNSquery))
    textObj.textLine()
    textObj.textLine("--------------------")
    textObj.textLine("Activity Report  ")
    textObj.textLine("--------------------")
    textObj.textLine("Top five domains queries by " + name)
    textObj.textLine()
    for x in top_activity:
        textObj.textLine(x.domain + " | " + str(x.freq))
    textObj.textLine()
    textObj.textLine("----------------------")
    textObj.textLine("Category Report  ")
    textObj.textLine("----------------------")
    textObj.textLine()
    textObj.textLine("Adult: " + str(adult))
    textObj.textLine("Gambling: " + str(gambling))
    textObj.textLine("Social Media: " + str(socialmed))
    textObj.textLine("Security: " + str(security))
    textObj.textLine("Others: " + str(others))
    textObj.textLine()
    textObj.textLine()
    textObj.setFont('Helvetica', 8)
    textObj.textLine("Adult: Domains that contains Not Safe for Work (NSFW) or any pornography content")
    textObj.textLine("Gambling: Domains that contains all gambling website.")
    textObj.textLine("Social Media: Domains that contains any realted social media platform.")
    textObj.textLine("Security: Domains that contains malicious and scam website")
    textObj.textLine("Others: Domains that is categorised not harmful but not listed in default categories")
    
    # Finish up
    c.line(50, 50, 560, 50)
    c.line(50, 100, 560, 100)
    c.line(50, 510, 560, 510)
    c.drawText(textObj)
    c.showPage()
    c.save()
    buffer.seek(0)
    """Drawing PDF process"""
    filename = 'dashboard_' + time + "_.pdf"
    # Return
    return FileResponse(buffer, as_attachment=True, filename=filename)

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


