from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

checks = []

root = client.get('/')
checks.append(('GET /', root.status_code, root.json().get('status') == 'online'))

profile_payload = {
    'name': 'Duda',
    'age': 14,
    'difficult_subjects': 'Matemática e interpretação de texto',
    'interests': 'K-pop, dança, música e idiomas',
    'reading_level': 'frases curtas',
    'math_level': 'passo a passo',
    'anxiety_triggers': 'pressa e textos longos',
    'helpful_strategies': 'pistas, exemplos e pausa para respirar',
}
profile = client.post('/api/profile', json=profile_payload)
checks.append(('POST /api/profile', profile.status_code, profile.status_code == 200 and profile.json()['name'] == 'Duda'))

routine = client.post('/api/routine/seed')
checks.append(('POST /api/routine/seed', routine.status_code, routine.status_code == 200 and len(routine.json()) >= 7))

achievements = client.post('/api/achievements/seed')
checks.append(('POST /api/achievements/seed', achievements.status_code, achievements.status_code == 200 and len(achievements.json()) >= 5))

chat = client.post('/api/chat/pedagogical', json={
    'text': 'não sei fazer essa questão',
    'mode': 'Me ajuda com a tarefa',
    'subject': 'matemática',
})
chat_json = chat.json()
checks.append(('POST /api/chat/pedagogical', chat.status_code, chat.status_code == 200 and chat_json['support_mode'] is True))

session = client.post('/api/sessions', json={
    'student_id': profile.json().get('id'),
    'subject': 'matemática',
    'mode': 'me_explica_devagar',
    'duration_minutes': 10,
})
checks.append(('POST /api/sessions', session.status_code, session.status_code == 200 and session.json()['duration_minutes'] == 10))

dashboard = client.get('/api/sessions/parent-dashboard')
checks.append(('GET /api/sessions/parent-dashboard', dashboard.status_code, dashboard.status_code == 200 and 'total_study_minutes' in dashboard.json()))

for name, status, passed in checks:
    print(f'{name}: status={status} passed={passed}')

if not all(passed for _, _, passed in checks):
    raise SystemExit(1)

print('Validação concluída com sucesso.')
