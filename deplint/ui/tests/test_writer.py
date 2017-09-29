from deplint.ui.writer import UiWriter


def test_writer(capsys):
    # Standard mode
    ui = UiWriter()

    ui.output('it is early')
    assert capsys.readouterr()[0] == 'it is early\n'

    ui.inform('it is late')
    assert capsys.readouterr()[0] == ''


    # Verbose mode
    ui = UiWriter(verbose=True)

    ui.output('it is early')
    assert capsys.readouterr()[0] == 'it is early\n'

    ui.inform('it is late')
    assert capsys.readouterr()[0] == 'it is late\n'
