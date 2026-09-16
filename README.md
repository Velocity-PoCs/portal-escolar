# Portal Escolar — EE Jardim das Flores

Sistema web interno para a secretaria acadêmica da Escola Estadual Jardim das Flores.
Permite consultar alunos matriculados, visualizar fichas com dados do responsável e
notas por bimestre, e listar turmas.

## Funcionalidades

- Autenticação de funcionários (secretaria, coordenação, direção)
- Painel com totais de alunos e turmas
- Busca de alunos por nome
- Ficha do aluno com notas por disciplina e bimestre
- Listagem de alunos por turma

## Tecnologias

- Python 3
- Flask
- SQLite

## Como executar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate  |  Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

O banco `escola.db` é criado automaticamente na primeira execução, a partir de
`schema.sql`. Acesse http://127.0.0.1:5000

### Credenciais de exemplo

| Usuário         | Senha         | Cargo       |
|-----------------|---------------|-------------|
| ana.ribeiro     | escola2024    | Secretaria  |
| carlos.mendes   | diretor@123   | Diretor     |

## Estrutura

```
portal-escolar/
├── app.py            # rotas e lógica da aplicação
├── schema.sql        # estrutura e dados iniciais
├── requirements.txt
├── templates/        # páginas Jinja2
└── static/           # estilos
```
