from PIL import Image, ImageDraw, ImageFont
import socket
import fcntl
import struct
import subprocess


class StatusImageBuilder:
    def __init__(self):
        self.font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 60)

    def generate(self, output):
        hostname = socket.gethostname()
        eth0_ip = get_ip_address('eth0')
        wlan0_ip = get_ip_address('wlan0')
        ssid = get_ssid()

        white = (255, 255, 255)
        font = self.font

        image = Image.new('RGBA', (1024, 768))
        draw = ImageDraw.Draw(image)

        self.labeled_field(draw, 20, 100, "hostname", hostname, white, font)
        self.labeled_field(draw, 20, 180, "eth0", eth0_ip, white, font)
        self.labeled_field(draw, 20, 260, "wlan0", wlan0_ip, white, font)
        self.labeled_field(draw, 20, 340, "ssid", ssid, white, font)

        image.save(output, "PNG")

    def labeled_field(self, draw, x, y, name, value, color, font):
        draw.text((x, y), name + ":", fill=color, font=font)
        draw.text((x + 350, y), value, fill=color, font=font)


def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode())
        )[20:24])
    except Exception:
        return "(unknown)"


def get_ssid():
    try:
        result = subprocess.run(['iwgetid', '-r'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    except Exception:
        return "(unknown)"
