# Photos

All photos sit in this one folder. Each board photo has an annotated copy beside it, with the chips
numbered and a legend underneath.

| Photo | Shows | Annotated copy |
|---|---|---|
| [front.jpg](front.jpg) | The unit from the front | — |
| [rear-covered.jpg](rear-covered.jpg) | The rear, cover on | — |
| [rear-uncovered.jpg](rear-uncovered.jpg) | The rear with the cover off: the rear plate | — |
| [main-boards.jpg](main-boards.jpg) | The rear plate off: backplane, DSP board, battery, speaker | [main-boards-annotated.jpg](main-boards-annotated.jpg) |
| [cpu-pcb-front.jpg](cpu-pcb-front.jpg) | DSP board, component side | [cpu-pcb-front-annotated.jpg](cpu-pcb-front-annotated.jpg) |
| [cpu-pcb-back.jpg](cpu-pcb-back.jpg) | DSP board, back | [cpu-pcb-back-annotated.jpg](cpu-pcb-back-annotated.jpg) |
| [keys-back.jpg](keys-back.jpg) | Keyboard board, back | [keys-back-annotated.jpg](keys-back-annotated.jpg) |

The first three show no chips, so they have no annotated copy.

## Annotated copies

The labels live in [labels.json](labels.json): one box per chip, in pixels of the original photo. After
changing a label or adding a photo, redraw the copies:

```bash
python3 tools/annotate.py
```

The script needs Pillow and never changes the originals. A yellow box is an identified part. An orange
box is a chip whose marking is read but whose part number is not known yet.

## Naming

- `<board>-<view>.jpg` for a whole board, square-on and evenly lit, such as `cpu-pcb-front.jpg`.
- `<board>-<part>.jpg` for a close-up of one chip's marking, such as `backplane-psoc.jpg`.
- `<name>-annotated.jpg` is generated. Do not edit it by hand.

## Before adding a photo

- **Cover serial labels.** The white stickers with a data-matrix code are unique to one unit. The grey
  rectangles in these photos cover them.
- **Strip location and camera data:**

  ```bash
  exiftool -all= -overwrite_original -ext jpg -ext jpeg photos
  ```

- Keep the full resolution. If a file is over about 10 MB, consider Git LFS rather than shrinking it,
  since chip markings need the detail.

Some markings in [parts.md](../parts.md) were read from close-ups that are not published, because the
same frame shows a serial label. Those entries say so.
