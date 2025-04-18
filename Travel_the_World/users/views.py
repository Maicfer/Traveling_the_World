from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from datetime import datetime, timedelta
from django.http import HttpResponse
from .models import Destino
from .forms import ReseñaForm
from .models import Reseña
import re
from .models import Profile
from django.core.files.storage import FileSystemStorage
from .forms import ProfileForm 

def home_view(request):
    return render(request, "home.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "users/login.html")

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        document_number = request.POST.get('document_number')
        birthdate = request.POST.get('birthdate')
        country = request.POST.get('country')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        profile_picture = request.FILES.get('profile_picture')
        terms = request.POST.get('terms')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return redirect('register')

        if Profile.objects.filter(document_number=document_number).exists():
            messages.error(request, 'Este número de documento ya está registrado.')
            return redirect('register')

        if not terms:
            messages.error(request, 'Debes aceptar los términos y condiciones.')
            return redirect('register')

        username = email.split('@')[0]
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = full_name
        user.save()

        profile = Profile.objects.create(
            user=user,
            document_number=document_number,
            birthdate=birthdate,
            country=country,
            city=city,
            phone=phone,
            gender=gender,
        )

        if profile_picture:
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            profile.profile_picture = filename
            profile.save()

        messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'users/register.html')


@login_required
def profile_view(request):
    return render(request, "users/profile.html")

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email', "").strip()

        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            messages.error(request, 'Correo electrónico inválido')
        elif User.objects.filter(email=email).exclude(username=user.username).exists():
            messages.error(request, 'Ese correo ya está en uso')
        else:
            user.email = email
            user.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('profile')

    return render(request, "users/update_profile.html")

@login_required
def change_password_view(request):
    success = False  # Bandera para mostrar modal de éxito

    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password', "").strip()
        new_password1 = request.POST.get('new_password1', "").strip()
        new_password2 = request.POST.get('new_password2', "").strip()
        new_email = request.POST.get('new_email', "").strip()

        # Validar contraseña actual
        if not user.check_password(old_password):
            messages.error(request, 'La contraseña actual es incorrecta')
        # Validar nueva contraseña
        elif new_password1 != new_password2:
            messages.error(request, 'Las nuevas contraseñas no coinciden')
        elif len(new_password1) < 8:
            messages.error(request, 'La nueva contraseña debe tener al menos 8 caracteres')
        else:
            # Actualizar contraseña
            user.set_password(new_password1)
            update_session_auth_hash(request, user)
            success = True
            messages.success(request, 'Contraseña cambiada correctamente.')

        # Validar y actualizar correo (opcional)
        if new_email:
            email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not re.match(email_regex, new_email):
                messages.error(request, 'Correo electrónico inválido')
            elif User.objects.filter(email=new_email).exclude(username=user.username).exists():
                messages.error(request, 'Ese correo ya está en uso')
            else:
                user.email = new_email
                messages.success(request, 'Correo actualizado correctamente.')

        # Guardar cambios
        user.save()

    return render(request, "users/change_password.html", {"success": success})

@login_required
def change_email_view(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email', "").strip()

        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, new_email):
            messages.error(request, 'Correo electrónico inválido')
        elif User.objects.filter(email=new_email).exclude(username=request.user.username).exists():
            messages.error(request, 'Ese correo ya está en uso')
        else:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Correo actualizado correctamente')
            return redirect('profile')

    return render(request, "users/change_email.html")

