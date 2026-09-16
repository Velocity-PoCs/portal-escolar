DROP TABLE IF EXISTS funcionarios;
DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS notas;

CREATE TABLE funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    cargo TEXT NOT NULL
);

CREATE TABLE alunos (
    matricula INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    turma TEXT NOT NULL,
    responsavel TEXT,
    telefone TEXT
);

CREATE TABLE notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula INTEGER NOT NULL,
    disciplina TEXT NOT NULL,
    bimestre INTEGER NOT NULL,
    nota REAL NOT NULL,
    FOREIGN KEY (matricula) REFERENCES alunos (matricula)
);

INSERT INTO funcionarios (nome, usuario, senha, cargo) VALUES
    ('Ana Ribeiro', 'ana.ribeiro', 'escola2024', 'Secretaria'),
    ('Carlos Mendes', 'carlos.mendes', 'diretor@123', 'Diretor'),
    ('Beatriz Souza', 'beatriz.souza', 'prof456', 'Coordenacao');

INSERT INTO alunos (matricula, nome, turma, responsavel, telefone) VALUES
    (20240001, 'Lucas Almeida', '6A', 'Marta Almeida', '(11) 98811-0001'),
    (20240002, 'Julia Ferreira', '6A', 'Paulo Ferreira', '(11) 98811-0002'),
    (20240003, 'Pedro Nascimento', '6B', 'Sonia Nascimento', '(11) 98811-0003'),
    (20240004, 'Mariana Costa', '7A', 'Renato Costa', '(11) 98811-0004'),
    (20240005, 'Gabriel Rocha', '7A', 'Fernanda Rocha', '(11) 98811-0005'),
    (20240006, 'Isabela Martins', '7B', 'Cesar Martins', '(11) 98811-0006'),
    (20240007, 'Rafael Lima', '8A', 'Vera Lima', '(11) 98811-0007'),
    (20240008, 'Camila Barbosa', '8B', 'Jorge Barbosa', '(11) 98811-0008');

INSERT INTO notas (matricula, disciplina, bimestre, nota) VALUES
    (20240001, 'Matematica', 1, 8.5),
    (20240001, 'Portugues', 1, 7.0),
    (20240001, 'Ciencias', 1, 9.0),
    (20240002, 'Matematica', 1, 6.5),
    (20240002, 'Portugues', 1, 8.0),
    (20240004, 'Matematica', 1, 9.5),
    (20240004, 'Historia', 1, 7.5),
    (20240007, 'Geografia', 1, 8.0);
