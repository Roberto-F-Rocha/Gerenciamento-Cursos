
from cursos.models import curso


class CursoService:

    def create(self, data):
        nome = data['nome']
        vagas = data['vagas']

        in_database = curso.objects.filter(
                nome=nome,
                vagas=vagas).exists()
        
        if in_database:
            raise ValueError
        else:
            nova_curso = curso.objects.create(
                nome=data['nome'],
                vagas=data['vagas'],
                titulo=data['titulo'],
                descricao=data['descricao'],
                categoria=data['categoria'],
                conteudo=data['conteudo'],
                disponivel=data['disponivel']
            )
            return nova_sala

    