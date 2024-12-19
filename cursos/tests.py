from django.test import TestCase
from rest_framework import status
from cursos.models import curso
from django.contrib.auth.models import User


from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Create your tests here.

class CursoTesteCase(TestCase):

    def setUp(self):
        self.novo_curso = curso.objects.create(
            nome="Curso de Django",
            vagas=20,
            titulo="Introdução ao Django",
            descricao="Curso básico para iniciantes em programação",
            categoria="Programação",
            conteudo="Variáveis, Loops, Funções e Estruturas de Dados",
            disponivel =True
        )
        
        self.new_user = User.objects.create_user(username="admin",password="adminadmin")
        self.new_user.is_staff = True
        self.new_user.is_superuser = True
        self.new_user.save()
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


    def test_cadastrar_cursos(self):
        url = "http://localhost:8000/cursos/"
        data = {
            "nome": "Curso de Django",
            "vagas": 20,
            "titulo": "Desenvolvimento Web com Django",
            "descricao": "Aprenda a criar aplicações web usando Django",
            "categoria": "Programação",
            "conteudo": "Introdução ao Django",
            "disponivel": True
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
            conteudo="Variáveis, Loops, Funções e Estruturas de Dados",
            disponivel=True
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nome'], "Curso de Django")
        self.assertEqual(response.data[0]['vagas'], 20)
        
    def test_atualizar_cursos(self):
        url = f"http://localhost:8000/cursos/{self.novo_curso.id}/"
        curso.objects.create(
            nome="Curso de Django",
            vagas=20,
            titulo="Introdução ao Django",
            descricao="Curso básico para iniciantes em programação",
            categoria="Programação",
            conteudo="Variáveis, Loops, Funções e Estruturas de Dados",
            disponivel=True
        )
        
    def test_atualizar_parcialmente_cursos(self):
        url = f"http://localhost:8000/cursos/{self.novo_curso.id}/"
        data = {
            "disponivel": False
        }
        response = self.client.patch(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.novo_curso.refresh_from_db()
        self.assertEqual(self.novo_curso.disponivel, False)
        
    def test_deletar_cursos(self):
        url = f"http://localhost:8000/cursos/{self.novo_curso.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(curso.objects.filter(id=self.novo_curso.id).exists())