# Limpieza de Categorías Web (CatWeb)

Pipeline en Python que limpia y normaliza las categorías web de un catálogo de productos y genera un CSV listo para cargar a una base de datos.

## Descripción

Los catálogos de productos suelen traer categorías escritas de forma inconsistente: con acentos, símbolos, mayúsculas y minúsculas mezcladas, valores vacíos y SKUs repetidos. Este proyecto toma un Excel en bruto y lo convierte en un dataset consistente.

## Objetivo

- Estandarizar el texto de las categorías para evitar que una misma categoría aparezca escrita de varias formas.
- Garantizar un único registro por SKU.
- Entregar un archivo limpio (CSV UTF-8) que se pueda cargar sin más transformaciones a una tabla relacional (por ejemplo, SQL Server).

## Qué hace

| Paso | Regla | Ejemplo |
|------|-------|---------|
| 1 | Elimina caracteres especiales y guiones bajos (regex) | `Iluminación_LED` → `Iluminación LED` sin símbolos |
| 2 | Quita acentos (Á É Í Ó Ú) | `Electrónica` → `ELECTRONICA` |
| 3 | Pasa a mayúsculas | `cables usb` → `CABLES USB` |
| 4 | Rellena valores nulos con `N/A` | `None` → `N/A` |
| 5 | Copia `ZCATWEB1` a `ZCATWEB2` | |
| 6 | Elimina duplicados, conserva el primer registro por `ZSKU_WEB` | |
| 7 | Exporta CSV y un respaldo; prepara la tabla `ZSKU_WEB, ZCATWEB1, ZCATWEB2` | |

La `Ñ` y la `Ü` se conservan, porque el mapa de acentos solo cubre las cinco vocales.

## Estructura del proyecto

```
├── src/limpieza_catweb.py      # Lógica de limpieza
├── scripts/generar_dummy.py    # Genera el Excel de prueba (datos ficticios)
├── data/input/catalogo_bruto.xlsx  # Excel dummy de entrada
├── data/output/                # CSV generados (ignorados por git)
├── tests/test_limpieza_catweb.py   # Pruebas automáticas
├── .env.example                # Plantilla de variables de entorno
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.9 o superior
- Dependencias: `pandas`, `openpyxl`, `pytest`

## Instalación

```bash
git clone <url-del-repositorio>
cd <carpeta-del-repositorio>
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

## Uso

```bash
# 1. (Opcional) regenerar el Excel dummy
python scripts/generar_dummy.py

# 2. Ejecutar la limpieza con las rutas por defecto
python src/limpieza_catweb.py

# 3. Ejecutar las pruebas
pytest
```

Con rutas propias:

```bash
python src/limpieza_catweb.py --input ruta/entrada.xlsx --output ruta/salida.csv --sin-respaldo
```

| Argumento | Descripción | Por defecto |
|-----------|-------------|-------------|
| `--input` | Excel de entrada | `data/input/catalogo_bruto.xlsx` |
| `--output` | CSV limpio | `data/output/catalogo_limpio.csv` |
| `--backup` | CSV de respaldo | `data/output/backup/catalogo_limpio_respaldo.csv` |
| `--sin-respaldo` | No genera respaldo | desactivado |

## Datos de entrada y salida

**Entrada** (Excel): columnas `ZSKU_WEB`, `ZCATWEB1`, `ZCATWEB2`.

**Salida** (CSV, UTF-8): las mismas columnas, con `ZCATWEB1` y `ZCATWEB2` normalizadas y un registro por SKU.

Los datos del repositorio son ficticios y se generan con `scripts/generar_dummy.py`.

## Pruebas

Las pruebas validan cada regla de limpieza, la eliminación de duplicados y que el DataFrame original no se modifique. El Excel dummy y las pruebas comparten la misma lista de casos, así que se mantienen sincronizados.

## Seguridad

El repositorio no incluye credenciales, hosts, rutas corporativas ni datos reales. La configuración sensible debe ir en un archivo `.env`, que git ignora; usa `.env.example` como plantilla.

## Tecnologías

Python · pandas · openpyxl · expresiones regulares · pytest
