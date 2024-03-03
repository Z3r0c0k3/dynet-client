import sys
try:
    from PIL import Image
except:
    sys.exit("PIL package not installed")

def image2ascii(image_path:str, width:int, height:int, 
                ascii_chars:str="@%#*+=-:. ", black:str=' ') -> str:
    img = Image.open(image_path)
    img = img.resize((width, height))
    img = img.convert('L')

    pixels = img.getdata()

    ascii_str = ''
    for i, brt_value in enumerate(pixels):
        if brt_value == 0:
            # if alpha channel or black (brightness 0)
            ascii_str += black
        else:
            ascii_str += ascii_chars[min(int(brt_value / (256 / len(ascii_chars))), len(ascii_chars) - 1)]
        
        # line break
        if (i + 1) % width == 0:
            ascii_str += '\n'
    
    return ascii_str
