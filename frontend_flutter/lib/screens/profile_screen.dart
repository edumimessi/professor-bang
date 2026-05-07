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

  void _save() {
    if (!_formKey.currentState!.validate()) return;
    context.read<AppState>().updateProfile(StudentProfile(
          name: name.text,
          age: int.tryParse(age.text) ?? 14,
          difficultSubjects: subjects.text,
          interests: interests.text,
          readingLevel: reading.text,
          mathLevel: math.text,
          anxietyTriggers: triggers.text,
          helpfulStrategies: strategies.text,
        ));
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Perfil salvo localmente.')));
  }

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: 'Perfil da aluna',
      child: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            _field(name, 'Nome'),
            _field(age, 'Idade', keyboardType: TextInputType.number),
            _field(subjects, 'Matérias com maior dificuldade'),
            _field(interests, 'Interesses'),
            _field(reading, 'Nível de leitura'),
            _field(math, 'Nível de matemática'),
            _field(triggers, 'Gatilhos de ansiedade'),
            _field(strategies, 'Estratégias que ajudam'),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: _save, child: const Text('Salvar perfil local')),
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
        minLines: label.length > 12 ? 1 : 1,
        maxLines: label.length > 12 ? 3 : 1,
        validator: (value) => value == null || value.trim().isEmpty ? 'Preencha este campo com calma.' : null,
        decoration: InputDecoration(labelText: label, filled: true, fillColor: Colors.white, border: const OutlineInputBorder()),
      ),
    );
  }
}
