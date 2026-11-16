#!/usr/bin/env python3
"""Draw the block diagrams in diagrams/ as plain SVG files.

    python3 tools/diagrams.py

Standard library only. Each diagram is laid out by hand on a grid: edit the
coordinates below and run this again. Every link drawn is listed in
parts.md; a dashed line is an inferred one.
"""
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "diagrams")

KINDS = {                      # fill, outline, title, subtitle
    "cpu": ("#EEEDFE", "#534AB7", "#26215C", "#3C3489"),
    "part": ("#F1EFE8", "#5F5E5A", "#2C2C2A", "#444441"),
    "todo": ("#FFFFFF", "#888780", "#444441", "#5F5E5A"),
}
LINE = "#5F5E5A"
TEXT = "#444441"
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


class Diagram:
    def __init__(self, width, height, title, desc):
        self.w, self.h = width, height
        self.items = [
            "<title>%s</title><desc>%s</desc>" % (escape(title), escape(desc)),
            '<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
            'stroke="%s" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
            "</marker></defs>" % LINE,
            '<rect x="0.5" y="0.5" width="%d" height="%d" rx="8" fill="#FFFFFF" stroke="#D3D1C7"/>'
            % (width - 1, height - 1),
        ]

    def text(self, x, y, s, size=12, anchor="middle", colour=TEXT, weight=400):
        self.items.append(
            '<text x="%s" y="%s" font-size="%d" font-weight="%d" text-anchor="%s" '
            'dominant-baseline="central" fill="%s">%s</text>' % (x, y, size, weight, anchor, colour, escape(s)))

    def box(self, x, y, w, h, title, *subs, kind="part"):
        fill, edge, head, sub = KINDS[kind]
        dash = ' stroke-dasharray="5 4"' if kind == "todo" else ""
        self.items.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s"%s/>'
                          % (x, y, w, h, fill, edge, dash))
        subs = [t for t in subs if t]
        lines = 1 + len(subs)
        top = y + h / 2 - (lines - 1) * 9
        self.text(x + w / 2, top, title, 14, colour=head, weight=600)
        for i, s in enumerate(subs, 1):
            self.text(x + w / 2, top + 18 * i, s, 12, colour=sub)

    def link(self, x1, y1, x2, y2, both=True, dashed=False, start=False):
        ends = ' marker-end="url(#a)"' + (' marker-start="url(#a)"' if both or start else "")
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.items.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"%s%s/>'
                          % (x1, y1, x2, y2, LINE, dash, ends))

    def plain(self, x1, y1, x2, y2, dashed=True):
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.items.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"%s/>'
                          % (x1, y1, x2, y2, LINE, dash))

    def frame(self, x, y, w, h, label):
        self.items.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="#FAFAF7" '
                          'stroke="#B4B2A9"/>' % (x, y, w, h))
        self.text(x + w / 2, y + 20, label, 14, colour="#2C2C2A", weight=600)

    def legend(self, y, entries):
        x = 40
        for kind, label in entries:
            if kind == "dash":
                self.plain(x, y + 6, x + 22, y + 6)
                x += 30
            else:
                fill, edge, _, _ = KINDS[kind]
                dash = ' stroke-dasharray="3 2"' if kind == "todo" else ""
                self.items.append('<rect x="%d" y="%d" width="12" height="12" rx="2" fill="%s" stroke="%s"%s/>'
                                  % (x, y, fill, edge, dash))
                x += 18
            self.text(x, y + 6, label, 12, anchor="start")
            x += len(label) * 6.4 + 22

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
                    'font-family="%s" role="img">\n' % (self.w, self.h, self.w, self.h, FONT))
            f.write("\n".join(self.items))
            f.write("\n</svg>\n")
        print(os.path.relpath(path, ROOT))


