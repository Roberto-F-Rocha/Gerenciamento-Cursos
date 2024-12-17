# Gerenciamento de Cursos - API

## Descrição do Projeto
Este projeto consiste em uma API para gerenciamento de cursos e inscrições, desenvolvida em Django com suporte para operações de CRUD e autenticação. A API foi projetada para facilitar o registro, busca e inscrição de usuários em cursos.

---

## Tecnologias Utilizadas
- **Django**: Framework web principal.
- **Django REST Framework (DRF)**: Para construção da API.
- **Insomnia**: Ferramenta para testes de API.
- **SQLite**: Banco de dados padrão para desenvolvimento local.

---

## Instalação e Configuração

### 1. Clonar o Repositório
```bash
$ git clone <https://github.com/mmvbs/gerenciamento_de_curso.git>
$ cd gerenciamento_de_curso
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ venv\Scripts\activate  # Windows
```

### 3. Instalar as Dependências
```bash
$ pip install -r requirements.txt
```

### 4. Rodar Migrações
```bash
$ python manage.py migrate
```

### 5. Rodar o Servidor
```bash
$ python manage.py runserver
```

O servidor estará acessível em `http://127.0.0.1:8000/`.

---

## Endpoints Disponíveis

### **Cursos**
- **Criar Curso**: POST `/cursos/`
- **Listar Cursos**: GET `/cursos/buscar/`

### **Inscrições**
- **Criar Inscrição**: POST `/inscricoes/`
  - **Nota**: Requer autenticação.

---

## Testando com o Insomnia

### Configuração de Requisições
1. Abra o Insomnia.
2. Crie uma nova "Workspace".
3. Configure os endpoints mencionados acima.
   - Para autenticação (Inscrições): Adicione um cabeçalho **Authorization** com o valor `Bearer <seu_token>`.

---

## Try-Exception Implementados

### Cursos
- Validação de dados antes da criação de um curso para evitar duplicidade.
- Mensagens de erro e logs ao tentar cadastrar um curso já existente.

### Inscrições
- Validação de dados antes de criar uma inscrição.
- Tratamento de erro para inscrições duplicadas.

---

## Loggers
Logs são gerados automaticamente para registrar:
- Sucessos nas operações de criação (cursos e inscrições).
- Erros durante o processamento de requisições.

---

## Autenticação
A autenticação é necessária para criar inscrições. Para obter um token de autenticação, é necessário implementar ou utilizar um 
endpoint de login (não incluído neste exemplo).

---

## Atualizações na Estrutura Central do Projeto
- Exclusão da pasta gerenciamento_de_curso duplicada: Consolidamos todo o conteúdo em uma única pasta para evitar redundâncias e facilitar o gerenciamento dos arquivos relacionados ao curso. Essa ação garante uma organização mais eficiente e reduz a possibilidade de conflitos futuros.

- Exclusão da pasta config duplicada: Assim como no caso anterior, mantivemos apenas uma instância da pasta config, centralizando todas as configurações em um único local. Isso simplifica a navegação e a manutenção do projeto.

- Reorganização do arquivo manage.py: O arquivo manage.py foi movido para o diretório correto, assegurando o funcionamento adequado do ambiente de desenvolvimento. Essa mudança também alinha a estrutura do projeto às práticas recomendadas para projetos baseados em frameworks como Django.

## Tratamento de Vulnerabilidades
- *Uso do arquivo .env:*
Variáveis sensíveis, como SECRET_KEY, DEBUG, ALLOWED_HOSTS e SENTRY_DSN, foram movidas para o arquivo .env. Isso garante que essas configurações não fiquem expostas no código-fonte.
- *Segurança das configurações:*
Todas as informações sensíveis foram removidas do código principal e agora estão armazenadas de forma segura no .env, utilizando a biblioteca python-decouple.

### Dependências Instaladas
Para implementar essas mudanças, foi necessário instalar as seguintes bibliotecas:

- python-decouple:
Para gerenciar as variáveis de ambiente e carregar as configurações do arquivo .env.

```bash
$ pip install python-decouple
```
- sentry-sdk (opcional):
Para integração com o Sentry, caso seja utilizado para monitoramento de erros e desempenho.

```bash
$ pip install sentry-sdk
```