def buscar_vuelos(request):
    origen = request.GET.get('origen', '').lower()
    destino = request.GET.get('destino', '').lower()
    fecha = request.GET.get('fecha', '')  # Fecha que el usuario ingresó

    fechas_simuladas = [(datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]

    vuelos_simulados = [
        {'origen': 'Bogotá', 'destino': 'Medellín', 'precio': 120000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Cali', 'precio': 150000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Cartagena', 'precio': 200000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Barranquilla', 'precio': 180000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'San Andrés', 'precio': 250000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Pereira', 'precio': 130000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Bucaramanga', 'precio': 110000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Leticia', 'precio': 300000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Armenia', 'precio': 140000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Manizales', 'precio': 135000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Madrid', 'precio': 2400000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Buenos Aires', 'precio': 1800000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Ciudad de México', 'precio': 1600000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Miami', 'precio': 2200000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Londres', 'precio': 3000000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'París', 'precio': 3100000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Tokio', 'precio': 4200000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Roma', 'precio': 2900000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Sídney', 'precio': 5000000, 'fechas': fechas_simuladas},
        {'origen': 'Bogotá', 'destino': 'Toronto', 'precio': 2600000, 'fechas': fechas_simuladas},
    ]

    resultados = [
        vuelo for vuelo in vuelos_simulados
        if (origen in vuelo['origen'].lower())
        and (destino in vuelo['destino'].lower())
        and (not fecha or fecha in vuelo['fechas'])
    ]

    # Esta línea renderiza la plantilla de resultados correctamente
    return render(request, 'users/buscar_vuelos.html', {
        'resultados': resultados,
        'origen': origen,
        'destino': destino,
        'fecha': fecha,
    })

def destinos_view(request):
    destinos = Destino.objects.all()
    return render(request, 'users/destinos.html', {'destinos': destinos})

from users.models import Destino

def crear_destinos_iniciales():
    destinos = [
        {
            "nombre": "Miami",
            "pais": "Estados Unidos",
            "descripcion": "Playas y vida nocturna",
            "precio": 1500,
            "imagen": "https://www.miamiandbeaches.com/getmedia/f35e8173-0df2-4bed-86dc-727805570021/Miami-Aerial-Photos-Golden-Dusk-Photography-1440x900.jpg?width=1000&resizemode=force"
        },
        {
            "nombre": "Medellín",
            "pais": "Colombia",
            "descripcion": "Ciudad de la eterna primavera",
            "precio": 800,
            "imagen": "https://locationcolombia.com/wp-content/uploads/2022/04/MEDELLIN-Panoramicas-noche-SEC-CULTURA-MED-2007-1-1-2048x1328.jpg"
        },
        {
            "nombre": "San Andrés",
            "pais": "Colombia",
            "descripcion": "Isla paradisíaca del Caribe",
            "precio": 1200,
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Panor%C3%A1mica_de_San_Andres.JPG/1280px-Panor%C3%A1mica_de_San_Andres.JPG"
        },
        {
            "nombre": "Madrid",
            "pais": "España",
            "descripcion": "Capital de España con mucha historia",
            "precio": 1800,
            "imagen": "https://madridando.com/wp-content/uploads/2018/10/plaza-de-cibeles.jpeg"
        },
        {
            "nombre": "París",
            "pais": "Francia",
            "descripcion": "Ciudad del amor y la Torre Eiffel",
            "precio": 2000,
            "imagen": "https://www.viajarafrancia.com/wp-content/uploads/2016/04/Paris-760x500.jpg"
        },
                {
            "nombre": "Roma",
            "pais": "Italia",
            "descripcion": "Todos los caminos conducen a roma!, Cultura e historia.",
            "precio": 2200,
            "imagen": "https://www.viajarafrancia.com/wp-content/uploads/2016/04/Paris-760x500.jpg"
        },
    ]

    for d in destinos:
        Destino.objects.get_or_create(
            nombre=d["nombre"],
            defaults={
                "pais": d["pais"],
                "descripcion": d["descripcion"],
                "precio": d["precio"],
                "imagen": d["imagen"],
            }
        )

def cargar_datos_si_es_necesario(request):
    crear_destinos_iniciales()
    return HttpResponse("✅ Datos cargados correctamente.")

def ready_crear_destinos():
    try:
        crear_destinos_iniciales()
    except Exception as e:
        print(f"❌ Error al crear destinos: {e}")

def mostrar_destinos(request):
    destinos = Destino.objects.all()
    texto = "<br>".join([f"{d.nombre} - {d.descripcion} - ${d.precio}" for d in destinos])
    return HttpResponse(texto)

def mas_visitados(request):
    destinos_mas_visitados = [
        {
            'nombre': 'París',
            'pais': 'Francia',
            'descripcion': 'La ciudad del amor y la Torre Eiffel.',
            'lat': 48.8566,
            'lon': 2.3522,
            'imagen': 'https://media.gettyimages.com/id/924891460/es/foto/torre-eiffel-en-par%C3%ADs-francia.jpg?s=612x612&w=0&k=20&c=vOrCHGUkAClTCCow2b0z_3xJ64MBKCKMAAipnWdpySw='
        },
        {
            'nombre': 'Bangkok',
            'pais': 'Tailandia',
            'descripcion': 'Templos exóticos, comida callejera y mercados flotantes.',
            'lat': 13.7563,
            'lon': 100.5018,
            'imagen': 'https://media.gettyimages.com/id/507913346/es/foto/templo-de-wat-arun-al-anochecer-en-bangkok-tailandia.jpg?s=612x612&w=0&k=20&c=GJJY6HPpQlktNYNRcp1QtgLC1y5w9lvWN7lZ2R8isz4='
        },
        {
            'nombre': 'Londres',
            'pais': 'Reino Unido',
            'descripcion': 'El Big Ben, museos y cultura inglesa.',
            'lat': 51.5074,
            'lon': -0.1278,
            'imagen': 'https://media.gettyimages.com/id/1594359572/es/foto/tr%C3%A1fico-en-londres-en-el-big-ben-y-westminster-bridge.jpg?s=612x612&w=0&k=20&c=9plJnVJIO8NLbAiRtOgraKeyoIpQMI0JQ1p2HJrm2do='
        },
        {
            'nombre': 'Dubái',
            'pais': 'Emiratos Árabes Unidos',
            'descripcion': 'Rascacielos futuristas, lujo y desierto.',
            'lat': 25.2048,
            'lon': 55.2708,
            'imagen': 'https://media.gettyimages.com/id/1309800132/es/foto/vista-del-horizonte-de-dub%C3%A1i-desde-el-puerto-deportivo-de-marasi-en-la-ciudad-en-el-centro-de.jpg?s=612x612&w=0&k=20&c=P6-NRxG1FIOnodOH0lsHXKpeF6s8kUrTVHCNZFWT9-M='
        },
        {
            'nombre': 'Estambul',
            'pais': 'Turquía',
            'descripcion': 'Historia, cultura y una mezcla entre oriente y occidente.',
            'lat': 41.0082,
            'lon': 28.9784,
            'imagen': 'https://media.gettyimages.com/id/656642008/es/foto/vista-a%C3%A9rea-de-estambul-iluminada-por-la-noche.jpg?s=612x612&w=0&k=20&c=2ggkTucbWLx-5d3CrC-wCB509ol2FyIMXNVSkiNiC6E='
        },
        {
            'nombre': 'Nueva York',
            'pais': 'Estados Unidos',
            'descripcion': 'La ciudad que nunca duerme, hogar de Times Square y Central Park.',
            'lat': 40.7128,
            'lon': -74.0060,
            'imagen': 'https://media.gettyimages.com/id/1401566574/es/foto/new-york-city-downtown-skyline-aerial-view-seen-from-helicopter-usa.jpg?s=612x612&w=0&k=20&c=ENijSbgVHgoGyn_eaTcPPUkGtWRzYMTJ1qcvj_9Jw_o='
        }
    ]
    return render(request, 'users/mas_visitados.html', {'destinos': destinos_mas_visitados})


def vuelos(request):
    return render(request, 'users/vuelos.html')

def hoteles(request):
    return render(request, 'users/hoteles.html')

def paquetes(request):
    return render(request, 'users/paquetes.html')


def reseñas_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        ciudad = request.POST.get('ciudad_visitada') 
        comentario = request.POST.get('comentario')

        if nombre and correo and ciudad and comentario:
            Reseña.objects.create(
                nombre=nombre,
                correo=correo,
                ciudad_visitada=ciudad,
                comentario=comentario
            )
            messages.success(request, '¡Gracias por tu reseña!')
            return redirect('reseñas')
        else:
            messages.error(request, 'Por favor completa todos los campos.')

    reseñas = Reseña.objects.order_by('-fecha')  # las más recientes primero
    return render(request, 'users/reseñas.html', {'reseñas': reseñas})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    else:
        return redirect("home")
