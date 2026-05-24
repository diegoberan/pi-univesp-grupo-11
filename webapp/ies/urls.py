from django.urls import path
from . import views

app_name = 'ies'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ies/', views.api_ies, name='api_ies'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('consulta/', views.consulta, name='consulta'),
    path('exportar/', views.exportar_csv, name='exportar_csv'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ies/<int:ies_id>/', views.detalhe, name='detalhe'),
]
