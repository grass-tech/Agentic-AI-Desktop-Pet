import json


class Parameters:
    def __init__(self, model_path: str):
        with open(model_path, 'r', encoding='utf-8') as mf:
            self.parameters = json.load(mf)
            mf.close()

    @property
    def get_expressions(self) -> list[str]:
        expressions = []
        try:
            for item in self.parameters['expressions']:
                expressions.append(item['name'])
        except KeyError:
            pass
        return expressions

    @property
    def get_motions(self) -> dict[str, list[str]]:
        motions: dict[str, list[str]] = {"NULL": ["motions/null.json"]}
        try:
            for motion in self.parameters['motions']:
                for file in self.parameters['motions'][motion]:
                    if motion not in motions:
                        motions.update({motion: []})
                    motions[motion].append(file['file'])
        except KeyError:
            pass
        return motions


if __name__ == '__main__':
    print(Parameters("../resources/model/Mao/mao.model3.json").get_expressions)
