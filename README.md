# API - Importador de XMLs para o Questor

Este projeto tem como objetivo importar automaticamente arquivos XML de NF-e, NFC-e e NFS-e para o sistema Questor via API, otimizando o tempo e reduzindo erros em tarefas repetitivas.

## 🚀 Funcionalidades

- Leitura de arquivos XML a partir de diretórios por empresa
- Envio de dados para o Questor via endpoint `TnArqDPImportarLctoFisNFEXML`
- Geração de log por XML processado
- Leitura de parâmetros e dados de empresas via planilha Excel
- Controle de pastas por empresa e período
- Ignora arquivos cancelados ou inválidos
- Integração com Google Drive (opcional)
- Interface gráfica com seleção de empresas, datas e painel de execução

## 🛠️ Tecnologias utilizadas

- Python 3.x
- Pandas
- openpyxl
- requests
- pyautogui (em versões anteriores)
- tkinter (GUI)
- Firebird / PostgreSQL (consultas e validações externas)
- Google API (Drive e Gmail, opcional)

## 🗂️ Estrutura do Projeto

```
Questor_Farmacias/
├── 1. Bot/               # Scripts principais (.py)
│   ├── main.py
│   ├── base_importador.py
│   ├── corrigir_e_dividir.py
│   ├── importar_questor.py
│   ├── lista_xmls.py
│   └── executar_importacao.py
├── 2. Config/            # Planilhas com parâmetros (datas, filtros, etc.)
├── 3. Empresas/          # Planilha com lista de empresas e CNPJs
├── 4. Logs/              # Logs gerados durante a execução
├── .gitignore            # Arquivos e pastas ignoradas no Git
├── README.md             # Documentação do projeto
└── requirements.txt      # (Opcional) Lista de dependências
```

## ▶️ Como executar o projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/Mangger91/api-importador-questor.git
cd api-importador-questor
```

2. **(Opcional) Crie um ambiente virtual:**

```bash
python -m venv venv
venv\Scripts\activate  # Para Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure as planilhas:**

- Em `2. Config/`: defina as datas, filtros e parâmetros
- Em `3. Empresas/`: insira a lista de empresas, CNPJs e nomes

5. **Execute o script principal:**

```bash
python "1. Bot/main.py"
```
## 👨‍💻 Autor

**Roberto Mangger**  
[LinkedIn](https://www.linkedin.com/in/rmangger/)  
