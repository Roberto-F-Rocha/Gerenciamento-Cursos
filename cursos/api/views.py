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
from cursos.services import CursoService, InscricaoService

logger = logging.getLogger("cursos")

class CursoViewSet(ModelViewSet):
    "ViewSet para gerenciar cursos."
    serializer_class = cursoSerializer
    permission_classes = [IsAuthenticated]
    queryset = curso.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsProfessor()] or [IsAdminUser()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        "Cria um novo curso, verificando se ele já existe."
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Utiliza o serviço para criar o curso
            novo_curso = CursoService.create(data=serializer.validated_data)
            serializer_saida = cursoSerializer(novo_curso)
            
            return Response(
                {"Info": "Curso cadastrado!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            logger.error("Erro ao cadastrar curso: %s", str(e))
            return Response(
                {"Info": str(e)},
                status=status.HTTP_409_CONFLICT
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
        try:
            serializer = inscricaoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Utiliza o serviço para criar a inscrição
            nova_inscricao = InscricaoService.create(data=serializer.validated_data)
            serializer_saida = inscricaoSerializer(nova_inscricao)
            
            return Response(
                {"Info": "Inscrição realizada!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            logger.error("Erro ao realizar inscrição: %s", str(e))
            return Response(
                {"Info": str(e)},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            logger.exception("Erro ao realizar inscrição: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar realizar a inscrição."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
