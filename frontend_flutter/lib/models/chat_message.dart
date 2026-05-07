enum ChatRole { student, mentor }

class ChatMessage {
  final ChatRole role;
  final String text;
  final bool supportMode;

  const ChatMessage({
    required this.role,
    required this.text,
    this.supportMode = false,
  });
}
