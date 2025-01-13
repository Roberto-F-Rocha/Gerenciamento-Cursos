import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from django.contrib.auth.models import Group
from django.db import IntegrityError
from users.models import aluno, Professor
from users.api.permissions import IsProfessor
from users.api.serializers import alunoSerializer, ProfessorSerializer, ProfessorCreateSerializer
from users.services import ProfessorService

logger = logging.getLogger("users")


class AlunoViewSet(ModelViewSet):
    serializer_class = alunoSerializer
    permission_classes = [AllowAny]
    queryset = aluno.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            alunos = self.get_queryset()
            serializer = self.get_serializer(alunos, many=True)
            logger.info("Lista de alunos recuperada com sucesso.")
            return Response(
                {"Info": "Lista de alunos", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.exception("Erro ao listar alunos: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar listar os alunos."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info("Aluno cadastrado com sucesso: %s", serializer.data)
            return Response(
                {"Info": "Cadastro do aluno realizado!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError as e:
            logger.error("Erro de integridade ao cadastrar aluno: %s", str(e))
            return Response(
                {"Info": "Erro ao cadastrar aluno. Matrícula ou usuário já existe."},
                status=status.HTTP_409_CONFLICT,
            )
        except ValidationError as e:
            logger.warning("Erro de validação ao cadastrar aluno: %s", str(e))
            return Response(
                {"Info": "Dados inválidos fornecidos para cadastro do aluno."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.exception("Erro ao cadastrar aluno: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar cadastrar o aluno."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info("Aluno deletado com sucesso: %s", instance.id)
            return Response(
                {"Info": "Aluno deletado com sucesso!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except NotFound:
            logger.warning("Aluno não encontrado para exclusão.")
            return Response(
                {"Info": "Aluno não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception("Erro ao deletar aluno: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar deletar o aluno."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info("Aluno atualizado com sucesso: %s", instance.id)
            return Response(
                {"Info": "Aluno atualizado com sucesso!", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            logger.warning("Erro de validação ao atualizar aluno: %s", str(e))
            return Response(
                {"Info": "Dados inválidos fornecidos para atualização do aluno."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotFound:
            logger.warning("Aluno não encontrado para atualização.")
            return Response(
                {"Info": "Aluno não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception("Erro ao atualizar aluno: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar atualizar o aluno."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfessorViewSet(ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [AllowAny]
    queryset = Professor.objects.all()
    service = ProfessorService()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsProfessor()]
        elif self.action == 'list':
            return [IsAdminUser()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        try:
            professores = self.get_queryset()
            serializer = self.get_serializer(professores, many=True)
            logger.info("Lista de professores recuperada com sucesso.")
            return Response(
                {"Info": "Lista de professores", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.exception("Erro ao listar professores: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar listar os professores."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = ProfessorCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Verificar e adicionar ao grupo "Professores"
            try:
                grupo_professores = Group.objects.get(name="Professores")
            except Group.DoesNotExist:
                logger.error("Grupo 'Professores' não encontrado.")
                return Response(
                    {"Info": "Grupo 'Professores' não encontrado. Verifique as configurações."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Criar usuário associado ao professor
            try:
                novo_user = Professor.objects.create_user(
                    username=serializer.validated_data["login"],
                    password=serializer.validated_data["senha"],
                )
                novo_user.groups.add(grupo_professores)
            except IntegrityError as e:
                logger.error("Erro ao criar usuário para professor: %s", str(e))
                return Response(
                    {"Info": "Erro ao criar usuário. Nome de usuário já existe."},
                    status=status.HTTP_409_CONFLICT,
                )

            # Criar o professor no sistema
            novo_professor = self.service.create(serializer.validated_data)
            serializer_saida = ProfessorSerializer(novo_professor)

            logger.info("Professor cadastrado com sucesso: %s", serializer_saida.data)
            return Response(
                {"Info": "Cadastro do professor realizado!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            logger.warning("Erro de validação ao cadastrar professor: %s", str(e))
            return Response(
                {"Info": "Dados inválidos fornecidos para cadastro do professor."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.exception("Erro ao cadastrar professor: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar cadastrar o professor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info("Professor deletado com sucesso: %s", instance.id)
            return Response(
                {"Info": "Professor deletado com sucesso!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except NotFound:
            logger.warning("Professor não encontrado para exclusão.")
            return Response(
                {"Info": "Professor não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception("Erro ao deletar professor: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar deletar o professor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info("Professor atualizado com sucesso: %s", instance.id)
            return Response(
                {"Info": "Professor atualizado com sucesso!", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            logger.warning("Erro de validação ao atualizar professor: %s", str(e))
            return Response(
                {"Info": "Dados inválidos fornecidos para atualização do professor."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotFound:
            logger.warning("Professor não encontrado para atualização.")
            return Response(
                {"Info": "Professor não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception("Erro ao atualizar professor: %s", str(e))
            return Response(
                {"Info": "Erro interno ao tentar atualizar o professor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )