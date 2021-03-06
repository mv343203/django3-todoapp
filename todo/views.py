from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render (request, 'todo/home.html')


# Create your views here.
def signupuser (request):
    #this lets you view the page
    if request.method == "GET":
        return render (request, 'todo/signupuser.html', {'form':UserCreationForm()})
    #this lets you create a user with django functions and models from import above
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:# this creates the user and grabs the keywords they inputed
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                #logs the user in and we send them somewhere
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render (request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': "Username already exists - please choose a new username!"})

        else:
            # if passwords dont match we send them back to the original page with a message
            return render (request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': "Passwords did not match!"})


def loginuser(request):
    #this lets you view the page
    if request.method == "GET":
        return render (request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    #this lets you create a user with django functions and models from import above
    else:#authenticates the user and provides back a user object
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # if they can not find the user then send them back to the login page
        if user is None:
            return render (request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': "Username and password did not match."})
        else: #were able to authenticate then run this
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodos(request):
    if request.method == "GET" :
        return render (request, 'todo/createtodos.html', {'form': TodoForm()})
    else:
        try:
            #this allows this to pass it into the form
            form = TodoForm(request.POST)
            #create new list but hold off on putting it into the database
            newtodo = form.save(commit=False)
            # this saves the request to the user
            newtodo.user=request.user
            newtodo.save()
            #after save this takes them back to the current page
            return redirect('currenttodos')
        except ValueError:
            # value error where lets say somebody types in a 100+ charactes was used as an example
            return render (request, 'todo/createtodos.html', {'form':TodoForm(), 'error': "Bad data passed in."})


@login_required
def currenttodos(request):
    #goes and gets the todos from the models that have been saved for that particular user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull = True)
    return render (request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    #goes and gets the todos from the models that have been saved for that particular user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render (request, 'todo/completedtodos.html', {'todos':todos})


@login_required
def viewtodo(request, todo_pk):
    #look for this object or raise error with this name Todo, primary key and ensure it belongs to the user)
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET" :
        form = TodoForm(instance=todo)
        return render (request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render (request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error': "Bad data passed in."})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST" :
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST" :
        todo.delete()
        return redirect('currenttodos')
