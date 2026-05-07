# Professor Bang — MVP pedagógico adaptativo

**Autor:** Manus AI  
**Stack:** Flutter, FastAPI, SQLite e arquitetura preparada para PostgreSQL e OpenAI API.

## Visão geral

O **Professor Bang** é um MVP de professor de reforço com IA pedagógica adaptativa. O projeto foi desenhado para apoiar uma adolescente com dificuldade cognitiva, ansiedade escolar, rigidez comportamental, dificuldade de abstração e baixa autonomia executiva. O aplicativo utiliza uma identidade original e genérica, sem imagem, voz, nome artístico real, marca registrada ou identidade visual oficial de artistas ou grupos.

> O objetivo central do MVP não é criar apenas um chatbot, mas um **sistema pedagógico adaptativo** que acolhe, divide tarefas em partes pequenas, oferece pistas antes de respostas e incentiva autonomia.

A versão inicial funciona com **chat pedagógico simulado local**, telas principais em Flutter, backend FastAPI básico, persistência SQLite e serviços separados para permitir futura integração com OpenAI API. Flutter é uma tecnologia multiplataforma usada para criar aplicativos a partir de uma única base de código, enquanto FastAPI é um framework Python moderno para criação de APIs baseado em tipagem e documentação automática.[1] [2]

## Arquitetura proposta

A arquitetura foi dividida em três camadas para facilitar manutenção, aprendizado por iniciantes e evolução futura. O frontend Flutter concentra experiência visual, navegação e interação pedagógica. O backend FastAPI concentra persistência, rotas REST e regras de domínio. A camada pedagógica fica isolada para permitir substituição gradual do simulador local por IA real estruturada em JSON.

| Camada | Responsabilidade | Implementação atual | Evolução planejada |
|---|---|---|---|
| **Frontend Flutter** | Telas, botões grandes, tema calmo, chat, rotina e painel dos pais. | Arquivos em `frontend_flutter/lib`, com telas e serviços locais. | Conectar totalmente à API, adicionar voz e acessibilidade avançada. |
| **Backend FastAPI** | API REST, modelos de dados, rotas, CORS e persistência. | Arquivos em `backend/app`, usando SQLAlchemy e SQLite. | Migrar para PostgreSQL via `DATABASE_URL` sem reescrever modelos. |
| **Serviço pedagógico** | Detectar travamento, gerar respostas curtas e estruturadas. | `backend/app/services/pedagogy.py` e `frontend_flutter/lib/services/local_pedagogy_service.dart`. | Substituir ou complementar por OpenAI API retornando JSON validado. |
| **Banco de dados** | Registrar perfil, sessões, mensagens, rotina, observações e conquistas. | SQLite local no backend e serviço local preparado no Flutter. | PostgreSQL, autenticação, criptografia e políticas de retenção. |

## Estrutura de pastas

```text
professor_bang/
├── README.md
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── db/session.py
│       ├── services/pedagogy.py
│       └── routers/
│           ├── achievements.py
│           ├── chat.py
│           ├── profile.py
│           ├── routine.py
│           └── sessions.py
└── frontend_flutter/
    ├── pubspec.yaml
    └── lib/
        ├── main.dart
        ├── app/
        ├── models/
        ├── services/
        ├── screens/
        └── widgets/
```

## Funcionalidades implementadas no MVP

O MVP contém as telas essenciais solicitadas e foi organizado para que cada parte seja compreensível para uma pessoa iniciante. As respostas pedagógicas são curtas, acolhedoras e orientadas por passos. O modo de apoio é ativado quando a aluna demonstra travamento por frases como “não sei”, “não consigo”, “travei” ou “ansiosa”.

