import shutil
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL_RECORRIDOS = "https://ceia-data.s3.us-east-1.amazonaws.com/trips_2023.zip"
URL_USUARIOS = "https://ceia-data.s3.us-east-1.amazonaws.com/usuarios_ecobici_2023.zip"

RETRIES = 5
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "*/*",
}

FILE_RECORRIDOS = "trips_2023.csv"
FILE_USUARIOS = "usuarios_ecobici_2023.csv"


def _download_zip(url, zip_path):
    """Stream `url` into `zip_path`, retrying on transient network errors."""
    print(f"Descargando {zip_path.name} ...")
    request = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=120) as response, open(zip_path, "wb") as dst:
                shutil.copyfileobj(response, dst)
            break
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if attempt == RETRIES:
                raise
            print(f"  intento {attempt} fallido ({e}); reintentando ...")
            time.sleep(2 * attempt)

    if not zipfile.is_zipfile(zip_path):
        head = zip_path.read_bytes()[:300]
        zip_path.unlink()
        raise RuntimeError(f"{url}: la respuesta no es un zip: {head!r}")


def _ensure_csv(url, filename, path):
    """Make sure `path/filename` exists, downloading and extracting the zip if needed."""
    csv_path = path / filename
    if csv_path.exists():
        # a previous failed download may have left an HTML error page behind
        if csv_path.read_bytes()[:5].lower() not in (b"<html", b"<!doc"):
            return
        csv_path.unlink()
    zip_path = csv_path.with_suffix(".zip")
    if not zip_path.exists():
        _download_zip(url, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        member = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        with zf.open(member) as src, open(csv_path, "wb") as dst:
            shutil.copyfileobj(src, dst)


def load_dataset(path="./dataset/"):
    """Load the Ecobici 2023 datasets, downloading them first if they are missing.

    Returns (df_recorridos, df_usuarios).
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)

    for url, filename in ((URL_RECORRIDOS, FILE_RECORRIDOS), (URL_USUARIOS, FILE_USUARIOS)):
        _ensure_csv(url, filename, path)

    df_recorridos = pd.read_csv(path / FILE_RECORRIDOS)
    # edad_usuario has mixed types; low_memory=False avoids the DtypeWarning
    df_usuarios = pd.read_csv(path / FILE_USUARIOS, low_memory=False)
    print(
        "Datasets cargados correctamente: "
        f"recorridos {df_recorridos.shape[0]:,} filas x {df_recorridos.shape[1]} columnas, "
        f"usuarios {df_usuarios.shape[0]:,} filas x {df_usuarios.shape[1]} columnas"
    )
    return df_recorridos, df_usuarios
