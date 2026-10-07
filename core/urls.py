from django.urls import path
from .views import home_view, time_list_view, time_form_view, time_confirm_delete_view, time_update_view

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('times/', time_list_view, name='time_list'),
    path('times/new/', time_form_view, name='time_form'),
    path('times/<int:pk>/delete/', time_confirm_delete_view, name='time_confirm_delete'),
    path('times/<int:pk>/edit/', time_update_view, name='time_update'),
]