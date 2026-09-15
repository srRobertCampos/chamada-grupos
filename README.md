# Chamada de grupos interdisciplinares

Projeto didático em Python e Django para registrar atendimentos em grupos de até 10 usuários. A chamada diária alimenta uma folha mensal horizontal, que pode ser vista no navegador e baixada em Excel.

## O que já funciona

- Login; cadastro de profissionais, usuários, grupos e participantes no painel administrativo.
- Agenda do dia por horário e dupla de profissionais.
- Registro de Presença (P), Falta (F), Falta justificada (FJ), Atendimento Familiar (AF) e Atendimento Extra (AE).
- Folha mensal gerada automaticamente a partir dos lançamentos. Alterações no lançamento aparecem imediatamente na folha.
- Envio da folha mensal por e-mail após salvar a chamada, quando SMTP e e-mail de destino estiverem configurados; envio manual também disponível na folha.

## 1. Instalação local no Windows

Instale Python 3.14 e Git. Abra o PowerShell na pasta deste projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abra `http://127.0.0.1:8000/`. Entre com a conta criada. O painel de cadastro fica em `http://127.0.0.1:8000/admin/`.

## 2. Primeiro cadastro

No painel administrativo, cadastre **dois profissionais**, depois os **usuários**. Cadastre um **grupo** com dia da semana, horário, dupla e participantes. O sistema limita cada grupo a 10 participantes ativos. Para guardar histórico, desative um usuário ou participação ao encerrar o atendimento, em vez de apagar registros antigos. Em **Configurações**, cadastre o e-mail destinatário.

## 3. Uso diário

Abra a página inicial. Os grupos previstos aparecem por horário. Marque cada usuário e clique em **Salvar chamada**. A folha mensal já estará atualizada; use **Folha mensal** para conferir ou baixar Excel. A tela **Atendimento extra/familiar** permite registrar essas modalidades fora da chamada regular. Nesta primeira versão, há um registro por usuário, grupo e data: um novo lançamento na mesma combinação substitui o anterior.

## 4. E-mail

Configure as variáveis de ambiente `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` e `SMTP_FROM` no PowerShell antes de iniciar o servidor. Exemplo:

```powershell
$env:SMTP_HOST = 'smtp.seu-provedor.com'
$env:SMTP_PORT = '587'
$env:SMTP_USER = 'conta@exemplo.com'
$env:SMTP_PASSWORD = 'token-do-provedor'
$env:SMTP_FROM = 'conta@exemplo.com'
```

O serviço SMTP precisa aceitar STARTTLS na porta informada. Não coloque senhas no código ou no GitHub. Sem essas variáveis, a chamada e a planilha continuam funcionando, mas o envio automático fica desativado.

## 5. Testes e controle de versão

```powershell
.\.venv\Scripts\python.exe manage.py test
git init
git add .
git commit -m "Primeira versão da chamada de grupos"
```

Para publicar, crie um **repositório privado** no GitHub e siga os comandos de conexão com um repositório existente que o GitHub mostrar. Confira antes que `db.sqlite3`, `.env` e `.venv` não apareçam em `git status`. O banco local contém dados pessoais e nunca deve ser enviado ao repositório.

## Próximas etapas sugeridas

1. Testar o fluxo com dados fictícios e ajustar o formato da folha à folha usada na instituição.
2. Definir se Atendimento Familiar e Extra podem coexistir com Presença no mesmo dia; isso exige múltiplos eventos por usuário/data.
3. Criar permissões separadas para administradores e profissionais, rotinas de backup e, antes de hospedar, configurar HTTPS, chave secreta própria, `DJANGO_DEBUG=0` e banco PostgreSQL.

Este projeto é uma base de aprendizagem e deve ser validado com a instituição antes de registrar dados reais.
