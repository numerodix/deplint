from deplint.ui.writer import UiWriter


def test_writer(capsys):
    # Standard mode
    ui = UiWriter()

    ui.inform('it is late')
    stdout, stderr = capsys.readouterr()
    assert stdout == ''
    assert stderr == ''

    ui.output('it is early')
    stdout, stderr = capsys.readouterr()
    assert stdout == 'it is early\n'
    assert stderr == ''


    # Verbose mode
    ui = UiWriter(verbose=True)

    ui.inform('it is late')
    stdout, stderr = capsys.readouterr()
    assert stdout == ''
    assert stderr == 'it is late\n'

    ui.output('it is early')
    stdout, stderr = capsys.readouterr()
    assert stdout == 'it is early\n'
    assert stderr == ''
