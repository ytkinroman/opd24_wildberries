from joblib import load


class NeuroClassifier:
    def __init__(self, classifier_path: str) -> None:
        """
        Инициализация NeuroClassifier.

        Параметры:
        - classifier_path (str): Путь к обученной модели классификатора.
        """
        self.classifier = load(classifier_path)

    def get_data(self, data_list: list[str]) -> str:
        """
        Генератор, который возвращает каждую строку данных из входного списка.

        Параметры:
        - data_list: Входной список данных.

        Возвращает:
        - line: Каждая строка данных из входного списка.
        """
        for line in data_list:
            yield line

    def classify_data(self, data_list: list[str]) -> list[dict]:
        """
        Классификация списка текстовых данных с использованием обученного классификатора.

        Параметры:
        - data_list (list[str]): Список текстовых данных для классификации.

        Возвращает:
        - results (list[dict]): Список словарей, содержащих результаты классификации для каждых текстовых
          данных. Каждый словарь содержит следующие ключи:
            - 'label' (str): Предсказанная метка/класс.
            - 'score' (float): Уверенность в предсказании.
            - 'text' (str): Входной текст.
        """
        results = []
        for text in self.get_data(data_list):
            result = self.classifier(text)
            result_dict = {'label': result[0]['label'], 'score': round(result[0]['score'], 6), 'text': text}
            results.append(result_dict)
        return results
