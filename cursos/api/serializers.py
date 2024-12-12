from rest_framework import serializers
from cursos.models import curso, inscricao

class cursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = curso
        fields = '__all__'

class inscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = inscricao
        fields = '__all__'