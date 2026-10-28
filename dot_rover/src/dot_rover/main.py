"""Discover nearby Bluetooth Classic (BR/EDR) devices using btpy."""

from argparse import ArgumentParser

from btpy import ClassicDevice


def discover(duration: int = 8) -> list[ClassicDevice]:
    """Run an inquiry scan for `duration` seconds and return unique devices."""
    devices = ClassicDevice.scan(duration=duration)

    # Devices can answer an inquiry several times; keep one entry per address.
    unique: dict[str, ClassicDevice] = {}
    for device in devices:
        if device.address not in unique or (device.name and not unique[device.address].name):
            unique[device.address] = device
    return list(unique.values())


def main() -> None:
    parser = ArgumentParser(description="Discover Bluetooth Classic devices")
    parser.add_argument("-d", "--duration", type=int, default=8, help="scan duration in seconds")
    args = parser.parse_args()

    print(f"Scanning for Bluetooth Classic devices for {args.duration}s...")
    try:
        devices = discover(args.duration)
    except Exception as e:
        print(f"Scan failed: {e}")
        return

    if not devices:
        print("No devices found.")
        return

    print(f"Found {len(devices)} device(s):")
    for device in devices:
        print(f"  {device.address}  {device.name or '<unknown>'}")


if __name__ == "__main__":
    main()
