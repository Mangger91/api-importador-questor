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

