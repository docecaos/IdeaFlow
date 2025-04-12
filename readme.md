# IdeaFlow SaaS
O **IdeaFlow** é uma aplicação desktop desenvolvida em **Python** utilizando **Tkinter** para interface gráfica e **SQLite** para armazenamento de dados. O software permite a criação, organização e gerenciamento de ideias, facilitando o registro e acompanhamento de projetos pessoais ou profissionais.

## Funcionalidades

- **Criar e armazenar ideias**: Inclui título e detalhes.
- **Filtrar ideias**: Opções para visualizar **Todas**, **Ativas** e **Concluídas**.
- **Pesquisar ideias**: Busca por palavras-chave.
- **Interface moderna**: Com botões personalizados e tema escuro.
- **Barra de status**: Informa ações recentes.
- **Rolagem suave**: Para navegação na lista de ideias.

## Tecnologias Utilizadas

- **Python** (versão 3.x)
- **Tkinter** (para interface gráfica)
- **SQLite3** (para armazenamento local de dados)
- **sv_ttk** (para tema moderno)

## Instalação

### Requisitos

Certifique-se de ter o **Python 3.x** instalado em seu sistema.

### Passos

1. Clone este repositório ou baixe os arquivos:

git clone https://github.com/docecaos/IdeaFlow.git
cd IdeaFlow

2. Instale as dependências necessárias:

pip install sv_ttk

text

3. Execute o programa:

python main.py

## Uso

- **Adicionar uma nova ideia**: Clique no botão "+ Nova Ideia", preencha o título e detalhes, e clique em "Salvar".
- **Filtrar ideias**: Utilize os botões de filtro na barra lateral para visualizar ideias ativas ou concluídas.
- **Pesquisar ideias**: Digite um termo na barra de pesquisa para encontrar ideias relacionadas.
- **Atualizar lista**: Clique no botão "Atualizar" para carregar novas ideias.

## Estrutura do Projeto

IdeaFlow/
│── main.py # Arquivo principal
│── database.db # Banco de dados SQLite
│── assets/ # Recursos visuais (se houver)
└── README.md # Documentação do projeto

text

## Contribuição

Sinta-se à vontade para sugerir melhorias ou contribuir com novas funcionalidades. Basta fazer um fork do repositório e abrir um Pull Request.
