from django.urls import path
from . import views

urlpatterns = [
    path('editar/<int:item_id>/', views.editar_item, name='editar_item'),
    path('excluir/<int:item_id>/', views.excluir_item, name='excluir_item'),
    path('historico/<int:item_id>/', views.historico_item, name='historico_item'),
]
