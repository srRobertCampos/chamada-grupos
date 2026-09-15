# Sistema de Registro de Atendimentos em Grupo

Aplicação web para organizar grupos interdisciplinares, registrar atendimentos diários e gerar folhas mensais de frequência.

O projeto foi desenvolvido em Python e Django para uso local. Os dados são armazenados em SQLite e a folha mensal pode ser consultada no navegador, exportada para Excel e enviada por e-mail.

## Situação do projeto

Primeira versão funcional, destinada a testes com dados fictícios.

Funcionalidades disponíveis:

- autenticação de acesso;
- cadastro de profissionais e usuários;
- criação de grupos por dia da semana e horário;
- definição da dupla responsável por cada grupo;
- inclusão de até 10 usuários ativos por grupo;
- exibição dos atendimentos previstos para a data selecionada;
- registro de presença, falta e modalidades de atendimento;
- geração automática da folha mensal;
- exportação da folha em formato Excel;
- envio da planilha por e-mail via SMTP;
- manutenção dos cadastros pelo painel administrativo do Django.

## Registros de atendimento

| Código | Descrição |
|---|---|
| `P` | Presença |
| `F` | Falta |
| `FJ` | Falta justificada |
| `AF` | Atendimento familiar |
| `AE` | Atendimento extra |

Cada combinação de data, grupo e usuário possui um registro. Se outro registro for feito para a mesma combinação, o valor anterior será atualizado.

## Regras de negócio

- Cada grupo possui um dia da semana, horário e dois profissionais responsáveis.
- Os dois profissionais de um grupo devem ser diferentes.
- Cada grupo aceita no máximo 10 participantes ativos.
- A página inicial apresenta somente os grupos programados para a data selecionada.
- A folha mensal é calculada a partir dos registros diários.
- Usuários e participações encerrados devem ser desativados para preservar o histórico.
- Atendimento familiar e atendimento extra podem ser registrados em uma tela própria.

## Tecnologias

- Python 3.14
- Django 6.1
- SQLite
- openpyxl
- HTML e CSS
- Git e GitHub

## Estrutura principal

```text
chamada_grupos/
├── atendimentos/          # Regras, telas, modelos e testes
│   ├── migrations/        # Histórico da estrutura do banco
│   ├── templates/         # Páginas HTML
│   ├── admin.py           # Painel administrativo
│   ├── models.py          # Estrutura dos dados
│   ├── tests.py           # Testes automatizados
│   ├── urls.py            # Rotas do módulo
│   └── views.py           # Fluxos e geração do Excel
├── config/                # Configuração geral do Django
├── manage.py              # Comandos administrativos
└── requirements.txt       # Dependências
```

## Instalação no Windows com PyCharm

### 1. Abrir o projeto

No PyCharm, selecione **File > Open** e abra a pasta que contém o arquivo `manage.py`.

### 2. Configurar o interpretador

Abra **Settings > Project > Python Interpreter**. Adicione um interpretador local do tipo **Virtualenv** e use um ambiente chamado `.venv`.

### 3. Instalar e preparar a aplicação

No terminal do PyCharm, execute:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Se `python` não usar o ambiente configurado, substitua-o pelo caminho do interpretador selecionado no PyCharm.

### 4. Iniciar o servidor

```powershell
python manage.py runserver
```

A aplicação ficará disponível em:

- sistema: <http://127.0.0.1:8000/>
- painel administrativo: <http://127.0.0.1:8000/admin/>

Use `Ctrl+C` no terminal para encerrar o servidor.

## Configuração inicial

No painel administrativo, faça os cadastros nesta ordem:

1. profissionais;
2. usuários;
3. grupos, horários e participantes;
4. e-mail destinatário em **Configurações**.

Depois, abra a página inicial e selecione uma data que corresponda ao dia da semana do grupo cadastrado.

## Envio por Gmail

O envio usa o servidor SMTP do Gmail com uma senha de app. Configure as variáveis no terminal antes de iniciar o servidor:

```powershell
$env:SMTP_HOST = 'smtp.gmail.com'
$env:SMTP_PORT = '587'
$env:SMTP_USER = 'conta@gmail.com'
$env:SMTP_FROM = 'conta@gmail.com'
$senha = Read-Host 'Senha de app' -AsSecureString
$env:SMTP_PASSWORD = [System.Net.NetworkCredential]::new('', $senha).Password.Replace(' ', '')
python manage.py runserver
```

A senha de app deve ser criada na Conta Google usada em `SMTP_USER`. As variáveis permanecem somente durante a sessão atual do terminal.

Credenciais não devem ser registradas em arquivos versionados. O arquivo `.env.example` contém somente os nomes das configurações esperadas.

## Testes

```powershell
python manage.py test
python manage.py check
```

Os testes atuais verificam o lançamento da chamada, a atualização da planilha mensal e a restrição do grupo ao dia programado.

## Controle de versão

Fluxo básico para registrar uma alteração:

```powershell
git status
git add .
git commit -m "Descreve a alteração realizada"
git push
```

O arquivo `db.sqlite3`, o ambiente `.venv` e arquivos de credenciais estão ignorados pelo Git. O GitHub armazena o código e a documentação; os cadastros e registros permanecem no banco local.

## Segurança e dados pessoais

Esta versão deve ser avaliada com dados fictícios antes do uso institucional. Para utilizar dados reais, é necessário definir controle de acesso, cópias de segurança, prazo de retenção, responsabilidade pelo tratamento dos dados e endereço autorizado para receber as planilhas.

O banco `db.sqlite3` pode conter nomes, datas de nascimento e registros de atendimento. Ele não deve ser publicado no GitHub ou enviado sem autorização.

## Próximos marcos

- criar uma rotina de backup e restauração do banco;
- separar permissões de administradores e profissionais;
- adequar a folha mensal ao modelo oficial da instituição;
- registrar histórico dos envios de e-mail;
- avaliar múltiplos atendimentos para o mesmo usuário no mesmo dia;
- preparar PostgreSQL, HTTPS e configurações de produção antes da hospedagem.
