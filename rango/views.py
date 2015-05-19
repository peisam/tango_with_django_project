from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories':category_list}
    return render(request,'rango/index.html',context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page <br/><a href='.//rango/'>index</a>")

def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)