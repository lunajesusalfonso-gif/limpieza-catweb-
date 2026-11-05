# -*- coding: utf-8 -*-
"""
Limpieza de categorías web (CatWeb).

Lee un Excel en bruto, normaliza las columnas de categoría, elimina
duplicados por SKU y exporta un CSV limpio (más un respaldo opcional).

Uso:
    python src/limpieza_catweb.py
    python src/limpieza_catweb.py --input data/input/catalogo_bruto.xlsx --output data/output/catalogo_limpio.csv
"""
import argparse
from pathlib import Path

import pandas as pd

# Raíz del proyecto: la carpeta que contiene /src
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = BASE_DIR / "data" / "input" / "catalogo_bruto.xlsx"
DEFAULT_OUTPUT = BASE_DIR / "data" / "output" / "catalogo_limpio.csv"
DEFAULT_BACKUP = BASE_DIR / "data" / "output" / "backup" / "catalogo_limpio_respaldo.csv"

# Patrón REGEXP: elimina caracteres especiales y guiones bajos
PATRON_ESPECIALES = r"[^\w\s]|_"
ACENTOS = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}


def limpiar_categoria(serie: pd.Series) -> pd.Series:
    """Quita caracteres especiales y acentos, pasa a mayúsculas y rellena nulos con 'N/A'."""
    return (
        serie.replace(PATRON_ESPECIALES, "", regex=True)
        .fillna("N/A")
        .str.upper()
        .str.replace(",", "", regex=False)
        .replace(ACENTOS, regex=True)
    )


def limpiar_catweb(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica toda la limpieza y devuelve un DataFrame nuevo (no modifica el original)."""
    limpio = df.copy()
    limpio["ZCATWEB1"] = limpiar_categoria(limpio["ZCATWEB1"])
    limpio["ZCATWEB2"] = limpio["ZCATWEB1"]
    # Se conserva solo el primer registro por SKU
    return limpio.drop_duplicates(subset=["ZSKU_WEB"], keep="first")


def preparar_tabla_sql(df: pd.DataFrame) -> pd.DataFrame:
    """Subconjunto de columnas listo para cargar a la tabla R_SKU&SUBCAT en SQL Server."""
    return df[["ZSKU_WEB", "ZCATWEB1", "ZCATWEB2"]]


def exportar_csv(df: pd.DataFrame, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, sep=",", encoding="utf-8", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Limpieza de categorías web.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Excel de entrada")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV limpio de salida")
    parser.add_argument("--backup", type=Path, default=DEFAULT_BACKUP, help="CSV de respaldo")
    parser.add_argument("--sin-respaldo", action="store_true", help="No generar respaldo")
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(
            f"No existe {args.input}. Genera datos de prueba con: python scripts/generar_dummy.py"
        )

    bruto = pd.read_excel(args.input)
    limpio = limpiar_catweb(bruto)

    exportar_csv(limpio, args.output)
    if not args.sin_respaldo:
        exportar_csv(limpio, args.backup)

    tabla_sql = preparar_tabla_sql(limpio)
    print(f"Filas entrada: {len(bruto)} | Filas salida: {len(limpio)}")
    print(f"CSV limpio: {args.output}")
    print(f"Tabla para SQL Server lista: {tabla_sql.shape[0]} filas x {tabla_sql.shape[1]} columnas")


if __name__ == "__main__":
    main()
