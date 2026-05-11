import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';
import { useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  RefreshControl,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

const API_BASE_URL = (process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');

const defaultProfile = {
  id: null,
  name: 'Duda',
  age: '14',
  difficultSubjects: 'Matematica, interpretacao de texto',
  interests: 'musica, danca, idiomas',
  readingLevel: 'medio',
  mathLevel: 'basico',
  anxietyTriggers: 'pressa, texto longo, muitas etapas juntas',
  helpfulStrategies: 'pistas, exemplos simples, pausa para respirar',
};

const modes = [
  'Me explica devagar',
  'Me ajuda com a tarefa',
  'Me da um exemplo',
  'Pode repetir?',
  'Estou travada',
  'Treinar para prova',
  'Pausa para respirar',
];

function splitList(value) {
  return value
    .split(/[,;\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function firstSubject(profile) {
  return splitList(profile.difficultSubjects)[0] || 'geral';
}

function modeToBackend(mode) {
  const normalized = mode.toLowerCase();
  if (normalized.includes('travada')) return 'stuck';
  if (normalized.includes('respirar') || normalized.includes('pausa')) return 'breathing';
  if (normalized.includes('prova')) return 'practice_test';
  if (normalized.includes('exemplo')) return 'give_example';
  if (normalized.includes('tarefa')) return 'help_homework';
  if (normalized.includes('repetir')) return 'repeat';
  return 'explain_slow';
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });

  const text = await response.text();
  const data = text ? JSON.parse(text) : {};

  if (!response.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : text;
    throw new Error(detail || `Erro ${response.status}`);
  }

  return data;
}

function backendResponseToMessage(data) {
  const lines = [data.message].filter(Boolean);
  if (data.hint) lines.push(`Pista: ${data.hint}`);
  if (data.next_step) lines.push(`Proximo passo: ${data.next_step}`);
  if (Array.isArray(data.options) && data.options.length > 0) {
    lines.push(`Escolha uma opcao: ${data.options.join(' | ')}`);
  }
  return lines.join('\n\n');
}

export default function App() {
  const [screen, setScreen] = useState('chat');
  const [profile, setProfile] = useState(defaultProfile);
  const [remoteStudentId, setRemoteStudentId] = useState(null);

  const api = useMemo(() => ({
    async ensureProfile(currentProfile) {
      if (remoteStudentId) return remoteStudentId;
      const created = await apiRequest('/students/', {
        method: 'POST',
        body: JSON.stringify({
          name: currentProfile.name.trim(),
          age: Number(currentProfile.age) || 14,
          difficult_subjects: splitList(currentProfile.difficultSubjects),
          interests: splitList(currentProfile.interests),
          reading_level: currentProfile.readingLevel.trim() || 'medio',
          math_level: currentProfile.mathLevel.trim() || 'basico',
          anxiety_triggers: splitList(currentProfile.anxietyTriggers),
          helpful_strategies: splitList(currentProfile.helpfulStrategies),
        }),
      });
      setRemoteStudentId(created.id);
      setProfile((previous) => ({ ...previous, id: created.id }));
      return created.id;
    },
  }), [remoteStudentId]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.shell}>
        <Header />
        <View style={styles.content}>
          {screen === 'perfil' && (
            <ProfileScreen
              profile={profile}
              setProfile={setProfile}
              remoteStudentId={remoteStudentId}
              setRemoteStudentId={setRemoteStudentId}
            />
          )}
          {screen === 'chat' && <ChatScreen profile={profile} api={api} />}
          {screen === 'rotina' && <RoutineScreen profile={profile} api={api} />}
          {screen === 'pais' && <ParentsScreen profile={profile} api={api} />}
        </View>
        <Nav current={screen} onChange={setScreen} />
      </View>
    </SafeAreaView>
  );
}

function Header() {
  return (
    <View style={styles.header}>
      <View>
        <Text style={styles.appName}>Professor Bang</Text>
        <Text style={styles.apiText}>API: {API_BASE_URL}</Text>
      </View>
      <View style={styles.logoMark}>
        <Ionicons name="sparkles" size={22} color="#213547" />
      </View>
    </View>
  );
}

function Nav({ current, onChange }) {
  const items = [
    ['chat', 'chatbubble-ellipses-outline', 'Chat'],
    ['rotina', 'checkbox-outline', 'Rotina'],
    ['pais', 'people-outline', 'Pais'],
    ['perfil', 'person-outline', 'Perfil'],
  ];

  return (
    <View style={styles.nav}>
      {items.map(([key, icon, label]) => {
        const active = current === key;
        return (
          <Pressable key={key} onPress={() => onChange(key)} style={[styles.navItem, active && styles.navItemActive]}>
            <Ionicons name={icon} size={22} color={active ? '#ffffff' : '#506070'} />
            <Text style={[styles.navLabel, active && styles.navLabelActive]}>{label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

function ProfileScreen({ profile, setProfile, remoteStudentId, setRemoteStudentId }) {
  const [saving, setSaving] = useState(false);

  function update(field, value) {
    setProfile((previous) => ({ ...previous, [field]: value }));
  }

  async function saveProfile() {
    setSaving(true);
    try {
      const created = await apiRequest('/students/', {
        method: 'POST',
        body: JSON.stringify({
          name: profile.name.trim(),
          age: Number(profile.age) || 14,
          difficult_subjects: splitList(profile.difficultSubjects),
          interests: splitList(profile.interests),
          reading_level: profile.readingLevel.trim() || 'medio',
          math_level: profile.mathLevel.trim() || 'basico',
          anxiety_triggers: splitList(profile.anxietyTriggers),
          helpful_strategies: splitList(profile.helpfulStrategies),
        }),
      });
      setRemoteStudentId(created.id);
      setProfile((previous) => ({ ...previous, id: created.id }));
      Alert.alert('Perfil salvo', `ID da aluna: ${created.id}`);
    } catch (error) {
      Alert.alert('Nao foi possivel salvar', error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.screenPad} keyboardShouldPersistTaps="handled">
      {remoteStudentId ? <Notice icon="cloud-done-outline" text={`Perfil conectado ao backend: ID ${remoteStudentId}`} /> : null}
      <Field label="Nome" value={profile.name} onChangeText={(value) => update('name', value)} />
      <Field label="Idade" value={profile.age} onChangeText={(value) => update('age', value)} keyboardType="number-pad" />
      <Field label="Materias com dificuldade" value={profile.difficultSubjects} onChangeText={(value) => update('difficultSubjects', value)} multiline />
      <Field label="Interesses" value={profile.interests} onChangeText={(value) => update('interests', value)} multiline />
      <Field label="Nivel de leitura" value={profile.readingLevel} onChangeText={(value) => update('readingLevel', value)} />
      <Field label="Nivel de matematica" value={profile.mathLevel} onChangeText={(value) => update('mathLevel', value)} />
      <Field label="Gatilhos de ansiedade" value={profile.anxietyTriggers} onChangeText={(value) => update('anxietyTriggers', value)} multiline />
      <Field label="Estrategias que ajudam" value={profile.helpfulStrategies} onChangeText={(value) => update('helpfulStrategies', value)} multiline />
      <PrimaryButton icon="save-outline" label={saving ? 'Salvando...' : 'Salvar no backend'} disabled={saving} onPress={saveProfile} />
    </ScrollView>
  );
}

function ChatScreen({ profile, api }) {
  const [mode, setMode] = useState(modes[0]);
  const [sessionId, setSessionId] = useState(null);
  const [welcomeLoaded, setWelcomeLoaded] = useState(false);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'mentor', text: 'Escolha um modo e envie a tarefa ou a parte que ficou dificil.' },
  ]);

  async function ensureSession() {
    if (sessionId) return sessionId;
    const studentId = await api.ensureProfile(profile);
    const session = await apiRequest('/sessions/start', {
      method: 'POST',
      body: JSON.stringify({
        student_id: studentId,
        subject: firstSubject(profile),
        study_mode: modeToBackend(mode),
      }),
    });
    setSessionId(session.id);
    return session.id;
  }

  async function loadWelcome(nextSessionId) {
    if (welcomeLoaded) return;
    const welcome = await apiRequest(`/chat/welcome?session_id=${nextSessionId}`, { method: 'POST' });
    setWelcomeLoaded(true);
    setMessages((previous) => [...previous, { role: 'mentor', text: backendResponseToMessage(welcome), support: welcome.is_stuck_detected }]);
  }

  async function send() {
    const text = input.trim();
    if (!text || sending) return;

    setInput('');
    setSending(true);
    setMessages((previous) => [...previous, { role: 'student', text }]);

    try {
      const nextSessionId = await ensureSession();
      await loadWelcome(nextSessionId);
      const response = await apiRequest('/chat/message', {
        method: 'POST',
        body: JSON.stringify({
          session_id: nextSessionId,
          message: text,
          subject: firstSubject(profile),
          study_mode: modeToBackend(mode),
        }),
      });

      const additions = [
        { role: 'mentor', text: backendResponseToMessage(response), support: response.is_stuck_detected },
      ];
      if (response.response_type === 'stuck_support') {
        additions.push({ role: 'mentor', text: 'Microvitoria percebida: pediu ajuda antes de desistir.' });
      }
      setMessages((previous) => [...previous, ...additions]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        { role: 'mentor', support: true, text: `Nao consegui falar com o backend agora.\n\n${error.message}` },
      ]);
    } finally {
      setSending(false);
    }
  }

  function changeMode(nextMode) {
    setMode(nextMode);
    setSessionId(null);
    setWelcomeLoaded(false);
    setMessages((previous) => [...previous, { role: 'mentor', text: `Modo alterado para: ${nextMode}` }]);
  }

  return (
    <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.modeRow}>
        {modes.map((item) => (
          <Pressable key={item} onPress={() => changeMode(item)} style={[styles.modeChip, item === mode && styles.modeChipActive]}>
            <Text style={[styles.modeText, item === mode && styles.modeTextActive]}>{item}</Text>
          </Pressable>
        ))}
      </ScrollView>
      <ScrollView contentContainerStyle={styles.chatList}>
        {messages.map((message, index) => (
          <View key={`${message.role}-${index}`} style={[styles.bubble, message.role === 'student' ? styles.studentBubble : styles.mentorBubble, message.support && styles.supportBubble]}>
            <Text style={[styles.bubbleText, message.role === 'student' && styles.studentBubbleText]}>{message.text}</Text>
          </View>
        ))}
        {sending ? <ActivityIndicator style={styles.loader} color="#213547" /> : null}
      </ScrollView>
      <View style={styles.inputRow}>
        <TextInput
          value={input}
          onChangeText={setInput}
          placeholder="Cole o enunciado ou diga onde travou..."
          style={styles.chatInput}
          multiline
        />
        <Pressable onPress={send} disabled={sending} style={[styles.sendButton, sending && styles.disabledButton]}>
          <Ionicons name="send" size={20} color="#ffffff" />
        </Pressable>
      </View>
    </KeyboardAvoidingView>
  );
}

function RoutineScreen({ profile, api }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadTasks() {
    setLoading(true);
    setError('');
    try {
      const studentId = await api.ensureProfile(profile);
      const data = await apiRequest(`/routine/${studentId}/today`);
      setTasks(data);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }

  async function toggleTask(task) {
    try {
      const updated = await apiRequest(`/routine/task/${task.id}/toggle`, {
        method: 'PUT',
        body: JSON.stringify({ is_completed: !task.is_completed }),
      });
      setTasks((previous) => previous.map((item) => (item.id === updated.id ? updated : item)));
    } catch (toggleError) {
      Alert.alert('Nao foi possivel atualizar', toggleError.message);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  const done = tasks.filter((task) => task.is_completed).length;

  return (
    <ScrollView contentContainerStyle={styles.screenPad} refreshControl={<RefreshControl refreshing={loading} onRefresh={loadTasks} />}>
      <Notice icon="checkmark-circle-outline" text={`Concluido: ${done} de ${tasks.length}`} />
      {error ? <ErrorBox message={error} /> : null}
      {tasks.map((task) => (
        <Pressable key={task.id} onPress={() => toggleTask(task)} style={styles.taskRow}>
          <Ionicons name={task.is_completed ? 'checkbox' : 'square-outline'} size={24} color="#213547" />
          <Text style={[styles.taskText, task.is_completed && styles.taskDone]}>{task.title}</Text>
        </Pressable>
      ))}
    </ScrollView>
  );
}

function ParentsScreen({ profile, api }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadReport() {
    setLoading(true);
    setError('');
    try {
      const studentId = await api.ensureProfile(profile);
      const data = await apiRequest(`/parents/${studentId}/report`);
      setReport(data);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReport();
  }, []);

  const achievements = (report?.recent_achievements || []).map((item) => item.title).join(', ');
  const subjects = (report?.subjects_studied || []).join(', ');

  return (
    <ScrollView contentContainerStyle={styles.screenPad} refreshControl={<RefreshControl refreshing={loading} onRefresh={loadReport} />}>
      {error ? <ErrorBox message={error} /> : null}
      <Info title="Aluna" text={report?.student_name || profile.name} />
      <Info title="Sessoes na semana" text={`${report?.week_sessions ?? 0}`} />
      <Info title="Tempo de estudo" text={`${report?.total_study_minutes ?? 0} minutos`} />
      <Info title="Materias estudadas" text={subjects || 'Ainda sem sessoes registradas.'} />
      <Info title="Momentos de travamento" text={`${report?.stuck_moments ?? 0}`} />
      <Info title="Microvitorias recentes" text={achievements || 'Ainda sem microvitorias registradas nesta semana.'} />
      <Info title="Observacao pedagogica" text={report?.pedagogical_note || 'Sem observacao no momento.'} />
      <Text style={styles.privacyText}>Privacidade: mantenha o minimo de dados necessario e apague historicos quando desejar.</Text>
    </ScrollView>
  );
}

function Field({ label, value, onChangeText, multiline, keyboardType }) {
  return (
    <View style={styles.fieldBlock}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        value={value}
        onChangeText={onChangeText}
        keyboardType={keyboardType}
        multiline={multiline}
        style={[styles.input, multiline && styles.multilineInput]}
      />
    </View>
  );
}

function PrimaryButton({ icon, label, onPress, disabled }) {
  return (
    <Pressable onPress={onPress} disabled={disabled} style={[styles.primaryButton, disabled && styles.disabledButton]}>
      <Ionicons name={icon} size={20} color="#ffffff" />
      <Text style={styles.primaryButtonText}>{label}</Text>
    </Pressable>
  );
}

function Notice({ icon, text }) {
  return (
    <View style={styles.notice}>
      <Ionicons name={icon} size={22} color="#213547" />
      <Text style={styles.noticeText}>{text}</Text>
    </View>
  );
}

function ErrorBox({ message }) {
  return (
    <View style={styles.errorBox}>
      <Ionicons name="warning-outline" size={22} color="#7a2d19" />
      <Text style={styles.errorText}>Nao consegui conectar com o backend. {message}</Text>
    </View>
  );
}

function Info({ title, text }) {
  return (
    <View style={styles.infoBlock}>
      <Text style={styles.infoTitle}>{title}</Text>
      <Text style={styles.infoText}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#F7F3EA',
  },
  shell: {
    flex: 1,
    backgroundColor: '#F7F3EA',
  },
  header: {
    minHeight: 86,
    paddingHorizontal: 18,
    paddingTop: 14,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E5DDCF',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  appName: {
    fontSize: 24,
    fontWeight: '800',
    color: '#213547',
  },
  apiText: {
    marginTop: 4,
    fontSize: 12,
    color: '#617080',
  },
  logoMark: {
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: '#F3DFA2',
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    flex: 1,
  },
  flex: {
    flex: 1,
  },
  screenPad: {
    padding: 16,
    paddingBottom: 28,
    gap: 12,
  },
  nav: {
    flexDirection: 'row',
    gap: 8,
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: '#E5DDCF',
    backgroundColor: '#FFFDF8',
  },
  navItem: {
    flex: 1,
    minHeight: 56,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 2,
  },
  navItemActive: {
    backgroundColor: '#213547',
  },
  navLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#506070',
  },
  navLabelActive: {
    color: '#ffffff',
  },
  fieldBlock: {
    gap: 6,
  },
  label: {
    fontSize: 14,
    fontWeight: '800',
    color: '#213547',
  },
  input: {
    minHeight: 48,
    borderWidth: 1,
    borderColor: '#D5CCBE',
    borderRadius: 8,
    backgroundColor: '#ffffff',
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    color: '#20272E',
  },
  multilineInput: {
    minHeight: 84,
    textAlignVertical: 'top',
  },
  primaryButton: {
    minHeight: 50,
    borderRadius: 8,
    backgroundColor: '#213547',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  primaryButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '800',
  },
  disabledButton: {
    opacity: 0.6,
  },
  notice: {
    borderRadius: 8,
    backgroundColor: '#EFE8D9',
    padding: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  noticeText: {
    flex: 1,
    fontSize: 15,
    color: '#213547',
    fontWeight: '700',
  },
  modeRow: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    gap: 8,
  },
  modeChip: {
    minHeight: 38,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#D5CCBE',
    backgroundColor: '#FFFDF8',
    justifyContent: 'center',
    paddingHorizontal: 12,
  },
  modeChipActive: {
    backgroundColor: '#213547',
    borderColor: '#213547',
  },
  modeText: {
    color: '#213547',
    fontWeight: '700',
  },
  modeTextActive: {
    color: '#ffffff',
  },
  chatList: {
    padding: 16,
    gap: 10,
  },
  bubble: {
    maxWidth: '88%',
    padding: 14,
    borderRadius: 8,
  },
  mentorBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#E4DCCC',
  },
  supportBubble: {
    backgroundColor: '#FFF3C8',
  },
  studentBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#466B7A',
  },
  bubbleText: {
    fontSize: 15,
    lineHeight: 21,
    color: '#20272E',
  },
  studentBubbleText: {
    color: '#ffffff',
  },
  loader: {
    marginTop: 8,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: '#E5DDCF',
    backgroundColor: '#FFFDF8',
  },
  chatInput: {
    flex: 1,
    maxHeight: 110,
    minHeight: 46,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#D5CCBE',
    backgroundColor: '#ffffff',
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 15,
  },
  sendButton: {
    width: 48,
    height: 48,
    borderRadius: 8,
    backgroundColor: '#213547',
    alignItems: 'center',
    justifyContent: 'center',
  },
  taskRow: {
    minHeight: 58,
    borderRadius: 8,
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#E4DCCC',
    paddingHorizontal: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  taskText: {
    flex: 1,
    fontSize: 16,
    color: '#20272E',
    fontWeight: '700',
  },
  taskDone: {
    textDecorationLine: 'line-through',
    color: '#6F7B83',
  },
  infoBlock: {
    borderRadius: 8,
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#E4DCCC',
    padding: 16,
    gap: 6,
  },
  infoTitle: {
    fontSize: 15,
    color: '#213547',
    fontWeight: '800',
  },
  infoText: {
    fontSize: 15,
    color: '#20272E',
    lineHeight: 21,
  },
  privacyText: {
    textAlign: 'center',
    color: '#617080',
    fontSize: 13,
    lineHeight: 18,
  },
  errorBox: {
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#E9B8A4',
    backgroundColor: '#FFF0E8',
    padding: 14,
    flexDirection: 'row',
    gap: 10,
  },
  errorText: {
    flex: 1,
    fontSize: 14,
    lineHeight: 20,
    color: '#7a2d19',
  },
});
