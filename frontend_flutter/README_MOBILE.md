# Professor Bang — Guia para rodar no celular

Este guia deixa claro como transformar o código Flutter em um app executável no celular e como conectar o aplicativo ao backend FastAPI corrigido. O projeto já contém a pasta `lib/` com as telas, modelos, serviços e integração de API; em uma máquina com Flutter instalado, as pastas nativas `android/`, `ios/`, `web/`, `macos/`, `windows` e `linux` podem ser geradas com `flutter create .` dentro de `frontend_flutter`.

> **Resumo operacional:** primeiro rode o backend na rede local; depois gere as plataformas Flutter; por fim, execute o app passando o endereço correto da API com `--dart-define=API_BASE_URL=...`.

## 1. Subir o backend

Na pasta raiz do repositório, entre no backend e inicie a API em modo de desenvolvimento. Use `0.0.0.0` para permitir que um celular na mesma rede Wi-Fi consiga acessar o servidor do computador.

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Depois, teste no navegador do computador:

```text
http://localhost:8000/docs
http://localhost:8000/health
```

Se estiver usando celular físico, descubra o IP local do computador. No macOS ou Linux, geralmente basta executar:

```bash
ipconfig getifaddr en0  # macOS em Wi-Fi
hostname -I            # Linux
```

No Windows, use:

```powershell
ipconfig
```

Procure o endereço IPv4 da rede Wi-Fi, por exemplo `192.168.0.25`. O celular e o computador precisam estar na **mesma rede Wi-Fi**.

## 2. Gerar as plataformas Flutter

A pasta `frontend_flutter` foi preparada como módulo Flutter, mas o ZIP original não trazia as pastas nativas. Em uma máquina com Flutter SDK configurado, rode:

```bash
cd frontend_flutter
flutter create .
flutter pub get
```

Esse comando preserva a pasta `lib/` existente e gera os arquivos necessários para Android, iOS, Web e desktop. Em seguida, confira os dispositivos disponíveis:

```bash
flutter doctor
flutter devices
```

## 3. Rodar no emulador Android

Para emulador Android, o endereço especial `10.0.2.2` aponta do emulador para o `localhost` do computador. O app já usa esse endereço como padrão, então normalmente basta executar:

```bash
cd frontend_flutter
flutter run -d android
```

Se quiser ser explícito, rode:

```bash
flutter run -d android --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

## 4. Rodar em celular Android físico

Para celular físico, substitua `SEU_IP_LOCAL` pelo IPv4 do computador que está rodando o backend.

```bash
cd frontend_flutter
flutter run -d <id_do_dispositivo> --dart-define=API_BASE_URL=http://SEU_IP_LOCAL:8000
```

Exemplo:

```bash
flutter run -d R58N123ABC --dart-define=API_BASE_URL=http://192.168.0.25:8000
```

Se o Android bloquear requisições HTTP durante o desenvolvimento, ajuste o arquivo `android/app/src/main/AndroidManifest.xml` após rodar `flutter create .`. Dentro da tag `<application>`, adicione temporariamente:

```xml
android:usesCleartextTraffic="true"
```

Em produção, o ideal é publicar o backend com **HTTPS** e remover essa permissão ampla.

## 5. Rodar no simulador iOS ou iPhone

No simulador iOS, muitas vezes `localhost` funciona porque o simulador compartilha a rede com o macOS. Execute:

```bash
cd frontend_flutter
flutter run -d ios --dart-define=API_BASE_URL=http://localhost:8000
```

Em iPhone físico, use o IP local do computador, assim como no Android físico:

```bash
flutter run -d <id_do_dispositivo> --dart-define=API_BASE_URL=http://SEU_IP_LOCAL:8000
```

Para iOS físico, você também precisará configurar assinatura no Xcode. Caso o iOS bloqueie HTTP em desenvolvimento, será necessário configurar exceções temporárias de App Transport Security no `ios/Runner/Info.plist` ou usar HTTPS.

## 6. Fluxo de teste recomendado

A tabela abaixo mostra uma sequência simples para confirmar que o app está funcionando no celular com o backend real.

| Etapa | Ação | Resultado esperado |
|---|---|---|
| 1 | Abrir `http://SEU_IP_LOCAL:8000/health` no navegador do celular | Resposta `{"status":"ok"}` |
| 2 | Abrir o app e entrar em **Perfil da aluna** | Tela com dados editáveis da Duda |
| 3 | Tocar em **Salvar no backend** | Mensagem informando o ID remoto da aluna |
| 4 | Abrir **Modos de estudo** e escolher **Estou travada** | Tela de chat aberta |
| 5 | Enviar “não entendi essa conta” | Resposta acolhedora do backend com modo apoio |
| 6 | Conferir `http://SEU_IP_LOCAL:8000/docs` no computador | Sessões, mensagens e perfil disponíveis na API |

## 7. O que já está pronto

O app Flutter agora usa `ApiService` com `API_BASE_URL`, salva o perfil no backend, cria uma sessão de estudo automaticamente ao iniciar o chat e envia mensagens reais para `/chat/message`. O backend integrado possui banco SQLite local, modelos SQLAlchemy, schemas Pydantic, rotas de estudantes, sessões, chat, rotina, conquistas e painel dos responsáveis.

## 8. Limites antes de publicar em produção

Este estado está pronto para **teste local no celular**, mas ainda não é uma versão de loja. Antes de publicar, implemente autenticação dos responsáveis, HTTPS obrigatório, política de privacidade, controle de acesso por usuário, logs sem dados sensíveis, backup de banco, revisão pedagógica e testes em aparelhos reais. Como o aplicativo lida com dados educacionais e emocionais de adolescente, a versão pública deve tratar privacidade e consentimento como requisitos centrais, não como etapa opcional.
