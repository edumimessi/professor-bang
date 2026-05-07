import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app/app_state.dart';
import '../models/student_profile.dart';
import '../widgets/calm_scaffold.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController name;
  late final TextEditingController age;
  late final TextEditingController subjects;
  late final TextEditingController interests;
  late final TextEditingController reading;
  late final TextEditingController math;
  late final TextEditingController triggers;
  late final TextEditingController strategies;
  bool _isSaving = false;

  @override
  void initState() {
    super.initState();
    final profile = context.read<AppState>().profile;
    name = TextEditingController(text: profile.name);
    age = TextEditingController(text: profile.age.toString());
    subjects = TextEditingController(text: profile.difficultSubjects);
    interests = TextEditingController(text: profile.interests);
    reading = TextEditingController(text: profile.readingLevel);
    math = TextEditingController(text: profile.mathLevel);
    triggers = TextEditingController(text: profile.anxietyTriggers);
    strategies = TextEditingController(text: profile.helpfulStrategies);
  }

  @override
  void dispose() {
    for (final controller in [name, age, subjects, interests, reading, math, triggers, strategies]) {
      controller.dispose();
    }
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate() || _isSaving) return;

    final appState = context.read<AppState>();
    appState.updateProfile(StudentProfile(
      id: appState.remoteStudentId,
      name: name.text.trim(),
      age: int.tryParse(age.text) ?? 14,
      difficultSubjects: subjects.text.trim(),
      interests: interests.text.trim(),
      readingLevel: reading.text.trim(),
      mathLevel: math.text.trim(),
      anxietyTriggers: triggers.text.trim(),
      helpfulStrategies: strategies.text.trim(),
    ));

    setState(() => _isSaving = true);
    try {
      final saved = await appState.saveProfileToApi();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Perfil salvo no backend. ID da aluna: ${saved.id}.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Perfil salvo no app, mas a API não respondeu: $error')),
      );
    } finally {
      if (mounted) setState(() => _isSaving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final studentId = context.watch<AppState>().remoteStudentId;
    return CalmScaffold(
      title: 'Perfil da aluna',
      child: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            if (studentId != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Card(
                  child: ListTile(
                    leading: const Icon(Icons.cloud_done),
                    title: Text('Perfil conectado ao backend: ID $studentId'),
                    subtitle: const Text('O chat usará este perfil para iniciar as sessões.'),
                  ),
                ),
              ),
            _field(name, 'Nome'),
            _field(age, 'Idade', keyboardType: TextInputType.number),
            _field(subjects, 'Matérias com maior dificuldade'),
            _field(interests, 'Interesses'),
            _field(reading, 'Nível de leitura'),
            _field(math, 'Nível de matemática'),
            _field(triggers, 'Gatilhos de ansiedade'),
            _field(strategies, 'Estratégias que ajudam'),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: _isSaving ? null : _save,
              icon: _isSaving
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.save),
              label: Text(_isSaving ? 'Salvando...' : 'Salvar no backend'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _field(TextEditingController controller, String label, {TextInputType? keyboardType}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: TextFormField(
        controller: controller,
        keyboardType: keyboardType,
        minLines: 1,
        maxLines: label.length > 12 ? 3 : 1,
        validator: (value) => value == null || value.trim().isEmpty ? 'Preencha este campo com calma.' : null,
        decoration: InputDecoration(
          labelText: label,
          filled: true,
          fillColor: Colors.white,
          border: const OutlineInputBorder(),
        ),
      ),
    );
  }
}
