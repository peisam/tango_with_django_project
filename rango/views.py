from django.shortcuts import render,redirect
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserprofileForm,RegisterForm
from django.contrib import  auth
from django.contrib.auth.decorators import login_required
from rango.google_search3 import getGooglepage

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html', {})
# def category(request, category_name_slug):
#     context_dict = {}
#
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#         context_dict['category'] = category
#         pages = Page.objects.filter(category=category).order_by('-views')
#         context_dict['pages'] = pages
#         context_dict['category_name_slug'] = category_name_slug
#     except Category.DoesNotExist:
#         pass
#
#     return render(request, 'rango/category.html', context_dict)
def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            G = getGooglepage()
            result_list = G.getpage(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid:
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request,'rango/add_category.html', {'form': form})

def display_meta(request):
    values = request.META.items()
    #values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

@login_required
def add_page(request,category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form  = PageForm(request.POST)
        if form.is_valid:
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict = {'form': form, 'caregory': cat}
    return render(request, 'rango/add_page.html', context_dict)

# def register(requset):
#     registered = False
#     if requset.method == 'POST':
#         user_form = RegisterForm(data=requset.POST)
#         profile_form = UserprofileForm(data=requset.POST)
#         if user_form.is_valid and profile_form.is_valid:
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in requset.FILES:
#                 profile.picture = requset.FILES['picture']
#             profile.save()
#
#             registered = True
#         else:
#             print user_form.errors, profile_form.errors
#
#     else:
#         user_form = RegisterForm()
#         profile_form = UserprofileForm()
#
#     return render(requset,'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})
#
#
# def login(request):
#
#     if request.method == 'POST':
#         username = request.POST.get('username',' ')
#         password = request.POST.get('password',' ')
#        #next =request.POST.get('next', ' ')
#         user = auth.authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 auth.login(request, user)
#                 #f next:
#                     #eurl = '/rango/' + next
#                     #eturn HttpResponseRedirect(reurl)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 # An inactive account was used - no logging in!
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             # Bad login details were provided. So we can't log the user in.
#             print "Invalid login details: {0}, {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")
#
#     else:
#         return render(request, 'rango/login.html', {})
#
# @login_required
# def logout(request):
#     auth.logout(request)
    # return HttpResponseRedirect('/rango/')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# from rango.google_search import run_query
# def search(request):
#     result_list = ' '
#
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#
#         if query:
  #          Run our Bing function to get the results list!
            # result_list = query
    #
    # return render(request, 'rango/google.html', {'cars': result_list})

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

#def add_profile(request):



