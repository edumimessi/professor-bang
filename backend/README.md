# APPDUDA / Professor Bang — Backend Corrigido

**Autor da correção:** Manus AI  
**Status:** MVP backend FastAPI corrigido, importável, testado e pronto para versionamento.

Este diretório contém a versão corrigida do backend enviado em `APPDUDA.ZIP`. A correção transformou os arquivos originais em uma aplicação FastAPI executável, com estrutura de pacote válida, banco de dados funcional, modelos ORM, schemas Pydantic, dependências declaradas, teste de smoke e documentação mínima para continuidade do desenvolvimento.

## Resumo da correção

O pacote original continha uma lógica pedagógica promissora, mas não conseguia executar porque dependia de arquivos ausentes, como `database.py`, `models.py` e `schemas.py`, além de não conter `requirements.txt` nem estrutura de pacote completa. A versão corrigida preserva a proposta original e acrescenta as camadas necessárias para que a API possa ser importada, documentada e testada.

| Área | Antes | Depois |
|---|---|---|
| Estrutura | Arquivos soltos com imports quebrados | Pacote `app/` com `routes/`, `services/`, modelos, schemas e banco |
| Banco de dados | Dependência ausente | SQLAlchemy com SQLite local e suporte a `DATABASE_URL` |
| API | Rotas parcialmente existentes | Rotas importáveis em `app.main:app` |
| Validação | Schemas ausentes | Schemas Pydantic para entrada e resposta |
| Testes | Ausentes | Teste de smoke cobrindo fluxo principal |
| CORS | Origem ampla fixa com `*` | Origens configuráveis por `ALLOWED_ORIGINS` |
| Motor pedagógico | Detectava alguns travamentos, mas não acionava apoio no primeiro bloqueio | Modo apoio acionado quando há frase explícita de travamento |

## Estrutura do projeto

```text
backend/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── parents.py
│   │   ├── routine.py
│   │   ├── sessions.py
│   │   └── students.py
│   └── services/
│       ├── __init__.py
│       └── ai_pedagogy.py
├── tests/
│   └── test_smoke_api.py
├── .env.example
├── requirements.txt
└── README.md
```

## Como executar localmente

Recomenda-se criar um ambiente virtual antes de instalar as dependências. A execução abaixo parte do diretório `backend/`.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Depois de iniciar o servidor, a documentação automática estará disponível nos caminhos abaixo.

| Recurso | URL local |
|---|---|
| Health check | `http://localhost:8000/health` |
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

## Como rodar os testes

O teste de smoke usa `FastAPI TestClient` e recria um banco SQLite de teste. Ele cobre criação de perfil, sessão de estudo, boas-vindas, mensagem de chat com travamento, histórico, check-in emocional, rotina, conquista, encerramento de sessão e relatório dos responsáveis.

```bash
pytest -q
```

Na validação realizada durante a correção, o teste principal foi executado com sucesso.

```text
1 passed
```

## Variáveis de ambiente

| Variável | Exemplo | Finalidade |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./professor_bang.db` | Define o banco de dados usado pela aplicação |
| `ALLOWED_ORIGINS` | `http://localhost,http://localhost:3000` | Define as origens permitidas no CORS |
| `ENV` | `development` | Indica o ambiente de execução |

Para produção, substitua o SQLite por PostgreSQL e configure `ALLOWED_ORIGINS` apenas com os domínios reais do frontend.

## Endpoints principais

| Método | Caminho | Finalidade |
|---|---|---|
| `GET` | `/health` | Verifica se a API está online |
| `POST` | `/students/` | Cria perfil pedagógico da aluna |
| `GET` | `/students/` | Lista perfis cadastrados |
| `POST` | `/sessions/start` | Inicia sessão de estudo |
| `PUT` | `/sessions/{session_id}/end` | Encerra sessão de estudo |
| `POST` | `/chat/welcome` | Gera mensagem de boas-vindas |
| `POST` | `/chat/message` | Envia mensagem da aluna e recebe resposta pedagógica |
| `GET` | `/chat/{session_id}/history` | Lista histórico da sessão |
| `POST` | `/chat/{session_id}/checkin` | Salva check-in emocional |
| `GET` | `/routine/{student_id}/today` | Lista ou cria rotina diária |
| `PUT` | `/routine/task/{task_id}/toggle` | Marca/desmarca tarefa da rotina |
| `GET` | `/achievements/{student_id}` | Lista conquistas |
| `POST` | `/achievements/{student_id}` | Registra conquista |
| `GET` | `/parents/{student_id}/report` | Gera relatório semanal para responsáveis |

## Observações importantes de segurança e privacidade

Este backend lida com dados pedagógicos e emocionais de uma adolescente. Por isso, antes de uso real, é necessário implementar autenticação, autorização por responsável, trilha de auditoria, consentimento, política de retenção e criptografia adequada de dados sensíveis. A versão atual é um MVP técnico para desenvolvimento local e validação funcional.

Também é recomendável substituir os parâmetros sensíveis enviados por query string em alguns endpoints por corpos JSON tipados. Essa mudança melhora clareza, testabilidade e reduz exposição acidental em logs de servidor.

## Próximas melhorias recomendadas

| Prioridade | Melhoria | Motivo |
|---|---|---|
| Alta | Adicionar autenticação e autorização | Proteger dados de menor de idade e separar acesso da aluna/responsáveis |
| Alta | Migrar para PostgreSQL em produção | Melhor confiabilidade, concorrência e backup |
| Alta | Criar migrations com Alembic | Controlar evolução do schema com segurança |
| Média | Trocar query string por payload JSON em check-ins e conquistas | Reduzir exposição de informações em logs |
| Média | Ampliar testes de unidade do motor pedagógico | Garantir respostas seguras e consistentes |
| Média | Criar integração com frontend Flutter | Validar o fluxo completo do produto |
| Baixa | Adicionar CI no GitHub Actions | Automatizar validação a cada commit |

## Diferenças pedagógicas preservadas

A correção manteve o motor pedagógico local como componente separado em `app/services/ai_pedagogy.py`. Essa separação permite substituir futuramente a lógica hardcoded por integração com IA real, sem reescrever as rotas do chat. A detecção de travamento foi ajustada para responder de forma acolhedora já no primeiro sinal explícito de bloqueio, como “não entendi” ou “estou travada”.

## Comando de validação usado

```bash
python3.11 -m py_compile app/*.py app/routes/*.py app/services/*.py
python3.11 -m pytest -q tests/test_smoke_api.py
```

O backend corrigido está pronto para ser empacotado ou enviado ao repositório GitHub do projeto.
