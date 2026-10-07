import html

from src.pycatsearch_qt.utils import chem_html


def test_chem_html() -> None:
    assert (c := html.unescape(chem_html("H2O"))) == "H<sub>2</sub>O", c
    assert (c := html.unescape(chem_html("O-17-O, v=0"))) == "O-17-O, v = 0", c
    assert (c := html.unescape(chem_html("gG'g'-CH3CHOHCH2OH"))) == "<i>gG'g'</i>-CH<sub>3</sub>CHOHCH<sub>2</sub>OH", c
    assert (c := html.unescape(chem_html("gGpgp-CH3CHOHCH2OH"))) == "<i>gGpgp</i>-CH<sub>3</sub>CHOHCH<sub>2</sub>OH", c
    assert (c := html.unescape(chem_html("gGpgp-CH3CHOHCH2OH"))) == "<i>gGpgp</i>-CH<sub>3</sub>CHOHCH<sub>2</sub>OH", c
    assert (c := html.unescape(chem_html("(O-18)2"))) == "(O-18)<sub>2</sub>", c
    assert (c := html.unescape(chem_html("H2CCO-18"))) == "H<sub>2</sub>CCO-18", c
    assert (c := html.unescape(chem_html("CH3O-18-H, vt=0,1,2"))) == "CH<sub>3</sub>O-18-H, v<sub>t</sub> = 0, 1, 2", c
    assert (
        c := html.unescape(chem_html("HNO3, 2v5+v9=2"))
    ) == "HNO<sub>3</sub>, 2 v<sub>5</sub> + v<sub>9</sub> = 2", c
    assert (c := html.unescape(chem_html("O-18-Kv2, vt=3"))) == "O-18-Kv<sub>2</sub>, v<sub>t</sub> = 3", c


if __name__ == "__main__":
    test_chem_html()
