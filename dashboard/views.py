from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #ensures user has to login in first before trying anything else
from django.contrib.auth import logout
from django.contrib import messages
from .models import Product, Order
from .forms import ProductForm, OrderForm, StockSearchForm
from django.contrib.auth.models import User
import csv

# Create your views here.
#this displays the web user interface actually it routes to the pages that actually have the web pages
@login_required(login_url='user-login')#Decorator for views that checks that the user is logged in, redirecting to the log-in page if necessary.
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    product_count = products.count()
    workers_count = User.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm

    context={
        'orders': orders,
        'form': form,
        'products':products,
        'product_count': product_count,
        'orders_count': orders_count,
        'workers_count': workers_count,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='user-login')
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers':workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'product_count':product_count
    }
    return render(request, 'dashboard/staff.html',context)

@login_required(login_url='user-login')
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required(login_url='user-login')
def product(request):   
    items = Product.objects.all() # this uses object relational mapping for fetching data from the database
    #items = Product.objects.raw('SELECT * FROM dashboard_product') # uses sql to fetch data from the database.
    search_form = StockSearchForm(request.POST)
    product_count = items.count()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    if request.method=="POST" or None:
        queryset = Product.objects.filter(category__icontains=search_form['category'].value(),
									      name__icontains=search_form['name'].value(),)
        if search_form['export_to_CSV'].value() == True:             
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
                writer = csv.writer(response)
                writer.writerow(['CATEGORY', ' NAME', 'QUANTITY'])
                instance = queryset
                for stock in instance:
                    writer.writerow([stock.category, stock.name, stock.quantity])
                return response
    context={
        'items':items,
        'form':form,
        'search_form':search_form,
        'product_count':product_count,
        'workers_count':workers_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/product.html',context)

@login_required(login_url='user-login')
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required(login_url='user-login')
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context={
        'form':form,
    }
    return render(request, 'dashboard/product_update.html', context)

@login_required(login_url='user-login')
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()

    context = {
        'orders':orders,
        'orders_count':orders_count,
        'workers_count':workers_count,
        'product_count':product_count,
    }
    return render(request, 'dashboard/order.html', context)

@login_required(login_url='user-login')
def logout_user(request):
    logout(request)
    messages.success(request, ("You have logged out!"))
    return render(request,'user/login.html')


