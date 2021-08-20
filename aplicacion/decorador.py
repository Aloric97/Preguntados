from django.http import HttpResponse




def allowed_user(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):

            group= None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('no esta permitido entrar a esta pagina ya que eres un usuario anonimo, debes registrar para poder acceder o loguearte a la pagina para acceder')

                
                
        return wrapper_func
    return decorators
