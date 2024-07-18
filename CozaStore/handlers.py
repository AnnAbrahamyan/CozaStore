from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    return render(request, "main/page_not_found.html", {})