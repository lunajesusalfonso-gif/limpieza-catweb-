import re
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "scripts"))
from limpieza_catweb import limpiar_catweb  # noqa: E402
from generar_dummy import CASOS, DUPLICADOS, generar  # noqa: E402


@pytest.fixture(scope="module")
def limpio():
    return limpiar_catweb(generar())


@pytest.mark.parametrize("sku,entrada,esperado,regla", CASOS, ids=[c[3] for c in CASOS])
def test_cada_regla(limpio, sku, entrada, esperado, regla):
    assert limpio.loc[limpio.ZSKU_WEB == sku, "ZCATWEB1"].iloc[0] == esperado


def test_duplicados_conservan_el_primero(limpio):
    assert limpio.ZSKU_WEB.is_unique
    esperado = {s: e for s, _, e, _ in CASOS}
    for sku, _ in DUPLICADOS:
        assert limpio.loc[limpio.ZSKU_WEB == sku, "ZCATWEB1"].iloc[0] == esperado[sku]


def test_catweb2_igual_catweb1(limpio):
    assert (limpio.ZCATWEB1 == limpio.ZCATWEB2).all()


def test_sin_nulos_ni_especiales_ni_acentos(limpio):
    assert limpio.ZCATWEB1.notna().all()
    for valor in limpio.ZCATWEB1:
        if valor == "N/A":
            continue
        assert not re.search(r"[ÁÉÍÓÚ_,&()/#@%!-]", valor), valor


def test_no_modifica_el_original():
    df = generar()
    copia = df.copy()
    limpiar_catweb(df)
    pd.testing.assert_frame_equal(df, copia)
