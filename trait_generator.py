import json
import random

from matplotlib import pyplot as plt


class TraitGenerator:
    def __init__(self, config):
        self.traits = []
        self.config = config

        random.seed(config["seed"])

    def generate(self):
        print("======= Generate Traits Start =======")
        for i in range(self.config["number"]):
            print(f"generate {i}")
            new_trait = self._new_random_unique_trait()
            self.traits.append(new_trait)

        print("======= Validation Traits Start =======")
        if self._validate():
            print("Confirmed that every single trait is unique")
        else:
            print("Error! There are duplicated trait")
            return

        print("======= Save All Traits Start =======")
        self._generate_all_trait_metadata()
        print("saved to metadata/all-traits.json")

        return self.traits

    def _validate(self):
        return self._is_all_trait_unique(self.traits)

    def _generate_all_trait_metadata(self):
        METADATA_FILE_NAME = './metadata/all-traits.json'
        with open(METADATA_FILE_NAME, 'w') as outfile:
            json.dump(self.traits, outfile, indent=4)

    def _new_random_unique_trait(self):
        trait = {}

        traits = self.config["traits"]
        categories = list(traits.keys())
        for category in categories:
            trait[category] = random.choices(
                [k for k in traits[category].keys()],
                [v["prob"] for v in traits[category].values()]
            )[0]

        if trait in self.traits:
            return self._new_random_unique_trait()
        else:
            return trait

    def _is_all_trait_unique(self, traits):
        seen = list()
        return not any(i in seen or seen.append(i) for i in traits)

    def plot_generated_traits(self):
        traits_config = self.config["traits"]
        for attribute in traits_config:
            counts_dict = {k: 0 for k in traits_config[attribute].keys()}
            for trait in self.traits:
                counts_dict[trait[attribute]] = counts_dict.get(trait[attribute], 0) + 1

            labels, counts = zip(*sorted(counts_dict.items(), key=lambda x: x[1]))

            fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(aspect="equal"))
            ax.pie(counts, autopct='%.1f%%', labels=labels, startangle=90, radius=1.1)

            ax.set_title(attribute)

            plt.savefig(f"plot/plot_{attribute}.png")
