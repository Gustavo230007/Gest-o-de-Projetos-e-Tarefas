from django.shortcuts import render
from django.shortcuts import redirect

from .forms import TimeForm, JogadorForm
from .models import Time, Jogador

# Create your views here.
def home_view(request):
    return (
        render(request, template_name="home.html")
    )

def time_list_view(request):
    return (
        render(request, template_name="core/time_list.html", context={"times": Time.objects.all()})
    )

def time_form_view(request):
    if request.method == "POST":
        form = TimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:time_list")
    else:
        form = TimeForm()
    return (
        render(request, template_name="core/time_form.html", context={"form": form})
    )

def time_confirm_delete_view(request, pk):
    time = Time.objects.get(pk=pk)
    if request.method == "POST":
        time.delete()
        return redirect("core:time_list")
    
    return (
        render(request, template_name="core/time_confirm_delete.html", context={"time": time})
    )

def time_update_view(request, pk):
    time = Time.objects.get(pk=pk)
    if request.method == "POST":
        form = TimeForm(request.POST, instance=time)
        if form.is_valid():
            form.save()
            return redirect("core:time_list")
    else:
        form = TimeForm(instance=time)
    return (
        render(request, template_name="core/time_form.html", context={"form": form})
    )
    
def jogador_list_view(request):
    return (
        render(
            request,
            template_name="core/jogador_list.html",
            context={"jogadores": Jogador.objects.all()}
        )
    )


def jogador_form_view(request):
    if request.method == "POST":
        form = JogadorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("core:jogador_list")
    else:
        form = JogadorForm()

    return (
        render(
            request,
            template_name="core/jogador_form.html",
            context={"form": form}
        )
    )


def jogador_confirm_delete_view(request, pk):
    jogador = Jogador.objects.get(pk=pk)

    if request.method == "POST":
        jogador.delete()
        return redirect("core:jogador_list")

    return (
        render(
            request,
            template_name="core/jogador_confirm_delete.html",
            context={"jogador": jogador}
        )
    )


def jogador_update_view(request, pk):
    jogador = Jogador.objects.get(pk=pk)

    if request.method == "POST":
        form = JogadorForm(request.POST, instance=jogador)

        if form.is_valid():
            form.save()
            return redirect("core:jogador_list")
    else:
        form = JogadorForm(instance=jogador)

    return (
        render(
            request,
            template_name="core/jogador_form.html",
            context={"form": form}
        )
    )