def overview():
    d = Diagram(680, 506, "OP-XY hardware overview",
                "Two ADSP-BF703 processors, master and slave, linked by an SPI bridge and a TDM audio "
                "link. The master connects to the display, the SPI flash, the nRF52840, the PSoC and "
                "USB. The slave connects to the e-MMC and the audio and CV chips.")
    d.box(200, 40, 130, 56, "ST7796", "LCD, 222 × 480 visible")
    d.box(350, 40, 130, 56, "SPI flash", "8 Mbit, program code")
    d.box(500, 40, 130, 56, "Kioxia e-MMC", "16 GB")
    d.link(300, 148, 300, 99, both=False)
    d.text(292, 124, "8080, 8-bit", anchor="end")
    d.link(385, 99, 385, 147)
    d.text(393, 124, "SPI2", anchor="start")
    d.link(565, 99, 565, 147)
    d.text(573, 124, "MSI0", anchor="start")

    d.box(40, 150, 150, 56, "nRF52840", "Bluetooth LE", kind="cpu")
    d.box(40, 274, 150, 56, "PSoC 4200L", "Backplane MCU", kind="cpu")
    d.box(265, 150, 150, 180, "ADSP-BF703", "Master", "2 Gbit DDR2", kind="cpu")
    d.box(490, 150, 150, 180, "ADSP-BF703", "Slave", "2 Gbit DDR2", kind="cpu")
    d.link(193, 178, 262, 178)
    d.text(227, 166, "UART1")
    d.link(193, 302, 262, 302)
    d.text(227, 290, "UART0")
    d.link(418, 200, 487, 200)
    d.text(452, 188, "SPI bridge")
    d.link(418, 280, 487, 280)
    d.text(452, 268, "TDM audio")

    d.box(40, 384, 150, 56, "Backplane parts", "Keys, LEDs, power")
    d.box(265, 384, 150, 56, "USB-C port", "FUSB302 for PD")
    d.box(490, 384, 150, 56, "Audio and CV", "Codec, amplifier, DACs")
    d.link(100, 333, 100, 381)
    d.items.append('<path d="M170 333 L170 357 L300 357 L300 381" fill="none" stroke="%s" '
                   'stroke-width="1.5" marker-end="url(#a)"/>' % LINE)
    d.text(235, 347, "CC, PD")
    d.link(370, 333, 370, 381)
    d.text(378, 362, "USB HS", anchor="start")
    d.link(565, 333, 565, 381)
    d.text(573, 362, "I2C, TDM", anchor="start")
    d.legend(472, [("cpu", "Processor or MCU"), ("part", "Peripheral or memory")])
    d.save("overview.svg")


def boards():
    d = Diagram(680, 470, "OP-XY boards",
                "Which chips sit on each of the three boards: the DSP board, the backplane and the "
                "keyboard board.")
    d.frame(30, 30, 300, 410, "DSP board  ·  175-00139 rev 5.0")
    d.frame(350, 30, 300, 266, "Backplane  ·  175-00140 rev 3.0")
    d.frame(350, 316, 300, 124, "Keyboard board  ·  175-00142")

    def stack(x, y, w, rows):
        for title, sub, kind in rows:
            d.box(x, y, w, 40, title, sub, kind=kind)
            y += 48

    stack(44, 64, 132, [("ADSP-BF703", "Processor", "cpu"), ("IS43DR16128C", "DDR2, 2 Gbit", "part"),
                        ("CS47L35", "Audio codec", "part"), ("CS43131", "Headphone DAC", "part"),
                        ("AS3709", "Power management", "part"), ("25 and 24 MHz", "Crystals", "part"),
                        ("Marked I6DEB3", "SPI flash?", "todo")])
    stack(184, 64, 132, [("ADSP-BF703", "Processor", "cpu"), ("IS43DR16128C", "DDR2, 2 Gbit", "part"),
                         ("Kioxia e-MMC", "16 GB", "part"), ("TPS65132T6", "Split-rail supply", "part"),
                         ("LTV-354T?", "Optocoupler", "part"), ("TI, marked P145A", "Not identified", "todo")])
    stack(364, 64, 132, [("PSoC 4200L", "CY8C4247BZI-L479", "cpu"), ("MAX77818", "Charger, fuel gauge", "part"),
                         ("MAX98390C", "Speaker amplifier", "part"), ("Four encoders", "", "part")])
    stack(504, 64, 132, [("nRF52840", "Bluetooth LE", "cpu"), ("SKY66404-11", "2.4 GHz front end", "part"),
                         ("32 MHz", "Crystal", "part"), ("Four chips", "Not identified", "todo")])
    d.box(364, 350, 132, 40, "Keys", "")
    d.box(504, 350, 132, 40, "Marked Z41KJ ×2", "Not identified", kind="todo")
    d.box(364, 396, 272, 32, "Display: not yet photographed", kind="todo")
    d.save("boards.svg")


