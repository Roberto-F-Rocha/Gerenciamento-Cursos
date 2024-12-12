from django.contrib import admin
from cursos.models import curso, inscricao
from users.models import aluno, Professor
# Register your models here.

admin.site.register(aluno)
admin.site.register(Professor)
admin.site.register(inscricao)
admin.site.register(curso)