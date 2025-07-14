import zipfile
from pathlib import Path
import shutil
import os

PASTA_XMLS = Path(r"\\192.168.100.233\5. Outputs\XML")
DESTINO_ZIPS = PASTA_XMLS / "Corrigidos"
DESTINO_ZIPS.mkdir(exist_ok=True)

LIMITE_MB = 50

def gerar_zip_corrigido(nome_vetorfarma):
    pasta_empresa = PASTA_XMLS / nome_vetorfarma
    if not pasta_empresa.exists():
        print(f"[ERRO] Pasta não encontrada: {pasta_empresa}")
        return

    xmls = list(pasta_empresa.glob("*.xml"))
    if not xmls:
        print(f"[ERRO] Nenhum XML em: {pasta_empresa}")
        return

    tamanho_total_mb = sum(xml.stat().st_size for xml in xmls) / (1024 * 1024)

    if tamanho_total_mb <= LIMITE_MB:
        zip_destino = DESTINO_ZIPS / f"{nome_vetorfarma}.zip"
        with zipfile.ZipFile(zip_destino, 'w', compression=zipfile.ZIP_STORED) as novo_zip:
            for xml in xmls:
                novo_zip.write(xml, arcname=xml.name)
        print(f"[OK] Gerado único: {zip_destino.name}")
    else:
        # Divide em 2 partes equilibradas
        meio = len(xmls) // 2 + len(xmls) % 2
        partes = [xmls[:meio], xmls[meio:]]

        for i, parte in enumerate(partes, start=1):
            nome_zip = f"{nome_vetorfarma}-parte{i}.zip"
            zip_destino = DESTINO_ZIPS / nome_zip
            with zipfile.ZipFile(zip_destino, 'w', compression=zipfile.ZIP_STORED) as novo_zip:
                for xml in parte:
                    novo_zip.write(xml, arcname=xml.name)
            print(f"[OK] Gerado dividido: {zip_destino.name}")

# Executa para todas as pastas de empresa
for pasta in PASTA_XMLS.iterdir():
    if pasta.is_dir() and (pasta / "dummy").exists() is False:  # ignora não-empresas
        gerar_zip_corrigido(pasta.name)

print("Processo concluído.")
