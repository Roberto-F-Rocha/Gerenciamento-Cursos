from cursos.models import curso, inscricao
import logging

logger = logging.getLogger("cursos")

class CursoService:
    "Serviço para operações relacionadas a cursos."

    @staticmethod
    def create(data):
        "Cria um curso com os dados fornecidos."
        nome = data['nome']
        categoria = data['categoria']

        # Verifica se o curso já existe
        if curso.objects.filter(nome=nome, categoria=categoria).exists():
            logger.error(
                "Curso já cadastrado: nome=%s, categoria=%s", nome, categoria
            )
            raise ValueError("Curso já existe.")

        # Cria e retorna o curso
        novo_curso = curso.objects.create(
            nome=nome,
            vagas=data['vagas'],
            titulo=data['titulo'],
            descricao=data['descricao'],
            categoria=categoria,
            conteudo=data['conteudo']
        )
        logger.info("Curso cadastrado com sucesso: %s", novo_curso.nome)
        return novo_curso

class InscricaoService:
    "Serviço para operações relacionadas a inscrições."

    @staticmethod
    def create(data):
        "Cria uma inscrição com os dados fornecidos."
        aluno = data['aluno']
        curso_instance = data['curso']

        # Verifica se a inscrição já existe
        if inscricao.objects.filter(aluno=aluno, curso=curso_instance).exists():
            logger.error(
                "Inscrição já realizada: aluno=%s, curso=%s", aluno, curso_instance
            )
            raise ValueError("Inscrição já existe.")

        # Cria e retorna a inscrição
        nova_inscricao = inscricao.objects.create(
            aluno=aluno,
            curso=curso_instance,
            data=data['data']
        )
        logger.info(
            "Inscrição realizada com sucesso: aluno=%s, curso=%s", aluno, curso_instance
        )
        return nova_inscricao
