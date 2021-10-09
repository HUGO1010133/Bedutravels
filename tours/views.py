from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Tour, Zona

from .serializers import ZonaSerializer, TourSerializer
from rest_framework import viewsets




# Create your views here.
@login_required()
def index(request):
	""" Atiende la petición GET / """
	tours = Tour.objects.filter(zonaSalida__nombre = "CDMX")

	return render(request, "tours/index.html", {"tours":tours})

def login_user(request):
    """ Atiende las peticiones de GET y POST /login/ """

    if request.method == "POST":
        # Se obtienen los datos del formulario
        user = request.POST["username"]
        passwd = request.POST["password"]
        next_ = request.GET.get("next", "/")
        user_obj = authenticate(username=user, password=passwd)
        if user_obj != None:
            # Tenemos usuario válido, redireccionamos a index
            login(request, user_obj)  # crea la sesión usando cookies
            return redirect(next_)
        else:
            # Usuario malo
            msg = "Datos incorrectos, intente de nuevo!"
    else:
        # Si no hay datos POST entonces es GET y enviamos formulario
        msg = ""

    return render(request, "registration/login.html",
        {
            "msg":msg,
        }
    )

# Vistas basadas en clases para Django Rest
class ZonaViewSet(viewsets.ModelViewSet):
   """
   API que permite realizar operaciones en la tabla Zona
   """
   # Se define el conjunto de datos sobre el que va a operar la vista,
   # en este caso sobre todos los users disponibles.
   queryset = Zona.objects.all().order_by('id')
   # Se define el Serializador encargado de transformar la peticiones
   # en formato JSON a objetos de Django y de Django a JSON.
   serializer_class = ZonaSerializer

class TourViewSet(viewsets.ModelViewSet):
   """
   API que permite realizar operaciones en la tabla Zona
   """
   # Se define el conjunto de datos sobre el que va a operar la vista,
   # en este caso sobre todos los users disponibles.
   queryset = Tour.objects.all().order_by('id')
   # Se define el Serializador encargado de transformar la peticiones
   # en formato JSON a objetos de Django y de Django a JSON.
   serializer_class = TourSerializer