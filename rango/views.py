from django.shortcuts import render
from django.http import HttpResponse
from html.parser import HTMLParser
from rango.models import Category #import the Category model
from rango.models import Page #import the Page model
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse

def index(request):
    category_list = Category.objects.order_by('-likes')[:5] #retrieve top 5 categories by the number of likes in descending order
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list
    
    return render(request, 'rango/index.html', context=context_dict)

    
def about(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'This tutorial has been put together by Alex Paterson.'}
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/about.html', context=context_dict)#
    
def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

def show_category(request, category_name_slug):
    context_dict = {} #create a context dictionary whch we can pass to the template rendering engine
    
    try: #attempt to find a category name slug with the given name
        category = Category.objects.get(slug=category_name_slug)
        
        pages = Page.objects.filter(category=category)  #retrieve all associated pages, filter() will return a list of page objects or an empty list
        
        context_dict['pages'] = pages   #add results list to template context under pages
        context_dict['category'] = category     #and under category
    
    except Category.DoesNotExist: #if try fails, display no category message
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context=context_dict)
    
def add_page(request, category_name_slug):
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None
            
        # You cannot add a page to a Category that does not exist...
        if category is None:
            return redirect('/rango/')
        
        form = PageForm()
        
        if request.method == 'POST':
            form = PageForm(request.POST)
        
            if form.is_valid():
                if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views = 0
                    page.save()
                    
                    return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context=context_dict)