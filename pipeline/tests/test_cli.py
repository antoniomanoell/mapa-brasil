from indicadores.cli import main


def test_build_only_desconhecido():
    assert main(["build", "--only", "nao_existe"]) == 2
