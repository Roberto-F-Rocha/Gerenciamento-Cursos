from django.db import models
from rest_framework import serializers
from users.models import aluno, Professor
from django.contrib.auth.models import User
class alunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = aluno
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Professor
        fields = ['nome', 'matricula', 'curso', 'user', 'login', 'senha']

class ProfessorCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=140)
    matricula = serializers.CharField(max_length=12)
    curso = serializers.CharField(max_length=140)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login = serializers.CharField(max_length=100)
    senha = serializers.CharField(max_length=100)