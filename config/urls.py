"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from users.api.views import alunoViewSet
from cursos.api.views import cursoViewSet, inscricaoViewSet
from users.api.views import ProfessorViewSet


router = SimpleRouter()
router.register("alunos", alunoViewSet, basename="alunos")
router.register("cursos", cursoViewSet, basename="cursos")
router.register("professores",ProfessorViewSet, basename="professores")
router.register("inscricoes", inscricaoViewSet, basename="inscricoes")

urlpatterns = [
    path('admin/', admin.site.urls),
]+router.urls
