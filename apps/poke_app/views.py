from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse ## need to import reverse when using named routes!
from django.contrib import messages
from .models import *
import bcrypt
from django.db.models import Q
from django.db.models import Count

def index(request):
    request.session.flush()
    return render(request, "poke_app/index.html")
def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if (errors): 
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect(reverse('index'))
        else:
            hashpass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'],email=request.POST['email'], password=hashpass, dob = request.POST['dob'])
            user_id = User.objects.get(email=request.POST['email']).id
            request.session['user'] = user_id
            request.session['alias'] = User.objects.get(alias=request.POST['alias']).name
            return redirect(reverse('pokes')) 
    else:
        return redirect(reverse('index'))
def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if (errors): 
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect(reverse('index'))
        user =  User.objects.get(email = request.POST["email"]) 
        if user.email == request.POST['email']:
            request.session["alias"] = user.alias
            request.session["user"] = user.id
            encpass = request.POST['password']
            dbpass= user.password
        if bcrypt.checkpw( encpass.encode(), dbpass.encode()):
            return redirect('pokes')
        else:
            return redirect(reverse('index'))
def pokes(request):
    user_id = request.session['user']  
    context = {
        "users": User.objects.all().exclude(id = user_id),
        "pokes" : Poke.objects.filter(poked_id = user_id),
        "peoplepokedme" : Poke.objects.filter(poked_id = user_id).annotate(the_count=Count('id')),
    }
    print 
    return render(request, 'poke_app/pokes.html', context, user_id)
def poke(request, user_id):
    poker = User.objects.get(id = request.session['user'])
    poked = User.objects.get(id = user_id)
    Poke.objects.create(poker = poker, poked = poked)
    return redirect(reverse('pokes'))
    
