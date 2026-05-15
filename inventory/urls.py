from django.urls import path
from . import views

urlpatterns = [
    path('editar/<int:item_id>/', views.editar_item, name='editar_item'),
    path('excluir/<int:item_id>/', views.excluir_item, name='excluir_item'),
    path('historico/<int:item_id>/', views.historico_item, name='historico_item'),
    path('os/', views.os_list, name='os_list'),
    path('os/novo/', views.os_create, name='os_create'),
    path('os/editar/<int:os_id>/', views.os_edit, name='os_edit'),
    path('os/<int:os_id>/', views.os_detail, name='os_detail'),
    path('os/finalizar/<int:os_id>/', views.os_finish, name='os_finish'),
]
