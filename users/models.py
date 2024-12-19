from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class aluno(models.Model):
    nome = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=10)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

class Professor(models.Model):

    nome = models.CharField(max_length=140)
    matricula = models.CharField(max_length=12)
    curso = models.CharField(max_length=140)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"