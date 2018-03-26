from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.

def index(request):
    return render(request, 'login/index.html')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['id']),
              # 'item': Wishlist.objects.get(id=id),
            'items': Wishlist.objects.all()
        }
        return render(request, 'login/success.html', context)   

# post method for add item

def createItem(request):
    if 'newitem' in request.POST:
        item = Wishlist.objects.create(name=request.POST['newitem'])
        users = User.objects.get(id=request.session['id'])
    else:
        newitem = False
    return render(request, 'login/add.html') 
 

def loading(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    first_name = request.POST['fname'] 
    last_name = request.POST['lname']
    email = request.POST['email']
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
    request.session['id'] = user.id
    return redirect('/wish_items/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    email = request.POST['email']
    request.session['id'] = User.objects.get(email=email).id
    return redirect('/wish_items/success')

def logout(request):
    request.session.clear()
    return redirect('/')     

def wish(request, id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'item': Wishlist.objects.get(id=id),
            'items': Wishlist.objects.all()
        } 
    # print Wishlist.objects.get(id=id)  
    return render(request, 'login/wish.html', context)  

def delete(request, id): 
    item = Wishlist.objects.get(id=id)
    item.delete()
    return redirect('/wish_items/success')   

# def add(request, id): 
#     if 'id' in request.session:
#         a = Wishlist.objects.get(id=id)
        
#     a.append()
#     return redirect('/wish_items/success')      



  
