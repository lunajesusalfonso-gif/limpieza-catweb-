# Limpieza de Categorías

Pipeline en Python que limpia y normaliza las categorías de un catálogo de productos y genera un CSV listo para cargar a una base de datos.

## Descripción

Los catálogos de productos suelen traer categorías escritas de forma inconsistente: con acentos, símbolos, mayúsculas y minúsculas mezcladas, valores vacíos y SKUs repetidos. Este proyecto toma un Excel en bruto y lo convierte en un dataset consistente.

## Objetivo

- Estandarizar el texto de las categorías para evitar que una misma categoría aparezca escrita de varias formas.
- Garantizar un único registro por SKU.
- Entregar un archivo limpio (CSV UTF-8) que se pueda cargar sin más transformaciones a una tabla relacional (por ejemplo, SQL Server).

## Qué hace

| Paso | Regla | Ejemplo |
|------|-------|---------|
| 1 | Elimina caracteres especiales y guiones bajos (regex) | `Baterías, Pilas (AA)` → `Baterías Pilas AA` |
| 2 | Quita acentos (Á É Í Ó Ú) | `Electrónica` → `ELECTRONICA` |
| 3 | Pasa a mayúsculas | `cables usb` → `CABLES USB` |
| 4 | Rellena valores nulos con `N/A` | `None` → `N/A` |
| 5 | Copia `categoria_1` a `categoria_2` | |
| 6 | Elimina duplicados, conserva el primer registro por `sku` | |
| 7 | Exporta CSV y un respaldo; prepara la tabla `sku, categoria_1, categoria_2` | |

La `Ñ` y la `Ü` se conservan, porque el mapa de acentos solo cubre las cinco vocales.

### Ejemplo antes y después

| sku | categoria_1 (entrada) | categoria_1 / categoria_2 (salida) |
|----------|--------------------|------------------------------|
| SKU00001 | `Electrónica y Audio` | `ELECTRONICA Y AUDIO` |
| SKU00004 | `Iluminación_LED` | `ILUMINACIONLED` |
| SKU00005 | `Baterías, Pilas y Cargadores` | `BATERIAS PILAS Y CARGADORES` |
| SKU00011 | *(vacío)* | `N/A` |
| SKU00001 (repetido) | `Categoría Distinta Uno` | *(se descarta, se conserva el primero)* |

## Estructura del proyecto

```
├── src/
│   └── limpieza_categorias.py        # Lógica de limpieza
├── scripts/
│   └── generar_dummy.py          # Genera el Excel de prueba (datos ficticios)
├── data/
│   ├── input/
│   │   └── catalogo_bruto.xlsx   # Excel dummy de entrada
│   └── output/                   # CSV generados (ignorados por git)
├── tests/
│   └── test_limpieza_categorias.py   # Pruebas automáticas
├── .env.example                  # Plantilla de variables de entorno
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.9 o superior
- Dependencias: `pandas`, `openpyxl`, `pytest`

## Instalación

```bash
git clone https://github.com/lunajesusalfonso-gif/limpieza-catweb-.git
cd limpieza-catweb-
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

## Uso

```bash
# 1. (Opcional) regenerar el Excel dummy
python scripts/generar_dummy.py

# 2. Ejecutar la limpieza con las rutas por defecto
python src/limpieza_categorias.py

# 3. Ejecutar las pruebas
pytest
```

Con rutas propias:

```bash
python src/limpieza_categorias.py --input ruta/entrada.xlsx --output ruta/salida.csv --sin-respaldo
```

| Argumento | Descripción | Por defecto |
|-----------|-------------|-------------|
| `--input` | Excel de entrada | `data/input/catalogo_bruto.xlsx` |
| `--output` | CSV limpio | `data/output/catalogo_limpio.csv` |
| `--backup` | CSV de respaldo | `data/output/backup/catalogo_limpio_respaldo.csv` |
| `--sin-respaldo` | No genera respaldo | desactivado |

## Datos de entrada y salida

**Entrada** (Excel): columnas `sku`, `categoria_1`, `categoria_2`.

**Salida** (CSV, UTF-8): las mismas columnas, con `categoria_1` y `categoria_2` normalizadas y un registro por SKU.

Los datos del repositorio son ficticios y se generan con `scripts/generar_dummy.py`.

## Pruebas

Las pruebas validan cada regla de limpieza, la eliminación de duplicados y que el DataFrame original no se modifique. El Excel dummy y las pruebas comparten la misma lista de casos, así que se mantienen sincronizados.

## Seguridad

El repositorio no incluye credenciales, hosts, rutas corporativas ni datos reales. La configuración sensible debe ir en un archivo `.env`, que git ignora; usa `.env.example` como plantilla.

## Tecnologías

Python · pandas · openpyxl · expresiones regulares · pytest
