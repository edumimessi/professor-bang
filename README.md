# Professor Bang — MVP pedagógico adaptativo

**Autor:** Manus AI  
**Stack:** Flutter, FastAPI, SQLite, SQLAlchemy e arquitetura preparada para PostgreSQL e integração futura com IA real.

## Visão geral

O **Professor Bang** é um MVP de professor de reforço com apoio pedagógico adaptativo. O projeto foi desenhado para apoiar uma adolescente com dificuldades cognitivas, ansiedade escolar, rigidez comportamental, dificuldade de abstração e baixa autonomia executiva. O aplicativo utiliza uma identidade original e genérica, sem imagem, voz, nome artístico real, marca registrada ou identidade visual oficial de artistas ou grupos.

> O objetivo central do MVP não é criar apenas um chatbot, mas um **sistema pedagógico adaptativo** que acolhe, divide tarefas em partes pequenas, oferece pistas antes de respostas e incentiva autonomia.

A versão atual já integra o **backend FastAPI corrigido** ao projeto principal e ajusta o **frontend Flutter** para consumir a API por meio de `API_BASE_URL`. Flutter é uma tecnologia multiplataforma usada para criar aplicativos a partir de uma única base de código, enquanto FastAPI é um framework Python moderno para criação de APIs baseado em tipagem e documentação automática.[1] [2]

## Arquitetura atual

A arquitetura foi organizada em três camadas para facilitar manutenção, evolução e teste no celular. O frontend Flutter concentra experiência visual, navegação e interação pedagógica. O backend FastAPI concentra persistência, rotas REST e regras de domínio. A camada pedagógica fica isolada em serviço próprio para permitir substituição gradual do motor local por uma IA real estruturada em JSON.

| Camada | Responsabilidade | Implementação atual | Evolução planejada |
|---|---|---|---|
| **Frontend Flutter** | Telas, botões grandes, tema calmo, perfil, chat, rotina e painel dos pais. | Arquivos em `frontend_flutter/lib`, com `ApiService` conectado ao backend. | Gerar pastas nativas com `flutter create .`, testar em Android/iOS e ampliar acessibilidade. |
| **Backend FastAPI** | API REST, modelos de dados, rotas, CORS e persistência. | Arquivos em `backend/app`, usando SQLAlchemy e SQLite. | Migrar para PostgreSQL via `DATABASE_URL` sem reescrever a lógica principal. |
| **Serviço pedagógico** | Detectar travamento, gerar respostas curtas e estruturadas. | `backend/app/services/ai_pedagogy.py`, com modo apoio acionado por sinais explícitos. | Substituir ou complementar por OpenAI API retornando JSON validado. |
| **Banco de dados** | Registrar perfil, sessões, mensagens, rotina, check-ins e conquistas. | SQLite local criado automaticamente pelo backend. | PostgreSQL, autenticação, criptografia, backups e políticas de retenção. |

## Estrutura de pastas

```text
professor_bang/
├── README.md
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── parents.py
│   │   │   ├── routine.py
│   │   │   ├── sessions.py
│   │   │   └── students.py
│   │   └── services/
│   │       └── ai_pedagogy.py
│   └── tests/
│       └── test_smoke_api.py
└── frontend_flutter/
    ├── README_MOBILE.md
    ├── pubspec.yaml
    └── lib/
        ├── main.dart
        ├── app/
        ├── models/
        ├── services/
        ├── screens/
        └── widgets/
```

## Funcionalidades implementadas

O MVP contém as telas essenciais solicitadas e foi organizado para que cada parte seja compreensível para uma pessoa iniciante. As respostas pedagógicas são curtas, acolhedoras e orientadas por passos. O modo de apoio é ativado quando a aluna demonstra travamento por frases como “não sei”, “não consigo”, “travei”, “não entendi” ou “estou travada”.

| Funcionalidade | Status | Arquivos principais |
|---|---:|---|
| Tela inicial com mensagem acolhedora e botões grandes | Implementada | `home_screen.dart`, `big_menu_button.dart`, `calm_scaffold.dart` |
| Perfil da aluna com campos pedagógicos e emocionais | Conectado ao backend | `profile_screen.dart`, `student_profile.dart`, `app_state.dart`, `/students/` |
| Modos de estudo | Implementados | `study_modes_screen.dart`, `chat_screen.dart` |
| Chat pedagógico | Conectado ao backend | `chat_screen.dart`, `api_service.dart`, `/chat/message` |
| Criação automática de sessão de estudo | Implementada | `app_state.dart`, `/sessions/start` |
| Detecção de travamento e Modo Apoio | Implementados | `ai_pedagogy.py` |
| Checklist de rotina | Backend implementado | `routine.py`, `/routine/{student_id}/today` |
| Painel dos pais | Backend implementado | `parents.py`, `/parents/{student_id}/report` |
| Microvitórias sem ranking | Backend implementado | `routine.py`, `/achievements/{student_id}` |
| Teste de smoke da API | Implementado e validado | `tests/test_smoke_api.py` |

## Como rodar o backend

Entre na pasta do backend e instale as dependências. O SQLite será criado automaticamente no primeiro carregamento da aplicação.

```bash
cd professor_bang/backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em `http://localhost:8000`. A documentação automática poderá ser acessada em `http://localhost:8000/docs`, recurso fornecido pelo ecossistema FastAPI/OpenAPI.[2]

## Como validar o backend

O backend corrigido possui teste de smoke para confirmar importação da aplicação, criação de perfil, sessão e resposta pedagógica com modo apoio.

```bash
cd professor_bang/backend
pytest -q
```

O resultado esperado é:

