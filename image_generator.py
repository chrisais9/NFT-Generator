import pathlib

from PIL import Image


class ImageGenerator:
    def __init__(self, config):
        self.config = config

        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

    def parse_image_directory(self, trait):

        image_path = dict.fromkeys(self.config["order"])

        human_type = trait["type"].split("_", 1)[0]

        for trait_name, value in trait.items():
            if pathlib.Path(f"layer/{trait_name}/{human_type}/{value}.png").exists():  # parse path by type
                image_path[trait_name] = f"layer/{trait_name}/{human_type}/{value}.png"
                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/{trait_name}/{human_type}/{value}.png"
            elif pathlib.Path(
                    f"layer/{trait_name}/common/{value}.png").exists():  # if type doesn't exist, get path from common
                image_path[trait_name] = f"layer/{trait_name}/common/{value}.png"

                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/h_{trait_name}/common/{value}.png"
            else:  # error
                print(trait_name, human_type, value, " no")

        return image_path

    def merge_image_layer(self, trait):
        image_layer_path = self.parse_image_directory(trait)

        stack = Image.new('RGBA', (self.width, self.height))

        for layer, path in image_layer_path.items():
            if layer == "hair" or layer == "h_hair":
                if trait["headgear"] == "none":
                    image_layer = Image.open(path).convert('RGBA')
                    stack = Image.alpha_composite(stack, image_layer)
            elif layer == "h_headgear_hair":
                if trait["headgear"] != "none":
                    image_layer = Image.open(path).convert('RGBA')
                    stack = Image.alpha_composite(stack, image_layer)
            else:
                image_layer = Image.open(path).convert('RGBA')
                stack = Image.alpha_composite(stack, image_layer)

        stack = stack.convert('RGB')
        return stack

    def generate(self, traits):
        print("======= Generate Images Start =======")

        token_id = 1
        for trait in traits:
            print("generating", token_id, trait)
            image = self.merge_image_layer(trait)
            image.save(f'./images/{token_id}.jpeg')
            print(f"saved {token_id}")

            token_id += 1
