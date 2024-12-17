from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', views.pagina_principal,name= 'pagina_principal'),
    path('login/', auth_views.LoginView.as_view(template_name='reservas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pagina_principal'), name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
   


    path('nacionalidades/', views.listar_nacionalidades, name='listar_nacionalidades'),
    path('nacionalidades/crear/', views.crear_nacionalidad, name='crear_nacionalidad'),

    path('pasajeros/', views.listar_pasajeros, name='listar_pasajeros'),
    path('pasajeros/crear/', views.crear_pasajero, name='crear_pasajero'),
    path('pasajero/editar/<int:id_pasajero>/', views.editar_pasajero, name='editar_pasajero'),
    path('pasajero/eliminar/<int:id_pasajero>/', views.eliminar_pasajero, name='eliminar_pasajero'),

    path('habitaciones/', views.listar_habitaciones, name='listar_habitaciones'),
    path('habitaciones/crear/', views.crear_habitacion, name='crear_habitacion'),
    path('habitacion/editar/<int:id_habitacion>/', views.editar_habitacion, name='editar_habitacion'),
    path('habitacion/eliminar/<int:id_habitacion>/', views.eliminar_habitacion, name='eliminar_habitacion'),

    path('listar/pagos/', views.listar_pagos, name='listar_pagos'),
    path('crear/pago/', views.crear_pago, name='crear_pago'),  # Asegúrate de que esta línea esté presente

    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('tipo_usuario/nueva/', views.crear_tipo_usuario, name='crear_tipo_usuario'),  
    
]
