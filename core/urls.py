from django.urls import path

from .views import (
    home_view,

    time_list_view,
    time_detail_view,
    time_form_view,
    time_confirm_delete_view,
    time_update_view,

    jogador_list_view,
    jogador_form_view,
    jogador_confirm_delete_view,
    jogador_update_view,
)


app_name = "core"


urlpatterns = [
    path("", home_view, name="home"),

    # Times
    path("times/", time_list_view, name="time_list"),
    path("times/<int:pk>/", time_detail_view, name="time_detail"),
    path("times/novo/", time_form_view, name="time_form"),
    path("times/<int:pk>/editar/", time_update_view, name="time_update"),
    path("times/<int:pk>/excluir/", time_confirm_delete_view, name="time_confirm_delete"),

    # Jogadores
    path("jogadores/", jogador_list_view, name="jogador_list"),
    path("jogadores/novo/", jogador_form_view, name="jogador_form"),
    path("jogadores/<int:pk>/editar/", jogador_update_view, name="jogador_update"),
    path("jogadores/<int:pk>/excluir/", jogador_confirm_delete_view, name="jogador_confirm_delete"),
]