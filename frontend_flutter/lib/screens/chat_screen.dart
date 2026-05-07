import 'package:flutter/material.dart';

import '../models/chat_message.dart';
import '../services/local_pedagogy_service.dart';
import '../widgets/calm_scaffold.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key, required this.initialMode});

  final String initialMode;

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  final _service = LocalPedagogyService();
  late String _mode;
  final List<ChatMessage> _messages = [];

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

  void _send() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    final response = _service.respond(text: text, mode: _mode);
    setState(() {
      _messages.add(ChatMessage(role: ChatRole.student, text: text));
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
      _controller.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: _mode,
      actions: [
        PopupMenuButton<String>(
          onSelected: (value) => setState(() => _mode = value),
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
                  onPressed: _send,
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