| Funcionalidade | Status | Arquivos principais |
|---|---:|---|
| Tela inicial com avatar genérico, mensagem acolhedora e botões grandes | Implementada | `home_screen.dart`, `big_menu_button.dart`, `calm_scaffold.dart` |
| Perfil da aluna com campos pedagógicos e emocionais | Implementado | `profile_screen.dart`, `student_profile.dart`, `app_state.dart` |
| Modos de estudo | Implementados | `study_modes_screen.dart`, `chat_screen.dart` |
| Chat pedagógico simulado local | Implementado | `chat_screen.dart`, `local_pedagogy_service.dart` |
| Detecção de travamento e Modo Apoio | Implementados | `local_pedagogy_service.dart`, `pedagogy.py` |
| Checklist de rotina | Implementado | `routine_screen.dart`, `routine.py` |
| Painel dos pais básico | Implementado | `parent_dashboard_screen.dart`, `sessions.py` |
| Microvitórias sem ranking | Implementadas | `achievements_screen.dart`, `achievements.py` |
| Backend FastAPI com SQLite | Implementado | `main.py`, `models.py`, `db/session.py` |
| Preparação para PostgreSQL | Implementada | `DATABASE_URL` em `db/session.py` |
| Preparação para OpenAI API | Implementada conceitualmente | `api_service.dart`, `pedagogy.py` |

## Regras pedagógicas aplicadas

O sistema nunca chama a aluna de incapaz, não utiliza linguagem dura, não compara com outros alunos, não pressiona com tempo e não entrega a resposta completa de início. O fluxo padrão acolhe, divide em partes pequenas, explica com exemplo concreto, faz uma pergunta por vez, oferece pista antes de resposta e reforça esforço específico.

| Situação detectada | Resposta do sistema | Objetivo pedagógico |
|---|---|---|
| A aluna cola um enunciado | “Vamos descobrir o que a questão pede.” | Reduzir abstração e iniciar leitura orientada. |
| A aluna escreve “não sei” | Ativa Modo Apoio com três opções. | Regular ansiedade e devolver sensação de controle. |
| A aluna pede repetição | Reformula sem irritação. | Repetir com paciência e linguagem simples. |
| A aluna completa uma etapa | Sugere microvitória. | Reforçar esforço específico e autonomia. |

## Instalação do backend

Entre na pasta do backend e instale as dependências. O SQLite será criado automaticamente no primeiro carregamento da aplicação.

```bash
cd professor_bang/backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`. A documentação automática poderá ser acessada em `http://localhost:8000/docs`, recurso fornecido pelo ecossistema FastAPI/OpenAPI.[2]

## Testes rápidos do backend

Crie uma sessão, inicialize rotina e conquistas, e teste o chat pedagógico:

```bash
curl http://localhost:8000/

curl -X POST http://localhost:8000/api/routine/seed

curl -X POST http://localhost:8000/api/achievements/seed

curl -X POST http://localhost:8000/api/chat/pedagogical \
  -H "Content-Type: application/json" \
  -d '{"text":"não sei fazer essa questão", "mode":"Me ajuda com a tarefa", "subject":"matemática"}'
```

A resposta do chat vem em JSON estruturado para facilitar o controle da interface, incluindo `support_mode`, `answer`, `steps`, `question_for_student`, `hint_options` e `achievement_suggestion`.

## Instalação do frontend Flutter

Entre na pasta do frontend e execute o projeto em Android ou Web. É necessário ter o Flutter SDK instalado no computador local.[1]

```bash
cd professor_bang/frontend_flutter
flutter pub get
flutter run
```

Para rodar no navegador:

```bash
flutter run -d chrome
```

No MVP, o chat funciona localmente pelo serviço `LocalPedagogyService`. O arquivo `ApiService` já foi criado para facilitar a conexão futura com o backend FastAPI.

## Banco de dados

O backend cria as tabelas principais solicitadas por meio de SQLAlchemy. A URL padrão é SQLite, mas a arquitetura já aceita PostgreSQL por variável de ambiente. SQLAlchemy permite alternar bancos relacionais por configuração de engine e dialeto, mantendo os modelos de domínio no código Python.[3]

