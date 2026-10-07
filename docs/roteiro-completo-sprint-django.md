# Roteiro Completo: Sprint Relâmpago em Django (Times e Jogadores de Futebol)

**Disciplina:** Desenvolvimento de Sistemas Web
**Dupla:** Jean e Gustavo
**Duração:** 1 semana (5 dias)
**Sprint Goal:** *Entregar um sistema Django funcional de cadastro de times e jogadores de futebol, com dois CRUDs integrados por um menu comum.*

> **Atenção:** o documento da atividade pede um "Sistema de Projetos e Tarefas". Confirmar com o professor se o tema de futebol é aceito. Se não for, trocar `Time` por `Projeto` e `Jogador` por `Tarefa`; a estrutura continua idêntica.

## Sumário

1. [Visão geral e modelagem](#1-visão-geral-e-modelagem)
2. [Regras de ouro](#2-regras-de-ouro)
3. [Dia 1: Sprint Planning](#3-dia-1-sprint-planning-juntos)
4. [Backlog: as 7 issues](#4-backlog-as-7-issues)
5. [Fluxo Git de cada issue](#5-fluxo-git-de-cada-issue)
6. [Modelo de Pull Request e Code Review](#6-modelo-de-pull-request-e-code-review)
7. [Dias 2 a 4: Dailies](#7-dias-2-a-4-dailies)
8. [Dia 5: Review e Retrospective](#8-dia-5-sprint-review-e-retrospective)
9. [Problemas comuns](#9-problemas-comuns)
10. [Checklist de avaliação](#10-checklist-de-avaliação)

---

## 1. Visão geral e modelagem

### Entidades (relação 1 para N)

| Documento | Nosso tema | Campos |
|---|---|---|
| `Projeto` | `Time` | `nome` (CharField), `cidade` (CharField), `data_fundacao` (DateField) |
| `Tarefa` | `Jogador` | `nome` (CharField), `posicao` (CharField com choices), `ativo` (BooleanField), `time` (ForeignKey para `Time`, `on_delete=models.CASCADE`) |

### Esboço dos models

```python
from django.db import models


class Time(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    data_fundacao = models.DateField()

    def __str__(self):
        return self.nome


class Jogador(models.Model):
    POSICOES = [
        ("GOL", "Goleiro"),
        ("ZAG", "Zagueiro"),
        ("LAT", "Lateral"),
        ("MEI", "Meia"),
        ("ATA", "Atacante"),
    ]

    nome = models.CharField(max_length=100)
    posicao = models.CharField(max_length=3, choices=POSICOES)
    ativo = models.BooleanField(default=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="jogadores")

    def __str__(self):
        return self.nome
```

### Estrutura

- **Um único app** (`core`) com os dois models, views, forms, urls e templates. O documento pede só "App criado e registrado em `INSTALLED_APPS`".
- Como `Jogador` depende de `Time` por causa da `ForeignKey`, manter tudo no mesmo app evita configuração extra e conflitos de merge.

### Divisão de papéis

| Bloco | Dev | PO (valida) |
|---|---|---|
| Bloco 1: setup (US01) | Juntos | Juntos |
| Bloco 2: CRUD de Times (US02 a US04) | Jean | Gustavo |
| Bloco 3: CRUD de Jogadores (US05 e US06) | Gustavo | Jean |
| Bloco 4: integração (US07) | Juntos | Juntos |

Os blocos 2 e 3 podem ser trocados. O importante é que **quem desenvolve não valida o próprio trabalho**.

---

## 2. Regras de ouro

1. **Proibido commitar direto na `main`.** Cada issue tem sua própria branch (ex.: `feature/crud-times`).
2. **Pull Request obrigatório** para todo código novo entrar na `main`.
3. **Code Review cruzado:** o colega revisa, testa e aprova antes do merge.

---

## 3. Dia 1: Sprint Planning (juntos)

### 3.1 Repositório

- [ ] Criar o repositório na conta pessoal de um dos dois (organização não é necessária)
- [ ] Em **Settings → Collaborators**, adicionar o outro; ele precisa aceitar o convite antes de criar branches e aprovar PRs
- [ ] Criar um `README.md` com nome do projeto, integrantes e Sprint Goal
- [ ] (Opcional) Proteger a `main` em **Settings → Branches**, exigindo PR e 1 aprovação. No plano gratuito isso costuma exigir repositório público

> Se o repositório ainda estiver vazio, o primeiro push precisa ir para a `main`, porque o PR precisa de uma branch base existente. Depois disso, tudo por branch.

### 3.2 GitHub Projects (Kanban)

- [ ] Criar o Project no perfil e vincular ao repositório
- [ ] Colunas: **Backlog, To Do, In Progress, In Review, Done**
- [ ] Criar as 7 issues da seção 4 e colocar todas em Backlog
- [ ] Mover as issues da sprint para **To Do**
- [ ] Atribuir um responsável (assignee) em cada issue
- [ ] Registrar o Sprint Goal no quadro ou no README

### 3.3 Ambiente local (fish shell)

```fish
python -m venv venv
source venv/bin/activate.fish
pip install django
django-admin startproject config .
python manage.py startapp core
```

Crie o `.gitignore` **antes** do primeiro `git add .`:

```gitignore
venv/
.venv/
__pycache__/
*.pyc
db.sqlite3
.env
```

Depois confira com `git status` que a venv não aparece na lista.

---

## 4. Backlog: as 7 issues

Cada issue abaixo traz título, descrição, critérios de aceite, branch, responsável e uma sugestão de mensagem de commit.

---

### [US01] Configuração do projeto Django e banco de dados

**Responsável:** Juntos
**Branch:** `feature/setup-inicial`

**Descrição:** Como desenvolvedor, quero inicializar o projeto Django, configurar o `settings.py` (banco de dados e app `core`) e criar a estrutura inicial, para que a equipe tenha uma base funcional para desenvolver.

**Critérios de aceite:**
- [ ] Projeto Django criado e rodando localmente sem erros
- [ ] App criado e registrado em `INSTALLED_APPS`
- [ ] `.gitignore` configurado (venv, `db.sqlite3`, arquivos `.pyc`)

**Commit sugerido:**
```
chore: configura projeto Django e cria app core

- inicializa projeto Django
- cria app core e registra em INSTALLED_APPS
- adiciona .gitignore (venv, db.sqlite3, *.pyc)
```

> Se o setup inicial já foi para a `main`, crie a issue mesmo assim, comente nela o que foi feito e linke o commit. Daqui para frente, tudo por branch e PR.

---

### [US02] Model e migrations de Time

**Responsável:** Jean (validação: Gustavo)
**Branch:** `feature/model-time`

**Descrição:** Como usuário, quero cadastrar os dados básicos de um time (nome, cidade e data de fundação), para ter a base onde os jogadores serão vinculados.

**Critérios de aceite:**
- [ ] Model `Time` criado com os campos corretos
- [ ] Migrations geradas e aplicadas com sucesso
- [ ] Model registrado no Django Admin

**Commit sugerido:** `feat: adiciona model Time e registra no admin`

---

### [US03] Listagem e cadastro de Times (Create & Read)

**Responsável:** Jean (validação: Gustavo)
**Branch:** `feature/times-create-read`

**Descrição:** Como usuário, quero visualizar todos os times cadastrados e criar um novo por uma interface web, para gerenciar os times sem usar o Admin.

**Critérios de aceite:**
- [ ] View de listagem e cadastro implementada
- [ ] Formulário Django (`ModelForm`) validando campos obrigatórios
- [ ] Template HTML estruturado exibindo os dados

**Commit sugerido:** `feat: adiciona listagem e cadastro de times`

---

### [US04] Edição e exclusão de Times (Update & Delete)

**Responsável:** Jean (validação: Gustavo)
**Branch:** `feature/times-update-delete`

**Descrição:** Como usuário, quero atualizar as informações de um time ou excluí-lo, para manter o cadastro sempre correto.

**Critérios de aceite:**
- [ ] Views de Update e Delete implementadas com rotas dinâmicas (`pk`)
- [ ] Mensagens de feedback visual após salvar ou excluir

**Commit sugerido:** `feat: adiciona edição e exclusão de times`

---

### [US05] Model e relacionamento de Jogadores

**Responsável:** Gustavo (validação: Jean)
**Branch:** `feature/model-jogador`

**Descrição:** Como usuário, quero cadastrar jogadores associados a um time específico, para saber quem joga em cada time.

**Critérios de aceite:**
- [ ] Model `Jogador` criado com os campos (`nome`, `posicao`, `ativo`) e `ForeignKey` para `Time` (`on_delete=models.CASCADE`)
- [ ] Migrations aplicadas e models registrados no Admin

**Commit sugerido:** `feat: adiciona model Jogador com relação ao Time`

> **Atenção:** só criar o `Jogador` depois que o model `Time` (US02) estiver na `main`, senão a migration depende de um model que ainda não existe. Antes de começar, atualize sua branch com `git pull origin main`.

---

### [US06] CRUD completo de Jogadores

**Responsável:** Gustavo (validação: Jean)
**Branch:** `feature/crud-jogadores`

**Descrição:** Como usuário, quero gerenciar os jogadores pertencentes a um time (criar, listar, editar e excluir), para manter o elenco atualizado.

**Critérios de aceite:**
- [ ] Listagem de jogadores exibindo a qual time cada um pertence
- [ ] Formulário de criação/edição selecionando o time via `<select>` (dropdown)
- [ ] Exclusão funcionando corretamente com redirecionamento adequado

**Commit sugerido:** `feat: adiciona CRUD de jogadores`

---

### [US07] Navegação integrada (template base)

**Responsável:** Juntos
**Branch:** `feature/template-base`

**Descrição:** Como usuário, quero navegar facilmente entre as páginas do sistema por um menu superior comum, para não precisar digitar URLs.

**Critérios de aceite:**
- [ ] Template base (`base.html`) criado com herança (`{% extends %}`) aplicada em todas as páginas
- [ ] Links de navegação funcionais no layout
- [ ] Última rodada de Code Review no GitHub via Pull Request, com aprovação mútua e merge para a `main`

**Commit sugerido:** `feat: adiciona template base com menu de navegação`

---

## 5. Fluxo Git de cada issue

### 5.1 Passo a passo

1. Mover o card para **In Progress**.
2. Criar a branch a partir da `main` atualizada:

```fish
git switch main
git pull
git switch -c feature/nome-da-branch
```

3. Desenvolver e commitar em pequenos passos, no padrão Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
4. Subir a branch:

```fish
git push -u origin feature/nome-da-branch
```

5. Abrir o PR no GitHub com `Closes #número` na descrição e mover o card para **In Review**.
6. O colega testa, comenta e aprova.
7. Merge na `main`. A issue fecha sozinha e o card vai para **Done**.
8. Voltar para a `main` e atualizar:

```fish
git switch main
git pull
```

### 5.2 Mantendo a branch atualizada

Se a `main` recebeu mudanças enquanto você trabalhava:

```fish
git switch main
git pull
git switch feature/nome-da-branch
git merge main
```

### 5.3 Dicas de commit

- Mensagem no imperativo/presente, curta (até uns 50 caracteres no título), sem ponto final.
- Um commit por ideia. Evite commits do tipo "ajustes" ou "arrumando coisas".
- Nunca commitar `venv`, `db.sqlite3`, `.env` ou arquivos `.pyc`.

---

## 6. Modelo de Pull Request e Code Review

### 6.1 Descrição do PR

```markdown
## O que foi feito
(resumo curto)

## Issue relacionada
Closes #

## Como testar
1.
2.

## Checklist
- [ ] Critérios de aceite da issue atendidos
- [ ] Rodei o projeto localmente sem erros
- [ ] Migrations incluídas (se houve mudança em model)
- [ ] Nenhum arquivo indevido commitado (venv, db.sqlite3)
```

### 6.2 Checklist do revisor

- [ ] Baixei a branch e rodei o projeto localmente
- [ ] Testei o fluxo da issue na prática (criar, listar, editar, excluir)
- [ ] Conferi cada critério de aceite da issue
- [ ] Código legível, sem sobras (prints, código comentado)
- [ ] Commits limpos e com mensagens claras
- [ ] Deixei comentários objetivos no PR e, se tudo certo, aprovei

```fish
git fetch origin
git switch feature/nome-da-branch
python manage.py migrate
python manage.py runserver
```

---

## 7. Dias 2 a 4: Dailies

**Daily Standup de 5 minutos por dia**, presencial ou no chat. Modelo de mensagem:

```
Ontem: o que fiz
Hoje: o que vou fazer
Impedimentos: nenhum / descreva
```

**Depois de cada daily, atualize o quadro.** A avaliação olha a higiene do Kanban: os cards precisam estar nas colunas certas e refletir o andamento real.

### Cronograma sugerido

| Dia | Foco |
|---|---|
| Dia 1 | Planning, repositório, quadro, issues e US01 (juntos) |
| Dia 2 | Jean: US02 e US03. Gustavo: US05 (após o `Time` estar na `main`) |
| Dia 3 | Jean: US04. Gustavo: US06. Code reviews cruzados |
| Dia 4 | Finalizar pendências, corrigir comentários de review, começar US07 |
| Dia 5 | US07 (juntos), Review e Retrospective |

---

## 8. Dia 5: Sprint Review e Retrospective

### 8.1 Sprint Review (demo)

- [ ] Sistema rodando localmente sem erros
- [ ] Cada PO valida os critérios de aceite das issues que revisou
- [ ] Demonstrar o fluxo completo: cadastrar time, editar, cadastrar jogadores vinculados, listar, excluir
- [ ] Menu de navegação funcionando em todas as páginas
- [ ] Todas as issues em **Done** e quadro atualizado

### 8.2 Retrospective (rápida)

- O que funcionou bem?
- O que não funcionou?
- O que vamos ajustar na próxima sprint?

---

## 9. Problemas comuns

### Tirar a venv do commit

**Ainda não commitou** (só deu `git add .`):

```fish
git rm -r --cached venv
git status
```

**Já commitou, mas não deu push:**

```fish
git rm -r --cached venv
git add .gitignore
git commit --amend
```

**Já deu push:** faça um novo commit removendo a venv:

```fish
git rm -r --cached venv
git add .gitignore
git commit -m "chore: remove venv do versionamento"
git push
```

> O `--cached` remove do controle de versão sem apagar a pasta do disco. Reescrever histórico com `--amend` e `git push --force-with-lease` só vale em branch ainda não mergeada, e combine com o colega antes.

### Conflito de migrations

Se as duas branches geraram migrations e deu conflito: atualize sua branch com a `main`, apague **apenas a sua migration nova**, rode `python manage.py makemigrations` de novo e commite.

### Esqueci de criar a branch e já commitei na `main`

Se ainda não deu push:

```fish
git branch feature/nome-da-branch
git reset --hard origin/main
git switch feature/nome-da-branch
```

---

## 10. Checklist de avaliação

- [ ] **Higiene do quadro Kanban:** o GitHub Projects reflete fielmente o andamento real
- [ ] **Qualidade dos artefatos:** issues com critérios de aceite claros e commits limpos
- [ ] **Prática de engenharia:** code review efetivo via Pull Requests, sem commits diretos na `main`
- [ ] **Definição de Pronto (DoD):** sistema Django funcional, integrado e atendendo aos requisitos no final da semana
