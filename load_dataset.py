import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL_RECORRIDOS = "https://data.buenosaires.gob.ar/dataset/bicicletas-publicas/resource/ff671909-6860-4398-8d0a-8f2389cb2780/download"
URL_USUARIOS = "https://data.buenosaires.gob.ar/dataset/bicicletas-publicas/resource/edb5ed27-8506-43f0-88ce-3e5c0aa1a406/download"

FILE_RECORRIDOS = "trips_2023.csv"
FILE_USUARIOS = "usuarios_ecobici_2023.csv"


def _download_csv(url, filename, path):
    """Download `url` into `path/filename`; extracts the CSV if the response is a zip."""
    print(f"Descargando {filename} ...")
    with urllib.request.urlopen(url) as response:
        content = response.read()

    if zipfile.is_zipfile(io.BytesIO(content)):
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            member = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
            with zf.open(member) as src, open(path / filename, "wb") as dst:
                dst.write(src.read())
    else:
        (path / filename).write_bytes(content)


def load_dataset(path="./dataset/"):
    """Load the Ecobici 2023 datasets, downloading them first if they are missing.

    Returns (df_recorridos, df_usuarios).
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)

    for url, filename in ((URL_RECORRIDOS, FILE_RECORRIDOS), (URL_USUARIOS, FILE_USUARIOS)):
        if not (path / filename).exists():
            _download_csv(url, filename, path)

    df_recorridos = pd.read_csv(path / FILE_RECORRIDOS)
    # edad_usuario has mixed types; low_memory=False avoids the DtypeWarning
    df_usuarios = pd.read_csv(path / FILE_USUARIOS, low_memory=False)
    return df_recorridos, df_usuarios
