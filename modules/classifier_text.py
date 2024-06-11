from transformers import BertTokenizer, BertForSequenceClassification
import torch

__version__ = "2.0.0"
__author__ = "ytkinroman"


class NeuroClassifier:
    def __init__(self, tokenizer_path: str, model_path: str) -> None:
        self.__tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.__model = BertForSequenceClassification.from_pretrained(model_path)
        self.__class_labels = {0: "neutral", 1: "positive", 2: "negative"}

    def classify_text(self, text: str):
        input_ids = self.__tokenizer.encode(text, add_special_tokens=True, max_length=512, truncation=True)
        input_ids_tensor = torch.tensor([input_ids])

        outputs = self.__model(input_ids_tensor)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)

        results = []
        for i, prob in enumerate(probs[0]):
            class_label = self.__class_labels[i]
            r = {"label": class_label, "score": round(prob.item(), 3)}
            results.append(r)

        return {"text": text, "results": results}

    def classify_data(self, data):
        results = []
        for text in data:
            r = self.classify_text(text)
            results.append(r)
        return results
