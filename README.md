# Análisis de Datos - CEIA

Este repositorio corresponde al trabajo integrador para la **Carrera de Especialización en Inteligencia Artificial (CEIA)** de la **Universidad Nacional de Buenos Aires (UBA)**.

## Requisitos Previos

- Python 3.12 o superior
- `uv` - gestor de paquetes moderno para Python (instalar globalmente)

## Configuración Inicial

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd data-anlysis-ceia
```

### 2. Instalar dependencias

Usar `uv` para sincronizar las dependencias del proyecto:

```bash
uv sync
```

Esto instalará todas las dependencias especificadas en `pyproject.toml` y configurará el entorno virtual.

### 3. Agregar el dataset

El dataset debe ser agregado manualmente en la carpeta `/dataset` de este repositorio.

#### Dataset: Recorrido de Ecobicis 2023

Se utiliza el dataset **"Recorrido de Ecobicis año 2023"**, que contiene datos del sistema de bicicletas públicas de la Ciudad de Buenos Aires.

**Ubicación del archivo:**
```
dataset/trips_2023.csv
```

El archivo `trips_2023.csv` contiene registros de viajes realizados con Ecobici durante el año 2023, incluyendo información como:
- Información de estaciones de origen y destino
- Tiempos de inicio y fin de viaje
- Tipo de usuario
- Duración del viaje

**Estructura esperada del repositorio:**
```
data-anlysis-ceia/
├── dataset/
│   └── trips_2023.csv
├── notebook.ipynb
├── actividad-2.ipynb
├── pyproject.toml
├── uv.lock
└── ...
```

## Ejecución

El análisis se desarrolla en notebooks de Jupyter (`notebook.ipynb`, `actividad-2.ipynb`).

Jupyter está incluido como dependencia de desarrollo del proyecto (ver `pyproject.toml`), por lo que no requiere instalación adicional: `uv sync` ya lo instala en el entorno virtual del proyecto.

Para correr el análisis interactivo:

```bash
uv run jupyter notebook .
```

Esto abrirá Jupyter en el navegador permitiendo explorar y ejecutar los notebooks del proyecto de forma interactiva.

> **Nota:** No uses el comando `jupyter` o `jup` sin el prefijo `uv run`, ya que dependen de que Jupyter esté instalado globalmente en el sistema. Usar siempre `uv run jupyter notebook .` asegura que se ejecute con las dependencias correctas del proyecto, sin importar la computadora.

## Gestión de Dependencias

Usar los siguientes comandos para manejar dependencias:

- **Agregar un paquete**: `uv add <nombre-paquete>`
- **Agregar dependencia de desarrollo**: `uv add --dev <nombre-paquete>`
- **Sincronizar cambios**: `uv sync`
- **Actualizar dependencias**: `uv sync --refresh`

Todas las dependencias se registran en `uv.lock` para garantizar reproducibilidad entre entornos.

## Estructura del Proyecto

- `pyproject.toml` — Metadatos del proyecto y definición de dependencias
- `uv.lock` — Archivo de bloqueo de dependencias (no editar manualmente)
- `.python-version` — Especificación de versión de Python para `uv`
- `notebook.ipynb` / `actividad-2.ipynb` — Notebooks con el análisis de datos
- `dataset/` — Carpeta para almacenar los datasets de entrada

## Notas

- Las modificaciones a las dependencias se registran en `uv.lock` para asegurar builds reproducibles
- El proyecto utiliza **pandas** como dependencia principal para manipulación y análisis de datos
- **Jupyter** está declarado como dependencia de desarrollo en `pyproject.toml`, por lo que `uv sync` lo instala automáticamente sin necesidad de tenerlo instalado globalmente