def backplane():
    d = Diagram(680, 514, "OP-XY PSoC and radio",
                "The PSoC with its peripherals: the MAX77818 charger, the AS3709 PMIC, the FUSB302 and "
                "a key LED driver on I2C, the LSM6DSO and the TW11 key scanner on SPI, the keys and "
                "knobs, and the master processor on UART0. Below, the master's UART1 to the nRF52840 "
                "with its front end and antennas.")
    d.box(40, 40, 135, 56, "MAX77818", "Charger, fuel gauge")
    d.box(195, 40, 135, 56, "AS3709", "PMIC, on the DSP board")
    d.box(350, 40, 135, 56, "FUSB302", "USB-C PD")
    d.box(505, 40, 135, 56, "Key LED driver", "Not identified", kind="todo")
    d.link(107, 99, 107, 167)
    d.text(115, 126, "I2C 0x36,", anchor="start")
    d.text(115, 142, "0x66, 0x69", anchor="start")
    d.link(262, 99, 262, 167, dashed=True)
    d.text(270, 126, "I2C 0x40", anchor="start")
    d.text(270, 142, "(inferred)", anchor="start")
    d.link(417, 99, 417, 167)
    d.text(425, 133, "I2C", anchor="start")
    d.link(572, 99, 572, 167)
    d.text(580, 133, "I2C 0x34", anchor="start")

    d.box(40, 170, 600, 56, "PSoC 4200L backplane MCU", "CY8C4247BZI-L479, Cortex-M0", kind="cpu")
    d.link(107, 229, 107, 297)
    d.text(115, 263, "SPI", anchor="start")
    d.link(262, 229, 262, 297)
    d.text(270, 263, "SPI", anchor="start")
    d.link(417, 229, 417, 297)
    d.text(425, 263, "GPIO, ADC", anchor="start")
    d.link(572, 229, 572, 297)
    d.text(580, 263, "UART0", anchor="start")

    d.box(40, 300, 135, 56, "LSM6DSO", "6-axis IMU")
    d.box(195, 300, 135, 56, "TW11", "Hall key scanner")
    d.box(350, 300, 135, 56, "Keys, knobs", "Encoders, pots")
    d.box(505, 300, 135, 56, "ADSP-BF703", "Master", kind="cpu")
    d.link(572, 359, 572, 407)
    d.text(564, 383, "UART1, RTS/CTS", anchor="end")

    d.box(40, 410, 135, 56, "Two antennas", "One is 'to ble clip'")
    d.box(273, 410, 135, 56, "SKY66404-11", "2.4 GHz front end")
    d.box(505, 410, 135, 56, "nRF52840", "Bluetooth LE", kind="cpu")
    d.link(502, 438, 411, 438)
    d.link(270, 438, 178, 438, both=False)
    d.legend(484, [("cpu", "Processor or MCU"), ("part", "Peripheral"), ("todo", "Not identified"),
                   ("dash", "Inferred")])
    d.save("backplane.svg")


def audio():
    d = Diagram(680, 404, "OP-XY audio and CV",
                "The slave processor with the CS47L35 codec, the MAX98390C speaker amplifier and the "
                "CS43131 headphone DAC above it, and the CV output DAC, its TPS65132T6 supply and the "
                "TRS MIDI and sync jacks below.")
    d.box(40, 40, 180, 56, "CS47L35", "Audio codec")
    d.box(250, 40, 180, 56, "MAX98390C", "Speaker amp, on the backplane")
    d.box(460, 40, 180, 56, "CS43131", "Headphone DAC")
    d.link(130, 99, 130, 167)
    d.text(138, 133, "I2C 0x1a, TDM", anchor="start")
    d.link(340, 99, 340, 167)
    d.text(348, 133, "I2C 0x38", anchor="start")
    d.link(550, 99, 550, 167)
    d.text(558, 133, "I2C 0x33", anchor="start")

    d.box(40, 170, 600, 56, "ADSP-BF703 slave", "TWI0, SPORT0, UART0, MSI0", kind="cpu")
    d.link(130, 229, 130, 297)
    d.text(138, 263, "I2C 0x48", anchor="start")
    d.link(340, 229, 340, 297)
    d.text(348, 263, "I2C 0x3e", anchor="start")
    d.link(550, 229, 550, 297)
    d.text(558, 263, "UART0, timer", anchor="start")

    d.box(40, 300, 180, 56, "CV output DAC", "14-bit, not identified", kind="todo")
    d.box(250, 300, 180, 56, "TPS65132T6", "CV supply, split rail")
    d.box(460, 300, 180, 56, "TRS MIDI and sync", "31,250 baud")
    d.legend(374, [("cpu", "Processor"), ("part", "Identified part"), ("todo", "Not identified")])
    d.save("audio.svg")


if __name__ == "__main__":
    overview()
    boards()
    backplane()
    audio()
