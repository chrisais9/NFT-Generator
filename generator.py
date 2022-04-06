from PIL import Image
from image4layer import Image4Layer

im1 = Image.open(f'traits/1.png').convert('RGBA')
im2 = Image.open(f'traits/2.png').convert('RGBA')
im3 = Image.open(f'traits/3.png').convert('RGBA')
im4 = Image.open(f'traits/4.png').convert('RGBA')
im5 = Image.open(f'traits/5.png').convert('RGBA')
im6 = Image.open(f'traits/6.png').convert('RGBA')
im7 = Image.open(f'traits/7.png').convert('RGBA')
im8 = Image.open(f'traits/8.png').convert('RGBA')

stack = Image.alpha_composite(im1, im2)
stack = Image.alpha_composite(stack, im3)
stack = Image.alpha_composite(stack, im4)
stack = Image.alpha_composite(stack, im5)
stack = Image.alpha_composite(stack, im6)
stack = Image.alpha_composite(stack, im7)
stack = Image.alpha_composite(stack, im8)

filter = Image.open("traits/watercolor.png").convert("RGBA")
filter.putalpha(int(256*0.3))

final = Image4Layer.pin_light(stack, filter)

final.show()