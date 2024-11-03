### Quick docs:
# make_thumbnails iterates over files in a given directory and makes thumnails out of them.

# kwargs:
#   source_path         - path to original images
#   output_path			- directory to which thumbnails are saved
#   new_width/height    - the sizes of the output thumbnail
#   format				- format of the image, see: PIL.format
#   force_overwrite     - whether the program should ask for permission before overwriting pre-existing thumbnails
#   pattern				- function that takes and returns a string
#							it transforms the name of the original image
#							None - a thumbnail_ is added before the name of the original file 

from PIL import Image
from pathlib import Path
from typing import Callable

from multiprocessing.pool import Pool as mpPool

if __name__ == "__main__": import argparse


# in case of export, make sure it's within __name__ == __main__ clause when using multiprocessing
# this is due to mpPool's need of replication of the source file, which results in an infinite loop
# multiprocessing seems to be faster for directories with ~15+ images
def thumbnalizeDirectory(
        source_path 	:str = "gallery",
        output_path		:str = "gallery_thumb",
        new_w   		:int = 360,
        new_h   		:int = 360,
        format_			:str = "JPEG",
        force_overwrite :bool = False,
        multiprocessing :bool = True,
        pattern			:Callable[[str], str] = lambda x: "thumbnail_"+str(x)
        ) -> None:
    
    gallery_dir = Path(source_path)
    thumbnail_dir = Path(output_path)

    if not thumbnail_dir.exists():
        thumbnail_dir.mkdir(parents=True, exist_ok=True)
    
    if (multiprocessing):
        with mpPool() as pool:
            pool.starmap(thumbnalizeImage,
                [[
                    gallery_dir.joinpath(file.name), 
                    thumbnail_dir.joinpath(pattern(file.name)),
                    new_w, new_h, force_overwrite, format_
                ]
                for file in gallery_dir.iterdir()]
            )
    else:
        for file in gallery_dir.iterdir():
            thumbnalizeImage(
                gallery_dir.joinpath(file.name), 
                thumbnail_dir.joinpath(pattern(file.name)),
                new_w, new_h, force_overwrite, format_
            )


    
def thumbnalizeImage(
        source_file:Path, 
        output_file:Path,
        new_w:int, 
        new_h:int, 
        force_overwrite:bool,
        format_:str
        )-> None:

    with Image.open(source_file) as img:
        
        width, height = img.size

        newScale = max(new_w/width, new_h/height)
        
        img = img.resize( (int(newScale * width), int(newScale*height)))

        width, height = img.size

        left = (width - new_w) // 2
        right = left + new_w
        top = (height - new_h) // 2
        bottom = top + new_h

        img = img.crop((left, top, right, bottom))

        if output_file.exists() and not force_overwrite:
            overwriteAnswer = input(f"Do you want to overwrite the file `{output_file.name}`? (y/n) ")
            if overwriteAnswer.lower() == 'y' or overwriteAnswer == '1':
                img.save(output_file, format_ if format_ else None)
                print(f"File `{output_file.name}` overwritten!\n")
            else:
                print(f"File `{output_file.name}` not overwritten!\n")
        else:
            img.save(output_file, format_ if format_ else None)




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
    parser.add_argument('--notmp', dest="not_multiprocessing", action="store_false", help="do not use multiprocessing")
    parser.add_argument('-y', '-Y', dest="force_overwrite", action="store_true", help="whether to inform of file overwrite")

    parsed = parser.parse_args()

    thumbnalizeDirectory(
        parsed.source_path, parsed.output_path, 
        parsed.width, parsed.height, 
        parsed.format, 
        parsed.force_overwrite, not parsed.not_multiprocessing)