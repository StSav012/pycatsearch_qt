from src.pycatsearch_qt.utils import chem_html


def test_chem_html() -> None:
    assert (c := chem_html("H2O")) == "H<sub>2</sub>O", c
    assert (c := chem_html("2H2 + O2 = 2H2O")) == "2H<sub>2</sub> + O<sub>2</sub> = 2H<sub>2</sub>O", c
    assert (c := chem_html("O-17-O, v=0")) == "<sup>17</sup>OO, v = 0", c
    assert (c := chem_html("O3, v1,3+v2")) == "O<sub>3</sub>, v<sub>1,3</sub> + v<sub>2</sub>", c
    assert (c := chem_html("gG'g'-CH3CHOHCH2OH")) == "<i>gG&#x27;g&#x27;</i>-CH<sub>3</sub>CHOHCH<sub>2</sub>OH", c
    assert (c := chem_html("gGpgp-CH3CHOHCH2OH")) == "<i>gGpgp</i>-CH<sub>3</sub>CHOHCH<sub>2</sub>OH", c
    assert (c := chem_html("gGpgp-CH3CHOHCH2OH")) == "<i>gGpgp</i>-CH<sub>3</sub>CHOHCH<sub>2</sub>OH", c
    assert (c := chem_html("(O-18)2")) == "<sup>18</sup>O<sub>2</sub>", c
    assert (c := chem_html("H2CCO-18")) == "H<sub>2</sub>CC<sup>18</sup>O", c
    assert (c := chem_html("CH3O-18-H, vt=0,1,2")) == "CH<sub>3</sub><sup>18</sup>OH, v<sub>t</sub> = 0, 1, 2", c
    assert (c := chem_html("HNO3, 2v5+v9=2")) == "HNO<sub>3</sub>, 2 v<sub>5</sub> + v<sub>9</sub> = 2", c
    assert (c := chem_html("O-18-Kv2, vt=3")) == "<sup>18</sup>OKv<sub>2</sub>, v<sub>t</sub> = 3", c
    assert (c := chem_html("AG-n-C4H9CN")) == "<i>AG</i>-<i>n</i>-C<sub>4</sub>H<sub>9</sub>CN", c
    assert (
        c := chem_html("GGag'g'-CH2(OH)CH(OH)CH2OH")
    ) == "<i>GGag&#x27;g&#x27;</i>-CH<sub>2</sub>(OH)CH(OH)CH<sub>2</sub>OH", c


if __name__ == "__main__":
    test_chem_html()
