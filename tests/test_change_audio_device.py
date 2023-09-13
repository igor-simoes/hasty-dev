from audio.change_audio_device import create_parser, cli

class TestChangeAudioDevice:
    cli = cli(create_parser())


def test_cli_cmd():
    self.cli
