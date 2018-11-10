# pideck

Raspberry Pi based playback deck with a webinterface.

## ATEM Compatibility

ATEM HDMI inputs will not convert framerates or scale video, so HDMI settings must be configured to match exactly. However, fractional framerate differences appear to be tolerated. For example, with an ATEM switcher configured for 1080p, 29.97 framerate, the following settings work in `config.txt`:

```
hdmi_group=1              # CEA, typical for TVs
hdmi_mode=34              # 1080p, 30 Hz
hdmi_pixel_encoding=3     # YCbCr limited (16-235)
disable_overscan=1
```

More information is available on the [Raspberry Pi video options page](https://www.raspberrypi.org/documentation/configuration/config-txt/video.md).
