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
#							None - a _thumb is appended to the name of the original file 

from pathlib import Path
from PIL import Image, UnidentifiedImageError

if __name__ == "__main__": import argparse


def make_thumbnails(
        source_path 	:str = "gallery",
        output_path		:str = "gallery_thumb",
        new_width		:int = 360,
        new_height		:int = 360,
        format			:str = "JPEG",
        forceOverwrite  :bool = False,
        pattern			:callable = None) -> None:
    
    gallery_dir = Path(source_path)
    thumbnail_dir = Path(output_path)

    if not thumbnail_dir.exists():
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

    for file in gallery_dir.iterdir():
        try:
            with Image.open(gallery_dir.joinpath(file.name)) as img:
                width, height = img.size                            # get original sizes
                
                if height >= width:                                 # img is portrait
                    resized_height = int(height * new_width/width)  # calc height of resized img
                    img = img.resize((new_width, resized_height))   # resize the image while keeping ratio
                    width, height = img.size                        # get new sizes
                    top = (height - new_height)//2                  # get the central vertical values
                    bottom = (height + new_height)//2               # =/=
                    img = img.crop((0, top, new_width, bottom))     # crop image to center

                else:                                               # img is landscape
                    resized_width = int(width * new_height/height)  # calc width of resized img
                    img = img.resize((resized_width, new_height))   # resize the image while keeping ratio
                    width, height = img.size                        # get new sizes
                    left = (width - new_width)//2                   # get the central horizontal values
                    right = (width + new_width)//2                  # =/=
                    img = img.crop((left, 0, right, new_height))    # crop image to center
                  
                save_path = thumbnail_dir.joinpath(Path("thumbnail"))

                if pattern and callable(pattern):
                    save_path = thumbnail_dir.joinpath(pattern(file.name))
                else:
                    if file.suffix:
                        save_path = thumbnail_dir.joinpath(
                                f"{file.name.split('.')[0]}_thumb.{'.'.join(file.name.split('.')[1:])}"
                            )
                    else:
                        save_path = thumbnail_dir.joinpath(f"{file.name}_thumb")
                
                if save_path.exists() and not forceOverwrite:
                    overwriteAnswer = input(f"Do you want to overwrite the file `{save_path}`? (y/n) ")
                    if overwriteAnswer.lower() == 'y' or overwriteAnswer == '1':
                        img.save(save_path, format if format else None)
                        print(f"File `{save_path}` overwritten!\n")
                    else:
                        print(f"File `{save_path}` not overwritten!\n")
                else:
                    img.save(save_path, format if format else None)
        
        except UnidentifiedImageError as error:
            print(error)
    
    
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
    parser.add_argument('-Y', dest="forceOverwrite", action="store_true", help="whether to inform of file overwrite")
    
    parsed = parser.parse_args()

    make_thumbnails(parsed.source_path, parsed.output_path, parsed.width, parsed.height, parsed.format, parsed.forceOverwrite)