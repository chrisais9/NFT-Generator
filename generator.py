import random
from matplotlib import pyplot as plt
import yaml
from trait_generator import TraitGenerator
from image_generator import ImageGenerator
from metadata_generator import MetadataGenerator


class Generator:

    def __init__(self):
        with open('config.xx.yaml') as config:
            self.config_xx = yaml.load(config, Loader=yaml.FullLoader)

        with open('config.xx.yaml') as config:
            self.config_xy = yaml.load(config, Loader=yaml.FullLoader)

    def generate(self):
        trait_generator_xx = TraitGenerator(self.config_xx)
        traits_xx = trait_generator_xx.generate()

        trait_generator_xy = TraitGenerator(self.config_xy)
        traits_xy = trait_generator_xy.generate()

        traits = traits_xx + traits_xy
        random.shuffle(traits)

        plot_generated_traits("xx", self.config_xx, traits_xx)
        plot_generated_traits("xy", self.config_xy, traits_xy)

        metadata_generator = MetadataGenerator(self.config_xx)
        metadata_generator.generate(traits)

        image_generator = ImageGenerator(self.config_xx)
        image_generator.generate(traits)

        # uploader = Uploader()
        # uploader.upload()


def plot_generated_traits(prefix, config, traits):
    traits_config = config["traits"]
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(aspect="equal"))
    for attribute in traits_config:
        counts_dict = {k: 0 for k in traits_config[attribute].keys()}
        for trait in traits:
            counts_dict[trait[attribute]] = counts_dict.get(trait[attribute], 0) + 1

        labels, counts = zip(*sorted(counts_dict.items(), key=lambda x: x[1]))

        ax.pie(counts, autopct='%.1f%%', labels=labels, startangle=90, radius=1.1)

        ax.set_title(attribute)

        plt.savefig(f"plot/plot_{prefix}_{attribute}.png")
        plt.cla()
    plt.close(fig)


def main():
    generator = Generator()
    generator.generate()


if __name__ == '__main__':
    main()
