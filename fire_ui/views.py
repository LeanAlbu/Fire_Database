# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .forms import FocosDeQueimadaForm
from django.shortcuts import render
from django.db.models import Count
from .models import FocosDeQueimada, Municipios, Satelites, SateliteQueimada

class FocosDeQueimadaListView(ListView):
    model = FocosDeQueimada
    template_name = 'fire_ui/focos_list.html'
    context_object_name = 'focos'
    paginate_by = 20

class FocosDeQueimadaDetailView(DetailView):
    model = FocosDeQueimada
    template_name = 'fire_ui/focos_detail.html'

class FocosDeQueimadaCreateView(CreateView):
    model = FocosDeQueimada
    form_class = FocosDeQueimadaForm
    template_name = 'fire_ui/focos_form.html'
    success_url = reverse_lazy('focos-list')

class FocosDeQueimadaUpdateView(UpdateView):
    model = FocosDeQueimada
    form_class = FocosDeQueimadaForm
    template_name = 'fire_ui/focos_form.html'
    success_url = reverse_lazy('focos-list')

class FocosDeQueimadaDeleteView(DeleteView):
    model = FocosDeQueimada
    template_name = 'fire_ui/focos_confirm_delete.html'
    success_url = reverse_lazy('focos-list')

def home(request):
    # Dados para dashboard
    total_focos = FocosDeQueimada.objects.count()
    total_municipios = Municipios.objects.count()
    total_satelites = Satelites.objects.count()
    
    # Focos por satélite (através de SateliteQueimada)
    focos_por_satelite = SateliteQueimada.objects.values(
        'id_satelite__nome_satelite'
    ).annotate(
        total=Count('id_queimada')
    ).order_by('-total')[:5]
    
    context = {
        'total_focos': total_focos,
        'total_municipios': total_municipios,
        'total_satelites': total_satelites,
        'focos_por_satelite': focos_por_satelite,
    }
    
    return render(request, 'fire_ui/home.html', context)
