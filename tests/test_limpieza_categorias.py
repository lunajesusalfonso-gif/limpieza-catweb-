import re
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "scripts"))
from limpieza_categorias import limpiar_categorias  # noqa: E402
from generar_dummy import CASOS, DUPLICADOS, generar  # noqa: E402


@pytest.fixture(scope="module")
def limpio():
    return limpiar_categorias(generar())


@pytest.mark.parametrize("sku,entrada,esperado,regla", CASOS, ids=[c[3] for c in CASOS])
def test_cada_regla(limpio, sku, entrada, esperado, regla):
    assert limpio.loc[limpio.sku == sku, "categoria_1"].iloc[0] == esperado


def test_duplicados_conservan_el_primero(limpio):
    assert limpio.sku.is_unique
    esperado = {s: e for s, _, e, _ in CASOS}
    for sku, _ in DUPLICADOS:
        assert limpio.loc[limpio.sku == sku, "categoria_1"].iloc[0] == esperado[sku]


def test_categoria_2_igual_categoria_1(limpio):
    assert (limpio.categoria_1 == limpio.categoria_2).all()


def test_sin_nulos_ni_especiales_ni_acentos(limpio):
    assert limpio.categoria_1.notna().all()
    for valor in limpio.categoria_1:
        if valor == "N/A":
            continue
        assert not re.search(r"[ÁÉÍÓÚ_,&()/#@%!-]", valor), valor


def test_no_modifica_el_original():
    df = generar()
    copia = df.copy()
    limpiar_categorias(df)
    pd.testing.assert_frame_equal(df, copia)
