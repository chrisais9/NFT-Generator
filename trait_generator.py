import random
import constant


class TraitGenerator:
    def __init__(self, config):
        self.traits = []
        self.config = config

    def generate(self):
        for i in range(self.config["number"]):
            print(f"generate {i}")
            new_trait = self._new_random_unique_trait()
            self.traits.append(new_trait)

        return self.traits

    def _new_random_unique_trait(self):
        trait = {}

        traits = self.config["traits"]
        for category in traits.keys():
            trait[category] = random.choices(
                [k for k in traits[category].keys()],
                [v["prob"] for v in traits[category].values()]
            ).pop()

        if trait in self.traits:
            return self._new_random_unique_trait()
        else:
            return trait
