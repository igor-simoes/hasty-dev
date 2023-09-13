import os
import re
from argparse import ArgumentParser
from subprocess import call, check_output

""" DISCLAIMER
Actually, this script uses 'pactl' and 'pacmd' to get/set PCI or USB devices.
Bluetooth phones works as well.

Note: Headphones that uses P3 connection can't found it by name.
"""

help_msg = (
    "help - display this message\n"
    "show - display audio device info\n"
    "set <device_pattern> - set output audio to a specific device. Default: Speaker"
)

app_desc = "Script to change audio output device."


def get_devices() -> list:
    return (
        check_output(["pactl", "list", "sinks", "short"]).decode("utf-8").splitlines()
    )


def show_devices():
    devices = get_devices()
    print("ID", "Name", "Status")
    for device in devices:
        device_info = device.split("\t")
        print(device_info[0], device_info[1], device_info[4])


def set_device(device_pattern: str = "Speaker") -> None:
    """
    Set device by device pattern name
    """

    if device_pattern == "Speaker":
        pattern = "hw_sofhdadsp__sink"
    else:
        pattern = device_pattern

    regex = re.compile(pattern, re.IGNORECASE)
    devices = get_devices()
    for device in devices:
        identifier, device_name, *_ = device.split("\t")
        if regex.findall(device_name):
            call(["pacmd", "set-default-sink", identifier])
    os.system(f'notify-send "Changed Audio Output" "Using {device_pattern} device"')


def create_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "cmd",
        nargs="*",
        help=f"{app_desc}. Available Commands [help, show, set]",
    )
    return parser

def cli(parser):
    arg = parser.parse_args()
    try:
        if arg.cmd[0] == "help":
            print(f"{app_desc}\n\n{help_msg}")
        elif arg.cmd[0] == "show":
            show_devices()
        elif arg.cmd[0] == "set":
            if len(arg.cmd) > 1:
                device_pattern = arg.cmd[1]
                set_device(device_pattern)
            else:
                set_device()
    except IndexError:
        print("Error: Invalid command. Supported commands:\n" f"{help_msg}")
    except Exception as err:
        print(err)


if __name__ == "__main__":
    cli(create_parser())
