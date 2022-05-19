import random


class TraitGenerator:
    def __init__(self, config):
        self.traits = []
        self.config = config

        # random.seed(config["seed"])

    def generate(self):
        for i in range(self.config["number"]):
            print(f"generate {i}")
            new_trait = self._new_random_unique_trait()
            self.traits.append(new_trait)

        return self.traits

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