| Tabela | Finalidade |
|---|---|
| `student_profile` | Dados mínimos do perfil pedagógico da aluna. |
| `study_sessions` | Sessões de estudo e modos utilizados. |
| `messages` | Mensagens do estudante e do assistente pedagógico. |
| `learning_observations` | Observações pedagógicas e estratégias úteis. |
| `emotional_checkins` | Registros simples de estado emocional. |
| `routine_tasks` | Checklist de rotina de estudo. |
| `achievements` | Microvitórias sem ranking. |

Para usar PostgreSQL futuramente:

```bash
export DATABASE_URL="postgresql+psycopg://usuario:senha@localhost:5432/professor_bang"
```

Nesse caso, será necessário adicionar o driver PostgreSQL correspondente ao `requirements.txt`.

## Segurança, privacidade e LGPD

O MVP foi desenhado com princípio de minimização de dados: coleta apenas informações pedagógicas necessárias para personalização local. O aplicativo inclui aviso de que não substitui escola, psicopedagoga, psicóloga ou médico, e não fornece orientação médica. A LGPD brasileira estabelece princípios como finalidade, adequação, necessidade e segurança no tratamento de dados pessoais.[4]

| Princípio | Aplicação no MVP |
|---|---|
| **Necessidade** | Armazenar somente dados úteis para apoio pedagógico. |
| **Controle local** | Começar com SQLite e permitir apagar histórico. |
| **Não exposição** | Não publicar dados pessoais e evitar integrações externas no MVP. |
| **Transparência** | Exibir aviso sobre limites educacionais e não médicos. |
| **Segurança futura** | Planejar autenticação, criptografia e retenção de dados antes de produção. |

## Próxima etapa: integração com IA real

A próxima etapa recomendada é substituir o simulador pedagógico por uma chamada controlada à OpenAI API, mantendo a resposta obrigatoriamente em JSON estruturado. Essa integração deve preservar as regras pedagógicas e incluir validação de schema para impedir respostas longas, respostas prontas indevidas ou linguagem inadequada.

| Etapa | Ação recomendada | Resultado esperado |
|---|---|---|
| 1 | Criar `AIProvider` no backend com interface única. | Permitir trocar IA real, mock ou regras locais. |
| 2 | Definir JSON Schema rígido para resposta pedagógica. | Interface previsível e segura no Flutter. |
| 3 | Adicionar camada de moderação pedagógica. | Bloquear linguagem dura, comparação e respostas completas. |
| 4 | Registrar observações de aprendizagem. | Melhorar adaptação semanal sem ranking. |
| 5 | Implementar voz opcional. | Usar speech-to-text e text-to-speech apenas com consentimento e privacidade. |

Um exemplo de contrato JSON para a IA real seria:

```json
{
  "support_mode": true,
  "emotional_tone": "acolhedor e calmo",
  "answer": "Tudo bem travar. Vamos fazer só o primeiro passo.",
  "steps": [
    {"kind": "acolhimento", "text": "Você não precisa resolver tudo agora."},
    {"kind": "pista", "text": "Procure o verbo da questão."}
  ],
  "question_for_student": "Qual palavra mostra o que a questão pede?",
  "hint_options": ["Quero uma pista", "Quero um exemplo", "Quero fazer junto"],
  "achievement_suggestion": "Pediu pista"
}
```

## Observação sobre validação local

O backend foi carregado com sucesso no ambiente de desenvolvimento. O ambiente atual não possui Flutter SDK instalado, portanto a análise estática e execução do app Flutter devem ser feitas em uma máquina local com Flutter configurado. Os arquivos foram organizados de modo convencional para facilitar `flutter pub get`, `flutter analyze` e `flutter run`.

## Referências

[1]: https://docs.flutter.dev/ "Flutter documentation"  
[2]: https://fastapi.tiangolo.com/ "FastAPI documentation"  
[3]: https://docs.sqlalchemy.org/ "SQLAlchemy documentation"  
[4]: https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd "Lei Geral de Proteção de Dados — Governo Federal"
