
#librerias de python
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


#librerias mias
from .forms import CreateUserForm

def home(request):
    context={}
    return render(request, 'index.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Participante')
            user.groups.add(group)
            messages.success(request, 'la carga ha sido exitosa ' + username)
            return redirect('login')



    context={'form': form}
    return render(request,'register.html',context)



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'el usuario o la contra, son invalidos')
            
    context ={}

    return render(request,'login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')



def Usuario(request):
    Participantes = User.objects.all()
    usuarios_totales = User.objects.count()
    context ={'participantes':Participantes, 'usuarios_totales':usuarios_totales}

    return render(request,'usuarios.html',context)