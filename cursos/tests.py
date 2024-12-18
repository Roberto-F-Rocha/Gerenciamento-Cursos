from django.test import TestCase
from rest_framework import status
from cursos.models import curso

# Create your tests here.

class CursoTesteCase(TestCase):

    def setUp(self):
        pass

    def test_cadastrar_cursos(self):
        url = "http://localhost:8000/cursos/"
        data = {
            "nome": "Curso de Django",
            "vagas": 20,
            "titulo": "Desenvolvimento Web com Django",
            "descricao": "Aprenda a criar aplicações web usando Django",
            "categoria": "Programação",
            "conteudo": "Introdução ao Django"
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(curso.objects.filter(nome="Curso de Django").exists())

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_listar_cursos(self):
        url = "http://localhost:8000/cursos/"
        curso.objects.create(
            nome="Curso de Django",
            vagas=20,
            titulo="Introdução ao Django",
            descricao="Curso básico para iniciantes em programação",
            categoria="Programação",
            conteudo="Variáveis, Loops, Funções e Estruturas de Dados"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nome'], "Curso de Django")
        self.assertEqual(response.data[0]['vagas'], 20)