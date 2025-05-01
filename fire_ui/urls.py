from django.urls import path
from . import views

urlpatterns = [
    # URLs para focos_de_queimada
    path('', views.home, name='home'),
    path('focos/', views.FocosDeQueimadaListView.as_view(), name='focos-list'),
    path('focos/<int:pk>/', views.FocosDeQueimadaDetailView.as_view(), name='focos-detail'),
    path('focos/novo/', views.FocosDeQueimadaCreateView.as_view(), name='focos-create'),
    path('focos/<int:pk>/editar/', views.FocosDeQueimadaUpdateView.as_view(), name='focos-update'),
    path('focos/<int:pk>/excluir/', views.FocosDeQueimadaDeleteView.as_view(), name='focos-delete'),
    
    # Adicione URLs para outras tabelas conforme necessário
]
