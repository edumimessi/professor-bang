# Professor Bang - Frontend Expo

Este e o app mobile em Expo/React Native conectado ao backend FastAPI do Professor Bang.

## O que ja funciona

- Perfil da aluna com criacao no backend.
- Chat pedagogico com sessao, boas-vindas e envio para `/chat/message`.
- Rotina do dia usando `/routine/{student_id}/today` e toggle de tarefas.
- Painel dos pais usando `/parents/{student_id}/report`.

## Requisitos

- Node.js instalado.
- Expo Go no celular ou emulador Android/iOS.
- Backend FastAPI rodando.

## Instalar

```bash
cd frontend_expo
npm install
```

## Configurar a API

Copie o exemplo de ambiente:

```bash
cp .env.example .env
```

Ajuste `EXPO_PUBLIC_API_BASE_URL`:

```bash
EXPO_PUBLIC_API_BASE_URL=http://10.0.2.2:8000
```

Use:

- Android emulator: `http://10.0.2.2:8000`
- iOS simulator: `http://localhost:8000`
- Celular fisico na mesma rede Wi-Fi: `http://IP_DO_COMPUTADOR:8000`
- Uso real fora da rede local: URL publicada, por exemplo `https://sua-api.onrender.com`

## Rodar

```bash
npm run start
```

Depois abra no Expo Go pelo QR Code.

## Backend local

Em outro terminal:

```bash
cd ../backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

No Windows PowerShell, se a ativacao do ambiente virtual variar, use o comando equivalente exibido pelo seu terminal.

## Proxima etapa para ficar realmente utilizavel

Publique o backend em Render, Railway, Fly.io ou outro provedor. O app no celular precisa acessar uma URL publica quando estiver fora da sua rede Wi-Fi.
