# -*- coding: utf-8 -*-
"""
Genera un Excel de prueba (datos 100% ficticios) en data/input/BD_raiz.xlsx.

CASOS define un caso por cada regla de limpieza: (SKU, valor de entrada, resultado esperado).
Los tests importan esta lista, así el dummy y las pruebas siempre están sincronizados.
"""
import random
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SALIDA = BASE_DIR / "data" / "input" / "BD_raiz.xlsx"

# (sku, ZCATWEB1 de entrada, ZCATWEB1 esperado tras la limpieza, regla que ejercita)
CASOS = [
    ("SKU00001", "Electrónica y Audio", "ELECTRONICA Y AUDIO", "acento en minúscula + mayúsculas"),
    ("SKU00002", "ÁÉÍÓÚ áéíóú", "AEIOU AEIOU", "las 5 vocales con acento, mayúscula y minúscula"),
    ("SKU00003", "Cables & Conectores", "CABLES  CONECTORES", "símbolo &"),
    ("SKU00004", "Iluminación_LED", "ILUMINACIONLED", "guion bajo"),
    ("SKU00005", "Baterías, Pilas y Cargadores", "BATERIAS PILAS Y CARGADORES", "comas"),
    ("SKU00006", "Herramientas (Taller)", "HERRAMIENTAS TALLER", "paréntesis"),
    ("SKU00007", "Telefonía/Accesorios", "TELEFONIAACCESORIOS", "diagonal"),
    ("SKU00008", "Cámara 4K - HD #1 @ 50% off!", "CAMARA 4K  HD 1  50 OFF", "varios símbolos mezclados"),
    ("SKU00009", "cables usb", "CABLES USB", "minúsculas a mayúsculas"),
    ("SKU00010", "AUDIO", "AUDIO", "ya limpio, no cambia"),
    ("SKU00011", None, "N/A", "nulo a N/A"),
    ("SKU00012", "N/A", "NA", "literal 'N/A': la diagonal se elimina antes del fillna"),
    ("SKU00013", "Diseño y Piñatería", "DISEÑO Y PIÑATERIA", "la Ñ se conserva"),
    ("SKU00014", "Ünico Pingüino", "ÜNICO PINGÜINO", "la diéresis (Ü) no está en el mapa y se conserva"),
]

# SKUs repetidos con otra categoría: debe quedarse la primera aparición.
DUPLICADOS = [
    ("SKU00001", "Categoría Distinta Uno"),
    ("SKU00011", "Categoría Distinta Dos"),
    ("SKU00003", None),
]

CATEGORIAS_RELLENO = [
    "Cámaras de Seguridad", "Computación y Periféricos", "Energía Solar",
    "Automatización del Hogar", "Pilas_AA", "Cargadores (USB-C)", None,
]


def generar(n_relleno: int = 26, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    filas = [{"ZSKU_WEB": s, "ZCATWEB1": c, "ZCATWEB2": None} for s, c, _, _ in CASOS]
    inicio = len(CASOS) + 1
    filas += [
        {"ZSKU_WEB": f"SKU{i:05d}", "ZCATWEB1": random.choice(CATEGORIAS_RELLENO), "ZCATWEB2": None}
        for i in range(inicio, inicio + n_relleno)
    ]
    # Duplicados al final para que "keep first" conserve los casos originales
    filas += [{"ZSKU_WEB": s, "ZCATWEB1": c, "ZCATWEB2": None} for s, c in DUPLICADOS]
    return pd.DataFrame(filas)


if __name__ == "__main__":
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df = generar()
    df.to_excel(SALIDA, index=False)
    print(f"Excel dummy generado: {SALIDA} ({len(df)} filas)")
