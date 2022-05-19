import random
from matplotlib import pyplot as plt
import yaml
from trait_generator import TraitGenerator
from image_generator import ImageGenerator
from metadata_generator import MetadataGenerator


class Generator:

    def __init__(self):

        with open('config.yaml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        with open('config.xx.yaml') as config:
            self.config_xx = yaml.load(config, Loader=yaml.FullLoader)

        with open('config.xy.yaml') as config:
            self.config_xy = yaml.load(config, Loader=yaml.FullLoader)

    @staticmethod
    def is_every_trait_unique(traits):
        seen = list()
        return not any(i in seen or seen.append(i) for i in traits)

    @staticmethod
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

    def generate(self):
        print("======= Generate Traits XX Start =======")
        trait_generator_xx = TraitGenerator(self.config_xx)
        traits_xx = trait_generator_xx.generate()

        print("======= Generate Traits XY Start =======")
        trait_generator_xy = TraitGenerator(self.config_xy)
        traits_xy = trait_generator_xy.generate()

        traits = traits_xx + traits_xy
        random.shuffle(traits)

        print("======= Validation Traits Start =======")
        if Generator.is_every_trait_unique(traits):
            print("Confirmed that every single trait is unique")
        else:
            print("Error! There are duplicated trait")
            return

        Generator.plot_generated_traits("xx", self.config_xx, traits_xx)
        Generator.plot_generated_traits("xy", self.config_xy, traits_xy)

        print("======= Save Token Metadata Start =======")
        metadata_generator = MetadataGenerator(self.config)
        metadata_generator.generate(traits)

        print("======= Generate Images Start =======")
        image_generator = ImageGenerator(self.config)
        image_generator.generate(traits)

        # print("======= Upload To IPFS Start =======")
        # uploader = Uploader()
        # uploader.upload()


def main():
    generator = Generator()
    generator.generate()


if __name__ == '__main__':
    main()
