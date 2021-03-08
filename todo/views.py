
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required




# Create your views here.
def home(request):
    return render(request,'todo/home.html')
def signupuser(request):
    if request.method=="GET":
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('current')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'username has already taken'})
        else: 
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'password didnot match'})

def loginuser(request):
    if request.method=="GET":
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user  is None:
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'username n password sidnot match'})

        else:
            login(request,user)
            return redirect('current')


@login_required
def current(request):
    todo=Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo/current.html',{'todo':todo})
@login_required
def logoutuser(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')
@login_required
def createtodo(request):
    if request.method=="GET":
        return render(request,'todo/createtodo.html',{'todoform':TodoForm()})
    else:
        try:
            todoform=TodoForm(request.POST)
            newtodoform=todoform.save(commit=False)
            newtodoform.user=request.user
            newtodoform.save()
            return redirect('current')
        except ValueError:
            return render(request,'todo/createtodo.html',{'todoform':TodoForm(),'error':'Bad data for the creating todo'})
@login_required
def viewtodo(request,todo_id):
    todo=get_object_or_404(Todo,pk=todo_id,user=request.user)
    if request.method=="GET":
        todoform=TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':todoform})
    else:
        try:
            todoform=TodoForm(request.POST,instance=todo)
            todoform.save()
            return redirect('current')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':todoform,'error':'Bad information'})

            
@login_required
def completetodo(request,todo_id):
    todo=get_object_or_404(Todo,pk=todo_id,user=request.user)
    if request.method=="POST":
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect('current')


@login_required
def deletetodo(request,todo_id):
    todo=get_object_or_404(Todo,pk=todo_id,user=request.user)
    if request.method=="POST":
        todo.delete()
        return redirect('current')

@login_required
def completedtodo(request):
    todo=Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by("-datecompleted")
    return render(request,'todo/completedtodo.html',{'todo':todo})
    