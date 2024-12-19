import logging
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from cursos.models import curso, inscricao
from cursos.api.serializers import cursoSerializer, inscricaoSerializer

logger = logging.getLogger("cursos")

class cursoViewSet(ModelViewSet):
    serializer_class = cursoSerializer
    permission_classes = [AllowAny]
    queryset = curso.objects.all()

    def create(self, request):
        serializer = None
        nome = categoria = None
        try:
            serializer = cursoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            nome = serializer.validated_data['nome']
            categoria = serializer.validated_data['categoria']

            if curso.objects.filter(nome=nome, categoria=categoria).exists():
                logger.error("Curso já cadastrado: nome=%s, categoria=%s", nome, categoria)
                return Response({"Info": "Falha ao tentar cadastrar o curso! Curso já existe."}, status=status.HTTP_409_CONFLICT)

            novo_curso = curso.objects.create(
                nome=nome,
                vagas=serializer.validated_data['vagas'],
                titulo=serializer.validated_data['titulo'],
                descricao=serializer.validated_data['descricao'],
                categoria=categoria,
                conteudo=serializer.validated_data['conteudo']
            )

            serializer_saida = cursoSerializer(novo_curso)
            logger.info("Curso cadastrado com sucesso: %s", novo_curso.nome)
            return Response({"Info": "Curso cadastrado!", "data": serializer_saida.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Erro ao cadastrar curso: %s", str(e))
            return Response({"Info": "Erro interno ao tentar cadastrar o curso."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False, url_path="buscar")
    def buscar_cursos(self, request):
        try:
            busca = curso.objects.all()
            serializer = cursoSerializer(busca, many=True)
            return Response({"Info": "Lista de cursos", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Erro ao buscar cursos: %s", str(e))
            return Response({"Info": "Erro interno ao tentar buscar os cursos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class inscricaoViewSet(ModelViewSet):
    serializer_class = inscricaoSerializer
    permission_classes = [IsAuthenticated]
    queryset = inscricao.objects.all()

    def create(self, request):
        serializer = None
        aluno = curso_instance = None
        try:
            serializer = inscricaoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            aluno = serializer.validated_data['aluno']
            curso_instance = serializer.validated_data['curso']

            if inscricao.objects.filter(aluno=aluno, curso=curso_instance).exists():
                logger.error("Inscrição já realizada: aluno=%s, curso=%s", aluno, curso_instance)
                return Response({"Info": "Falha ao tentar realizar a inscrição! Inscrição já existe."}, status=status.HTTP_409_CONFLICT)

            nova_inscricao = inscricao.objects.create(
                aluno=aluno,
                curso=curso_instance,
                data=serializer.validated_data['data']
            )

            serializer_saida = inscricaoSerializer(nova_inscricao)
            logger.info("Inscrição realizada com sucesso: aluno=%s, curso=%s", aluno, curso_instance)
            return Response({"Info": "Inscrição realizada!", "data": serializer_saida.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Erro ao realizar inscrição: %s", str(e))
            return Response({"Info": "Erro interno ao tentar realizar a inscrição."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
