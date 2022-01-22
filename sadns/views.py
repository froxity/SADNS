from django.shortcuts import render

def handler400(request, exception):
  return render(request, "httpresponse/http400.html", status=400)

def handler403(request, exception):
  return render(request, "httpresponse/http403.html", status=403)

def handler404(request, exception):
  return render(request, "httpresponse/http404.html", status=404)

# def handler500(request):
#   return render(request, "httpresponse/http500.html", status=500)