```text
1 passed
```

## Como rodar o app no celular

A pasta `frontend_flutter` contém a aplicação Flutter conectada ao backend por `API_BASE_URL`. Como o ambiente de geração não possuía Flutter SDK instalado, as pastas nativas Android/iOS devem ser geradas localmente em uma máquina com Flutter configurado.[1]

```bash
cd professor_bang/frontend_flutter
flutter create .
flutter pub get
```

Para emulador Android, use o endereço especial `10.0.2.2`, que aponta para o `localhost` do computador:

```bash
flutter run -d android --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

Para celular físico Android ou iPhone, coloque o celular e o computador na mesma rede Wi-Fi, descubra o IP local do computador e execute:

```bash
flutter run -d <id_do_dispositivo> --dart-define=API_BASE_URL=http://SEU_IP_LOCAL:8000
```

Exemplo:

```bash
flutter run -d R58N123ABC --dart-define=API_BASE_URL=http://192.168.0.25:8000
```

O passo a passo detalhado está em [`frontend_flutter/README_MOBILE.md`](frontend_flutter/README_MOBILE.md).

## Endpoints principais

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/health` | Verificar se a API está online. |
| `POST` | `/students/` | Criar perfil da aluna. |
| `GET` | `/students/{student_id}` | Buscar perfil da aluna. |
| `POST` | `/sessions/start` | Iniciar sessão de estudo. |
| `PUT` | `/sessions/{session_id}/end` | Encerrar sessão de estudo. |
| `POST` | `/chat/message` | Enviar mensagem ao tutor pedagógico. |
| `GET` | `/chat/{session_id}/history` | Consultar histórico de uma sessão. |
| `POST` | `/chat/{session_id}/checkin` | Registrar check-in emocional. |
| `GET` | `/routine/{student_id}/today` | Consultar rotina do dia. |
| `GET` | `/achievements/{student_id}` | Consultar microvitórias. |
| `GET` | `/parents/{student_id}/report` | Consultar relatório dos responsáveis. |

## Banco de dados

O backend cria as tabelas principais por meio de SQLAlchemy. A URL padrão é SQLite, mas a arquitetura aceita PostgreSQL por variável de ambiente. SQLAlchemy permite alternar bancos relacionais por configuração de engine e dialeto, mantendo os modelos de domínio no código Python.[3]

| Tabela | Finalidade |
|---|---|
| `student_profiles` | Dados mínimos do perfil pedagógico da aluna. |
| `study_sessions` | Sessões de estudo e modos utilizados. |
| `messages` | Mensagens do estudante e do assistente pedagógico. |
| `emotional_checkins` | Registros simples de estado emocional. |
| `routine_tasks` | Checklist de rotina de estudo. |
| `achievements` | Microvitórias sem ranking. |

Para usar PostgreSQL futuramente:

```bash
export DATABASE_URL="postgresql+psycopg://usuario:senha@localhost:5432/professor_bang"
```

## Segurança, privacidade e LGPD

O MVP foi desenhado com princípio de minimização de dados: coleta apenas informações pedagógicas necessárias para personalização local. O aplicativo inclui limites educacionais claros e não deve ser tratado como substituto de escola, psicopedagoga, psicóloga ou médico. A LGPD brasileira estabelece princípios como finalidade, adequação, necessidade e segurança no tratamento de dados pessoais.[4]

| Princípio | Aplicação no MVP | Requisito antes de produção |
|---|---|---|
| **Necessidade** | Armazenar somente dados úteis para apoio pedagógico. | Revisar campos e política de retenção. |
| **Controle de acesso** | Ainda não há autenticação no MVP local. | Implementar login dos responsáveis e autorização por aluna. |
| **Transparência** | Documentar limites educacionais e não médicos. | Criar política de privacidade e consentimento. |
| **Segurança** | CORS configurável e banco local de desenvolvimento. | Exigir HTTPS, logs seguros e backup controlado. |

## Próxima etapa: integração com IA real

A próxima etapa recomendada é substituir o motor pedagógico local por uma chamada controlada à OpenAI API, mantendo resposta obrigatoriamente estruturada e validada. Essa integração deve preservar as regras pedagógicas e incluir validação de schema para impedir respostas longas, respostas prontas indevidas ou linguagem inadequada.

| Etapa | Ação recomendada | Resultado esperado |
|---|---|---|
| 1 | Criar `AIProvider` no backend com interface única. | Permitir trocar IA real, mock ou regras locais. |
| 2 | Definir JSON Schema rígido para resposta pedagógica. | Interface previsível e segura no Flutter. |
| 3 | Adicionar camada de moderação pedagógica. | Bloquear linguagem dura, comparação e respostas completas. |
| 4 | Registrar observações de aprendizagem. | Melhorar adaptação semanal sem ranking. |
| 5 | Implementar voz opcional. | Usar speech-to-text e text-to-speech apenas com consentimento e privacidade. |

## Observação de validação

O backend foi validado com teste automatizado no ambiente de desenvolvimento. O ambiente atual não possui Flutter SDK instalado, portanto a análise estática e execução do app Flutter devem ser feitas em uma máquina local com Flutter configurado. Os arquivos foram organizados de modo convencional para facilitar `flutter create .`, `flutter pub get`, `flutter analyze` e `flutter run`.

## Referências

[1]: https://docs.flutter.dev/ "Flutter documentation"  
[2]: https://fastapi.tiangolo.com/ "FastAPI documentation"  
[3]: https://docs.sqlalchemy.org/ "SQLAlchemy documentation"  
[4]: https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd "Lei Geral de Proteção de Dados — Governo Federal"
