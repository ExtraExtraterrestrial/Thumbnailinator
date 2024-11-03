### Quick docs:
# make_thumbnails iterates over files in a given directory and makes thumnails out of them.

# kwargs:
#   source_path         - path to original images
#   output_path			- directory to which thumbnails are saved
#   new_width/height    - the sizes of the output thumbnail
#   format				- format of the image, see: PIL.format
#   forceOverwrite      - whether the program should ask for permission before overwriting pre-existing thumbnails
#   pattern				- function that takes and returns a string
#							it transforms the name of the original image
#							None - a thumbnail_ is added before the name of the original file 

from pathlib import Path
from PIL import Image
from typing import Callable

if __name__ == "__main__": import argparse


def make_thumbnails(
        source_path 	:str = "gallery",
        output_path		:str = "gallery_thumb",
        new_w   		:int = 360,
        new_h   		:int = 360,
        format			:str = "JPEG",
        forceOverwrite  :bool = False,
        pattern			:Callable[[str], str] = None) -> None:
    
    gallery_dir = Path(source_path)
    thumbnail_dir = Path(output_path)

    if not thumbnail_dir.exists():
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

    for file in gallery_dir.iterdir():
        outputFile = thumbnail_dir.joinpath(f"thumbnail_{file.name}")      # default value

        if pattern and callable(pattern):
            outputFile = thumbnail_dir.joinpath(pattern(file.name))
        
        with Image.open(gallery_dir.joinpath(file.name)) as img:
            
            width, height = img.size

            newScale = max(new_w/width, new_h/height)
            
            img = img.resize( (int(newScale * width), int(newScale*height)))

            width, height = img.size

            left = (width - new_w) // 2
            right = left + new_w
            top = (height - new_h) // 2
            bottom = top + new_h

            img = img.crop((left, top, right, bottom))

            if outputFile.exists() and not forceOverwrite:
                overwriteAnswer = input(f"Do you want to overwrite the file `{outputFile.name}`? (y/n) ")
                if overwriteAnswer.lower() == 'y' or overwriteAnswer == '1':
                    img.save(outputFile, format if format else None)
                    print(f"File `{outputFile.name}` overwritten!\n")   
                else:
                    print(f"File `{outputFile.name}` not overwritten!\n")
            else:
                img.save(outputFile, format if format else None)


    
    print("\nThumbnailinator is done!")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='Thumbnailinator',
        description="Generate thumbnails from images."
    )

    parser.add_argument("source_path", help="path to the directory with original images")
    parser.add_argument("output_path", help="path to the thumbnail directory")
    parser.add_argument('width', type=int, help="width of the thumbnails")
    parser.add_argument('height', type=int, help="height of the thumbnails")
    parser.add_argument('-f', '--format', dest="format", default="JPEG", help="image format, JPEG by default (ex. PNG, BPM, DDS)")
    parser.add_argument('-y', '-Y', dest="forceOverwrite", action="store_true", help="whether to inform of file overwrite")
    
    parsed = parser.parse_args()

    make_thumbnails(parsed.source_path, parsed.output_path, parsed.width, parsed.height, parsed.format, parsed.forceOverwrite)