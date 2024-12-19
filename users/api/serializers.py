from rest_framework import serializers
from users.models import aluno, Professor
class alunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = aluno
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Professor
        fields = "__all__"

class ProfessorCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=140)
    matricula = serializers.CharField(max_length=12)
    curso = serializers.CharField(max_length=140)
    login = serializers.CharField(max_length=100)
    senha = serializers.CharField(max_length=100)

    