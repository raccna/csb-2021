from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flaw-1', views.flaw1, name='flaw-1'),
    path('flaw-2', views.flaw2, name='flaw-2'),
    path('flaw-3', views.flaw3, name='flaw-3'),
    path('flaw-4', views.flaw4, name='flaw-4'),
    path('flaw-5', views.flaw5, name='flaw-5'),
    path('fix-1', views.fix1, name='fix-1'),
    path('fix-2', views.fix2, name='fix-2'),
    path('fix-3', views.fix3, name='fix-3'),
    path('fix-4', views.fix4, name='fix-4'),
    path('fix-5', views.fix5, name='fix-5'),
]