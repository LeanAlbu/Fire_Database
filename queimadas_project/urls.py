from django.contrib import admin
from django.urls import path
from queimadas_app import views

urlpatterns = [


    path('limpar_banco/', views.limpar_banco, name='limpar_banco'),


    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    
    # Regiao URLs
    path('regioes/', views.regiao_list, name='regiao_list'),
    path('regioes/add/', views.regiao_create, name='regiao_create'),
    path('regioes/<int:pk>/edit/', views.regiao_update, name='regiao_update'),
    path('regioes/<int:pk>/delete/', views.regiao_delete, name='regiao_delete'),
    
    # Municipio URLs
    path('municipios/', views.municipio_list, name='municipio_list'),
    path('municipios/add/', views.municipio_create, name='municipio_create'),
    path('municipios/<int:pk>/edit/', views.municipio_update, name='municipio_update'),
    path('municipios/<int:pk>/delete/', views.municipio_delete, name='municipio_delete'),
    
    # Foco URLs
    path('focos/list', views.foco_list, name='foco_list'),
    path('focos/add/', views.foco_create, name='foco_create'),
    path('focos/<int:pk>/edit/', views.foco_update, name='foco_update'),
    path('focos/<int:pk>/delete/', views.foco_delete, name='foco_delete'),
    
    # Satelite URLs
    path('satelites/', views.satelite_list, name='satelite_list'),
    path('satelites/add/', views.satelite_create, name='satelite_create'),
    path('satelites/<int:pk>/edit/', views.satelite_update, name='satelite_update'),
    path('satelites/<int:pk>/delete/', views.satelite_delete, name='satelite_delete'),
    
    # SateliteQueimada URLs
    #path('relacoes/', views.satelite_queimada_list, name='satelite_queimada_list'),
    #path('relacoes/add/', views.satelite_queimada_create, name='satelite_queimada_create'),
    #path('relacoes/<int:pk>/edit/', views.satelite_queimada_update, name='satelite_queimada_update'),
    #path('relacoes/<int:pk>/delete/', views.satelite_queimada_delete, name='satelite_queimada_delete'),
]
