
#librerias de python
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

#librerias mias
from .forms import *
from .models import *
from .decorador import allowed_user
from .admin import *


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
            group = Group.objects.get(name='participante')
            user.groups.add(group)
            participante.objects.create(user=user,name=user.username,email=user.email)
            messages.success(request, 'la carga ha sido exitosa ' + username)
            return redirect('login')



    context={'form': form}
    return render(request,'registro.html',context)



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
    Usuarios = User.objects.all()
    usuarios_totales = User.objects.count()
    admin= Usuarios.filter(is_superuser=True).count()
    participante= Usuarios.filter(is_superuser=False).count()
    context ={'participantes':Usuarios, 'usuarios_totales':usuarios_totales, 'admin':admin, 'participante':participante}

    return render(request,'usuarios.html',context)

@login_required(login_url='login')


def Juego(request):
    
    context ={}

    render(request,'juego.html', context)


def Actualizar_Usuario(request,pk):

    usuarios=User.objects.get(id=pk)
    form =CustomerForm(instance=usuarios)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=usuarios)
        if form.is_valid():
            form.save()
            return redirect('estadisticas')

    context ={'form':form}

    return render(request,'actualizar_usuario.html',context)



@login_required(login_url='login')
def Perfil_usuario(request):
	participante = request.user.participante
	form = CustomerForm(instance=participante)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=participante)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'perfil_usuario.html', context)

@login_required(login_url='login')
def deleteUser(request, pk):
    usuarios = User.objects.get(id=pk)
    context ={'item': usuarios}
    if request.method == 'POST':
        usuarios.delete()
        return redirect('estadisticas')

    return render(request,'eliminar_usuario.html',context)


def tablero(request):
    total_usuarios = participante.objects.order_by('-puntaje_total')[:10]
    contador = total_usuarios.count()

    context = {

        'participantes':total_usuarios,
        'contar_user':contador
    }

    return render(request,'tablero.html', context)

@allowed_user(allowed_roles=['participante'])
def jugar(request):

	participantes, created= participante.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		pregunta_pk = request.POST.get('pregunta_pk')
		pregunta_respondida = participantes.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
		respuesta_pk = request.POST.get('respuesta_pk')
		opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)

		participantes.validar_intento(pregunta_respondida, opcion_selecionada)

		return redirect('resultado', pregunta_respondida.pk)

	else:
		pregunta = participantes.obtener_nuevas_preguntas()
		if pregunta is not None:
			participantes.crear_intentos(pregunta)

		context = {
			'pregunta':pregunta
		}

	return render(request, 'jugar.html', context)



def resultado_pregunta(request, pregunta_respondida_pk):
	respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

	context = {
		'respondida':respondida
	}
	return render(request, 'resultados.html', context)





def inicio_juego(request):
    context = {}
    return render(request, 'inicio_juego.html',context)



def crear_pregunta(request):
    form = pregunta()

    if request.method == 'POST':
        form= pregunta(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')



    context={'form': form}
    return render(request, 'crear_pregunta.html',context)

def crear_respuesta(request):
    form = respuesta()

    if request.method == 'POST':
        form= respuesta(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')



    context={'form': form}
    return render(request, 'crear_pregunta.html',context)