"Gerencia o CRUD para cursos e incricoes"
import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from cursos.models import curso, inscricao
from cursos.api.serializers import cursoSerializer, inscricaoSerializer

from users.api.permissions import IsProfessor
from cursos.services import CursoService

logger = logging.getLogger("cursos")


class CursoViewSet(ModelViewSet):
    "ViewSet para gerenciar cursos."
    serializer_class = cursoSerializer
    permission_classes = [IsAuthenticated]
    queryset = curso.objects.all()
    service = CursoService()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsProfessor()] or [IsAdminUser()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        "Cria um novo curso, verificando se ele já existe."
        serializer = None
        nome = categoria = None
        
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                novo_curso = self.service.create(data=serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            novo_curso = self.service.create(data=serializer.validated_data)
            
            serializer = cursoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            nome = serializer.validated_data['nome']
            categoria = serializer.validated_data['categoria']

            if curso.objects.filter(nome=nome, categoria=categoria).exists():
                logger.error(
                    "Curso já cadastrado: nome=%s, categoria=%s", nome, categoria
                )
                return Response(
                    {"Info": "Falha ao tentar cadastrar o curso! Curso já existe."},
                    status=status.HTTP_409_CONFLICT
                )

            novo_curso = curso.objects.create(
                nome=nome,
                vagas=serializer.validated_data['vagas'],
                titulo=serializer.validated_data['titulo'],
                descricao=serializer.validated_data['descricao'],
                categoria=categoria,
                conteudo=serializer.validated_data['conteudo']
            )

            serializer_saida = cursoSerializer(novo_curso)
            logger.info(
                "Curso cadastrado com sucesso: %s", novo_curso.nome
            )
            return Response(
                {"Info": "Curso cadastrado!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception("Erro ao cadastrar curso: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar cadastrar o curso."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['get'], detail=False, url_path="buscar")
    def buscar_cursos(self):
        "Endpoint customizado para buscar todos os cursos."
        try:
            busca = curso.objects.all()
            serializer = cursoSerializer(busca, many=True)
            return Response(
                {"Info": "Lista de cursos", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception("Erro ao buscar cursos: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar buscar os cursos."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InscricaoViewSet(ModelViewSet):
    "ViewSet para gerenciar inscrições."
    serializer_class = inscricaoSerializer
    permission_classes = [IsAuthenticated]
    queryset = inscricao.objects.all()

    def create(self, request, *args, **kwargs):
        "Cria uma inscrição, verificando se ela já existe."
        serializer = None
        aluno = curso_instance = None
        try:
            serializer = inscricaoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            aluno = serializer.validated_data['aluno']
            curso_instance = serializer.validated_data['curso']

            if inscricao.objects.filter(aluno=aluno, curso=curso_instance).exists():
                logger.error(
                    "Inscrição já realizada: aluno=%s, curso=%s", aluno, curso_instance
                )
                return Response(
                    {"Info": "Falha ao tentar realizar a inscrição! Inscrição já existe."},
                    status=status.HTTP_409_CONFLICT
                )

            nova_inscricao = inscricao.objects.create(
                aluno=aluno,
                curso=curso_instance,
                data=serializer.validated_data['data']
            )

            serializer_saida = inscricaoSerializer(nova_inscricao)
            logger.info(
                "Inscrição realizada com sucesso: aluno=%s, curso=%s", aluno, curso_instance
            )
            return Response(
                {"Info": "Inscrição realizada!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception("Erro ao realizar inscrição: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar realizar a inscrição."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
