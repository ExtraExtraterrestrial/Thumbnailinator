# Thumbnailinator
Creates centered thumbnails from images using Python3 (with PIL and pathlib) by resizing the image.
Requires Python with PIL.

```
thumbnailinator.py [-h] [-f FORMAT] [--notmp] [-y] source_path output_path width height

positional arguments:
  source_path                 path to the directory with original images
  output_path                 path to the thumbnail directory
  width                       width of the thumbnails
  height                      height of the thumbnails

options:
  -f FORMAT                   image format - JPEG by default (ex. PNG, BPM, DDS)
  --notmp                     flag: do not use multiprocessing
  -y, -Y                      flag: do not inform of file overwrites when saving thumbnails
```
