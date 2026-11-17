# Parts

**Confidence** says where each identification comes from:

- **marking**: read off the chip's package. *(published)* means the marking is legible in a photo in
  [photos/](photos/). *(close-up)* means it was read from a close-up that is not published, because the
  frame also shows a serial label.
- **ID read**: an identification register read back from the chip on a working unit.
- **firmware**: known from how the device's firmware drives the hardware: which bus and address it
  uses for a chip, or a part name it prints. No firmware code or data is reproduced here.
- **inferred**: deduced from what the chip has to do, or from its package and position. Not yet seen on
  the package.
- **unknown**: the function is known, the part is not.

**Board** names the PCB by its silkscreen: **DSP**, **backplane** or **keyboard** (see [boards/](boards/)).
`?` means no photo shows the chip yet.

## Identified

| Role | Part | Confidence | Board | Connection | Datasheet |
|---|---|---|---|---|---|
| Main processors (×2, "master" and "slave") | Analog Devices **ADSP-BF703KBCZ-4** (Blackfin+, 400 MHz grade, 184-ball BGA) | marking *(published)*: `ADSP-BF703 / KBCZ-4 / #2448 KOREA` on both | DSP | One is strapped as master | [ADSP-BF703 product page](https://www.analog.com/en/products/adsp-bf703.html) (data sheet, hardware reference, programming reference, anomaly list) |
| DDR2 SDRAM (×2, one beside each processor) | ISSI **IS43DR16128C-25DBL** (2 Gbit, ×16, DDR2-800, 84-ball BGA) | marking *(published)*: `ISSI 2442 / IS43DR16128C / -25DBL` on both | DSP | DMC of each ADSP-BF703 | [ISSI DDR2 page](https://www.issi.com/US/product-dram-ddr2.shtml) |
| Storage, 16 GB | Kioxia **THGAMVG7T13BAIL** (e-MMC 5.1, 153-ball BGA) | marking: faint in the published photo, clear in a close-up | DSP | Slave MSI0, 8-bit | [Kioxia e-MMC page](https://americas.kioxia.com/en-us/business/memory/mlc-nand/emmc.html) |
| Audio codec | Cirrus Logic **CS47L35** (smart codec with integrated DSP) | marking *(close-up)*: `CS47L35 / NRA1CH2429 / TW`. Faint in the published photo | DSP | Slave SPORT0 (TDM), slave I2C `0x1a` | [CS47L35 product page](https://www.cirrus.com/products/cs47l35/) |
| Headphone DAC | Cirrus Logic **CS43131** (DAC with headphone amplifier) | marking *(close-up)*: `CS43131 / A1BX2134`. Faint in the published photo | DSP | Slave I2C `0x33` | [CS43131 product page](https://www.cirrus.com/products/cs43131/) |
| Speaker amplifier | Analog Devices (Maxim) **MAX98390C** (boosted class-D with speaker sensing), EWX package | marking *(close-up)*: `+MAX / 98390C / EWX / K 2429` | backplane, by the speaker connector | Slave I2C `0x38` | [MAX98390 product page](https://www.analog.com/en/products/max98390.html) |
| Split-rail supply (one positive and one negative output) | Texas Instruments **TPS65132T6** (±5.6 V by default, 15-ball WCSP) | marking *(close-up)*: `TPS / 65132T6` | DSP | Slave I2C `0x3e`, which is this part's address in its datasheet. It supplies the CV outputs | [TPS65132 product page](https://www.ti.com/product/TPS65132) |
| Power management on the DSP board | ams **AS3709** (five DC/DC converters and two LDOs, 32-pin QFN) | marking *(close-up)*: `ams / AS3709 / K2V0-10 / DEBA` | DSP, beside its inductors | Probably the PMIC the PSoC drives at I2C `0x40` (inferred: it is the only PMIC in the photos) | ams OSRAM datasheet DS000292. No manufacturer product page found; distributors host copies |
| Battery charger and fuel gauge | Analog Devices (Maxim) **MAX77818** (EWZ package) | marking *(close-up)*: `MAX77818 / EWZ / KVED 227` | backplane | PSoC I2C `0x36`, `0x66` and `0x69`. Not on a Blackfin bus | [MAX77818 product page](https://www.analog.com/en/products/max77818.html) |
| Key, LED and power coprocessor | Infineon (Cypress) **CY8C4247BZI-L479** (PSoC 4200L, Cortex-M0, 128 KB flash, 124-ball VFBGA) | marking *(close-up)*: `CY8C4247BZI- / L479 TWN2249 / CYP 633964`. It also takes the PSoC UART bootloader protocol (application note AN68272) | backplane | Master UART0, 1 Mbaud | [CY8C4247BZI-L479 part page](https://www.infineon.com/part/CY8C4247BZI-L479) (PSoC 4200L family datasheet) |
| Bluetooth LE | Nordic Semiconductor **nRF52840** (CKAA package, a WLCSP) | marking *(close-up)*: `N52840 / CKAAD0 / 2241KU`. Takes Nordic DFU updates | backplane | Master UART1, 1 Mbaud, RTS/CTS | [nRF52840 product page](https://www.nordicsemi.com/Products/nRF52840) |
| 2.4 GHz front end for the nRF52840 | Skyworks **SKY66404-11** (PA, LNA and antenna switch in a 22-pad module) | marking *(close-up)*: Skyworks logo and `66404` | backplane, between the nRF52840 and the antenna connector | Two antenna outputs. One is silkscreened `to ble clip`; the other label is partly covered by its cable | [SKY66404-11 product page](https://www.skyworksinc.com/Products/Front-end-Modules/SKY66404-11) |
| Optocoupler, probably the MIDI input isolation | 4-pin SOP, probably Lite-On **LTV-354T** | marking *(close-up)*: a logo, then `N48 / 354T / WC`. The part is inferred from `354T`, and the role from the package | DSP, back | Not traced | — |
| Program flash, 1 MiB | ISSI **IS25WP080D** (8 Mbit, 1.8 V SPI NOR) | ID read `9d 70 14` (JEDEC ID), which is the IS25WP080D's in the ISSI datasheet: `9d` is ISSI, `70` the memory type and `14` the capacity. Marking *(close-up)*: `I6DEB3 / P1L944`, on an 8-pad leadless package | DSP, between the two processors | Master SPI2; the boot ROM boots from it | [ISSI serial flash page](https://www.issi.com/US/product-flash.shtml) |
| Display controller | Sitronix **ST7796** family (ST7796S command set) | ID read: RDID4 `00 77 96` | ? | 8080 8-bit parallel to the master; 320×480 controller, 222×480 visible | [Sitronix](https://www.sitronix.com.tw/en/) (no public product page; the ST7796S datasheet is widely mirrored) |
| RTC | On-chip RTC of the ADSP-BF703 | n/a (on-chip) | — | — | see ADSP-BF703 |
| USB | On-chip USB 2.0 OTG controller and PHY of the master ADSP-BF703 | n/a (on-chip) | — | — | see ADSP-BF703 |

## Named by the firmware, not yet found in a photo

| Role | Part | Confidence | Connection |
|---|---|---|---|
| USB-C configuration channel and Power Delivery | onsemi **FUSB302** | firmware | PSoC I2C |
| Accelerometer and gyroscope | STMicroelectronics **LSM6DSO** | firmware | PSoC SPI |
| Hall-sensor key scanner | **TW11** (no manufacturer part number known) | firmware | PSoC SPI |
| Key LED driver | not identified | firmware | PSoC I2C `0x34` |
| CV output DAC | not identified, 14-bit | firmware | Slave I2C `0x48` |

Some of the unidentified chips in the next table may be these parts.

## Links between the processors

| Link | Master end | Slave end | Notes |
|---|---|---|---|
| SPI bridge | SPI0 | SPI2 | Carries the slave's boot image, storage requests and messages between the two processors |
| Audio | SPORT1 | SPORT0 | TDM. The CS47L35 supplies the clocks |
| TRS MIDI and sync | — | UART0 at 31,250 baud, and a timer | |

All three are known from the firmware.

## Marking read, part not identified

These markings are legible in a close-up but have not been matched to a part number.

| Board | Package | Marking | Notes |
|---|---|---|---|
| DSP, by the e-MMC | 10-pin VSSOP, Texas Instruments | `TI 34 / P145A / 751Z` | Next to the TPS65132T6 |
| DSP | SOT-23, 5 or 6 pins | `1CUV` | |
| DSP, both sides | 6-pad leadless, several | `X5` | |
| DSP, back | SOT-23 | `5B` | By the optocoupler |
| keyboard (×2) | 32-pin QFN | `Z41KJ / 3729` | Visible through the two cut-outs in the cover sheet |
| backplane, by the MAX77818 | small chip-scale package | `TYAA / CUD` | |
| backplane, by the MAX77818 | leadless, a few millimetres long | `X20PPD / 307H0725` (reading uncertain) | |
| backplane | small leadless package | `S0`, a data-matrix code, `240` | |
| backplane, by a 10 µH inductor | 8-pin leadless | `D60 / A60 / E25` | A small switching converter, going by the inductor |

## Known function, part unknown

| Role | What is known | Connection | Reference |
|---|---|---|---|
| Display panel module | TFT on the ST7796; maker and size not yet read from the module | — | — |
| Battery | Li-ion, 3.7 V, 4900 mAh, 18 Wh, 85 g, by its label ([photos/main-boards.jpg](photos/main-boards.jpg)) | Backplane | — |

## Clocks

| Signal | Value | Status |
|---|---|---|
| CLKIN (both ADSP-BF703s) | 25 MHz | A crystal marked `25.0 AD3C` sits beside the processors on the DSP board, and the derived clocks below check out on a unit. How one crystal reaches both processors is not traced |
| CCLK / SYSCLK / DCLK | 400 / 200 / 200 MHz | Configured and checked on a unit |
| USB_CLKIN | probably 24 MHz | A second crystal marked `24.0 AG39` sits next to the 25 MHz one. Not traced to the pin |
| nRF52840 | 32 MHz | A crystal marked `3200T` sits beside it on the backplane, with a smaller one marked `A148L` (probably 32.768 kHz) |

## Open questions

The photos settled the processors, the DDR2, the codec, the headphone DAC, the speaker amplifier, the
charger, the PSoC, the Nordic part and its front end, and which board each of them is on.

Still open:

1. The CV output DAC, and whether the TI part marked `P145A` is it.
2. The parts in the "marking read" table above, most of all the two `Z41KJ` chips on the keyboard.
3. The key LED driver at I2C `0x34`, and where the FUSB302, LSM6DSO and TW11 sit.
4. The display module and its flex marking.
5. The underside of the backplane and the key side of the keyboard, which no photo shows yet.
