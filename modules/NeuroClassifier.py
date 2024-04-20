from joblib import load
from typing import Iterable, List

__version__ = "1.3.0"
__author__ = "ytkinroman"


class NeuroClassifier:
    def __init__(self, classifier_path: str) -> None:
        """
        Инициализация NeuroClassifier.

        Параметры:
        - classifier_path (str): Путь к обученной модели классификатора.
        """
        self.classifier = load(classifier_path)

    def classify_data(self, data_iterable: Iterable[str]) -> List[dict]:
        """
        Классификация итерируемого объекта текстовых данных с использованием обученного классификатора.

        Параметры:
        - data_iterable (Iterable[str]): Итерируемый объект текстовых данных для классификации.

        Возвращает:
        - results (List[dict]): Список словарей, содержащих результаты классификации для каждого текстового
          данных. Каждый словарь содержит следующие ключи:
            - 'label' (str): Предсказанная метка/класс.
            - 'score' (float): Уверенность в предсказании.
            - 'text' (str): Входной текст.
        """
        results = []
        for text in data_iterable:
            result = self.classifier(text)
            result_dict = {'label': result[0]['label'], 'score': round(result[0]['score'], 6), 'text': text}
            results.append(result_dict)
        return results
