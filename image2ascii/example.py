from image2ascii import image2ascii

image_path = r'src/image.png'
width = 100
height = 25

ascii_art = image2ascii(image_path, width, height, black=" ")
print(ascii_art)