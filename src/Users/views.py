from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape

from Users.models import *


# Create your views here.
def index(request):

    context = {}

    category_slug = request.GET.get("category")
    category = Category.get_default_category()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

    context["categories"] = Category.objects.order_by("slug")
    context["users"] = category.user_set.order_by("description")

    return render(request, "users/index.html", context=context)


def add_category(request):
    category_name = escape(request.POST.get("category-name"))
    category, created = Category.objects.get_or_create(
        name=category_name, slug=slugify(category_name)
    )
    if not created:
        return HttpResponse(" the category already exist ! ", status=409)
    return render(request, "users/categories.html", context={"category": category})


def add_user(request):

    category = Category.objects.get(slug=request.POST.get("category"))

    description = escape(request.POST.get("user-description"))
    user = User.objects.create(description=description, category=category)

    return render(request, "users/user.html", context={"user": user})


def delete_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.delete()

    return HttpResponse("")


def get_users(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    users = category.user_set.order_by("description")
    return render(request, "users/users.html", context={"users": users})
