from PIL import Image
from image4layer import Image4Layer


class ImageGenerator:
    def __init__(self, config):
        self.config = config

        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

    def generate_image(self, trait):
        stack = Image.new('RGBA', (self.width, self.height))

        for category, name in trait.items():
            image_layer = Image.open(f'{self.config["traits"][category]["values"][name]["src"]}').convert('RGBA')
            stack = Image.alpha_composite(stack, image_layer)

        # filter = Image.open("layer/filter.png").convert("RGBA")
        # filter.putalpha(int(256 * 0.3))
        # stack = Image4Layer.pin_light(stack, filter)

        stack = stack.convert('RGB')
        return stack
