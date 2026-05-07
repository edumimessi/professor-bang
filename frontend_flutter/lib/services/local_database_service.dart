import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

class LocalDatabaseService {
  static final LocalDatabaseService instance = LocalDatabaseService._();
  LocalDatabaseService._();

  Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    final path = join(await getDatabasesPath(), 'professor_bang_local.db');
    _database = await openDatabase(path, version: 1, onCreate: _create);
    return _database!;
  }

  Future<void> _create(Database db, int version) async {
    await db.execute('''
      CREATE TABLE student_profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        difficult_subjects TEXT,
        interests TEXT,
        reading_level TEXT,
        math_level TEXT,
        anxiety_triggers TEXT,
        helpful_strategies TEXT
      )
    ''');
    await db.execute('''
      CREATE TABLE messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        created_at TEXT
      )
    ''');
    await db.execute('''
      CREATE TABLE routine_tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        is_done INTEGER,
        order_index INTEGER
      )
    ''');
    await db.execute('''
      CREATE TABLE achievements(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        created_at TEXT
      )
    ''');
  }

  Future<void> clearHistory() async {
    final db = await database;
    await db.delete('messages');
  }
}
