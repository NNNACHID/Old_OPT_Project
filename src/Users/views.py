from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.html import escape

from Users.models import *

# Create your views here.
def index(request):
    
    context = {}
    categories = Category.objects.order_by("name")
    
    context["categories"] = categories
    
    return render(request, 'users/index.html', context=context)

def add_category(request):
    category_name = escape(request.POST.get("category-name"))
    category, created = Category.objects.get_or_create(name=category_name)
    if not created:
        return HttpResponse(" the category already exist ! ", status=409)
    return HttpResponse(f'<h2>{category_name}</h2>')

def add_user(request):
    user_name = escape(request.POST.get("category-name"))
    Category.objects.create(name=user_name)
    return redirect('home')