import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app/app_state.dart';
import '../models/chat_message.dart';
import '../widgets/calm_scaffold.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key, required this.initialMode});

  final String initialMode;

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  late String _mode;
  final List<ChatMessage> _messages = [];
  bool _isSending = false;
  int? _sessionId;

  @override
  void initState() {
    super.initState();
    _mode = widget.initialMode;
    _messages.add(ChatMessage(
      role: ChatRole.mentor,
      text: 'Vamos usar o modo "$_mode". Escreva a tarefa ou a parte que ficou difícil.',
    ));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _isSending) return;

    setState(() {
      _isSending = true;
      _messages.add(ChatMessage(role: ChatRole.student, text: text));
      _controller.clear();
    });

    try {
      final appState = context.read<AppState>();
      _sessionId ??= await appState.startStudySession(
        subject: appState.profile.difficultSubjects.split(',').first.trim().isEmpty
            ? 'geral'
            : appState.profile.difficultSubjects.split(',').first.trim(),
        studyMode: _mode,
      );

      final response = await appState.api.sendPedagogicalMessage(
        sessionId: _sessionId!,
        text: text,
        mode: _mode,
        subject: appState.profile.difficultSubjects.split(',').first.trim().isEmpty
            ? 'geral'
            : appState.profile.difficultSubjects.split(',').first.trim(),
      );

      if (!mounted) return;
      setState(() {
        _messages.add(ChatMessage(
          role: ChatRole.mentor,
          text: response.toReadableText(),
          supportMode: response.supportMode,
        ));
        if (response.achievementSuggestion != null) {
          _messages.add(ChatMessage(
            role: ChatRole.mentor,
            text: 'Microvitória percebida: ${response.achievementSuggestion}.',
          ));
        }
      });
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _messages.add(ChatMessage(
          role: ChatRole.mentor,
          supportMode: true,
          text: 'Não consegui conectar com o servidor agora. Confira se o backend está rodando e se o endereço da API está correto.\n\nDetalhe técnico: $error',
        ));
      });
    } finally {
      if (mounted) {
        setState(() => _isSending = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: _mode,
      actions: [
        PopupMenuButton<String>(
          onSelected: (value) => setState(() {
            _mode = value;
            _sessionId = null;
          }),
          itemBuilder: (_) => const [
            PopupMenuItem(value: 'Me explica devagar', child: Text('Me explica devagar')),
            PopupMenuItem(value: 'Me ajuda com a tarefa', child: Text('Me ajuda com a tarefa')),
            PopupMenuItem(value: 'Estou travada', child: Text('Estou travada')),
            PopupMenuItem(value: 'Pausa para respirar', child: Text('Pausa para respirar')),
          ],
        ),
      ],
      child: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isStudent = message.role == ChatRole.student;
                return Align(
                  alignment: isStudent ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    constraints: const BoxConstraints(maxWidth: 330),
                    margin: const EdgeInsets.symmetric(vertical: 6),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: isStudent
                          ? Theme.of(context).colorScheme.secondary
                          : message.supportMode
                              ? const Color(0xFFFFF6D8)
                              : Colors.white,
                      borderRadius: BorderRadius.circular(18),
                    ),
                    child: Text(
                      message.text,
                      style: TextStyle(
                        color: isStudent ? Colors.white : Colors.black87,
                        height: 1.35,
                        fontSize: 15,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isSending)
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: LinearProgressIndicator(),
            ),
          Container(
            color: Colors.white,
            padding: const EdgeInsets.fromLTRB(12, 10, 12, 12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    minLines: 1,
                    maxLines: 4,
                    decoration: const InputDecoration(
                      hintText: 'Cole o enunciado ou diga onde travou...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _send(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  onPressed: _isSending ? null : _send,
                  icon: const Icon(Icons.send),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
