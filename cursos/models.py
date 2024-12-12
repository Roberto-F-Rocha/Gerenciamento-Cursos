from django.db import models
from users.models import aluno
# Create your models here.
class curso(models.Model):
   nome = models.CharField(max_length=100)
   vagas = models.IntegerField()
   titulo = models.CharField(max_length=100)
   descricao = models.CharField(max_length=100)
   categoria = models.CharField(max_length=100)
   conteudo = models.TextField()

   def __str__(self):
      return self.nome
   
   class Meta:
      verbose_name = "Curso"
      verbose_name_plural = "Cursos"

class inscricao(models.Model):
   aluno = models.ForeignKey(aluno, on_delete=models.CASCADE)
   curso = models.ForeignKey(curso, on_delete=models.CASCADE)
   data = models.DateTimeField(auto_now_add=True)
   def __str__(self):
      return f'aluno {self.aluno.nome} +  foi incrito em  + {self.curso.nome}'
   
   class Meta:
      verbose_name = "Inscrição"
      verbose_name_plural = "Inscrições"