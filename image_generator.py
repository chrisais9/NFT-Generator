import pathlib

from PIL import Image
from image4layer import Image4Layer


class ImageGenerator:
    def __init__(self, config):
        self.config = config

        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

    def parse_image_directory(self, trait):

        image_path = dict.fromkeys(self.config["order"])

        human_type = trait["type"].split("-", 1)[0]

        for key, val in trait.items():
            if pathlib.Path(f"layer/{key}/{human_type}/{val}.png").exists():  # parse path by type
                image_path[key] = f"layer/h_{key}/{human_type}/{val}.png"

                if f"h_{key}" in image_path:
                    image_path[f"h_{key}"] = f"layer/{key}/{human_type}/{val}.png"
            elif pathlib.Path(f"layer/{key}/common/{val}.png").exists():  # if type doesn't exist, get path from common
                image_path[key] = f"layer/{key}/common/{val}.png"

                if f"h_{key}" in image_path:
                    image_path[f"h_{key}"] = f"layer/h_{key}/common/{val}.png"
            else:  # error
                print(key, val, " no")

        return image_path

    def generate_image(self, trait):

        print(trait)
        image_path = self.parse_image_directory(trait)
        print(image_path)
        # stack = Image.new('RGBA', (self.width, self.height))
        #
        # for category, name in trait.items():
        #     image_layer = Image.open(f'{self.config["traits"][category]["values"][name]["src"]}').convert('RGBA')
        #     stack = Image.alpha_composite(stack, image_layer)
        #
        # filter = Image.open("layer/filter.png").convert("RGBA")
        # filter.putalpha(int(256 * 0.3))
        # stack = Image4Layer.pin_light(stack, filter)
        #
        # stack = stack.convert('RGB')
        # return stack
