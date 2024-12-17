import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, APIException
from rest_framework import status
from django.contrib.auth.models import Group
from django.db import IntegrityError
from users.models import aluno, Professor
from users.api.serializers import alunoSerializer, ProfessorSerializer, ProfessorCreateSerializer

logger = logging.getLogger("users")


class alunoViewSet(ModelViewSet):
    serializer_class = alunoSerializer
    permission_classes = [AllowAny]
    queryset = aluno.objects.all()

    def criar_aluno(self, request):
        try:
            serializer = alunoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                novo_aluno = aluno.objects.create(
                    nome=serializer.validated_data['nome'],
                    matricula=serializer.validated_data['matricula'],
                    user=serializer.validated_data['user']
                )
            except IntegrityError as e:
                logger.error("Erro de integridade ao cadastrar aluno: %s", str(e))
                return Response({"Info": "Erro ao cadastrar aluno. Matrícula ou usuário já existe."}, status=status.HTTP_409_CONFLICT)

            serializer_saida = alunoSerializer(novo_aluno)
            logger.info("Aluno cadastrado com sucesso: nome=%s, matrícula=%s", novo_aluno.nome, novo_aluno.matricula)
            return Response({"Info": "Cadastro do aluno realizado!", "data": serializer_saida.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning("Erro de validação ao cadastrar aluno: %s", str(e))
            return Response({"Info": "Dados inválidos fornecidos para cadastro do aluno."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Erro ao cadastrar aluno: %s", str(e))
            return Response({"Info": "Erro interno ao tentar cadastrar o aluno."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfessorViewSet(ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [AllowAny]
    queryset = Professor.objects.all()

    def criar_Professor(self, request):
        try:
            serializer = ProfessorCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                grupo_professores = Group.objects.get(name="Professores")
            except Group.DoesNotExist:
                logger.error("Grupo 'Professores' não encontrado.")
                return Response({"Info": "Grupo 'Professores' não encontrado. Verifique as configurações."}, status=status.HTTP_404_NOT_FOUND)

            try:
                novo_user = Professor.objects.create_user(
                    username=serializer.validated_data['login'],
                    password=serializer.validated_data['senha'],
                )
                novo_user.groups.add(grupo_professores)
            except IntegrityError as e:
                logger.error("Erro ao criar usuário para professor: %s", str(e))
                return Response({"Info": "Erro ao criar usuário. Nome de usuário já existe."}, status=status.HTTP_409_CONFLICT)

            novo_professor = Professor.objects.create(
                nome=serializer.validated_data['nome'],
                matricula=serializer.validated_data['matricula'],
                curso=serializer.validated_data['curso'],
                user=novo_user
            )

            serializer_saida = ProfessorSerializer(novo_professor)
            logger.info("Professor cadastrado com sucesso: nome=%s, matrícula=%s", novo_professor.nome, novo_professor.matricula)
            return Response({"Info": "Cadastro do professor realizado!", "data": serializer_saida.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning("Erro de validação ao cadastrar professor: %s", str(e))
            return Response({"Info": "Dados inválidos fornecidos para cadastro do professor."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Erro ao cadastrar professor: %s", str(e))
            return Response({"Info": "Erro interno ao tentar cadastrar o professor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False, url_path="buscar")
    def buscar_professor(self, request):
        try:
            busca = Professor.objects.all()
            serializer = ProfessorSerializer(busca, many=True)
            logger.info("Busca de professores realizada com sucesso.")
            return Response({"Info": "Lista de professores", "data": serializer.data}, status=status.HTTP_200_OK)
        except NotFound:
            logger.warning("Nenhum professor encontrado.")
            return Response({"Info": "Nenhum professor encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Erro ao buscar professores: %s", str(e))
            return Response({"Info": "Erro interno ao tentar buscar os professores."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
