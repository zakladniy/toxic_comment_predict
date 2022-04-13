"""Module with predict tools."""
from typing import List

import numpy as np
import torch
from transformers import (
    AutoTokenizer,
    BertForSequenceClassification,
)

from .text_preprocessing import text_preprocessing

MAX_LENGTH = 275


def get_prediction(
    texts: List[str],
    tokenizer: AutoTokenizer,
    model: BertForSequenceClassification,
    max_length: int = MAX_LENGTH,
) -> List[dict]:
    """Predict label and toxic probability by input text.

    @param texts: list of texts or comments
    @param tokenizer: BERT tokenizer
    @param model: BERT model
    @param max_length: sequence maximum length
    @return: label and toxic probability
    """
    # Clean input texts
    clean_texts = [text_preprocessing(text) for text in texts]
    # Tokenize preprocessed text
    inputs = tokenizer(
        clean_texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    ).to("cpu")
    with torch.no_grad():
        outputs = model(**inputs)
        probas = outputs.logits.softmax(1).detach().numpy()
    toxic_probas = list(probas[:, 1])
    classes_num = list(np.argmax(probas, axis=1))
    classes = ["Toxic" if class_ == 1 else "Not toxic" for class_ in classes_num]
    results = list(zip(classes, toxic_probas, texts))
    results = [
        {
            "class": item[0],
            "toxic_proba": float(item[1]),
            "input_text": item[2],
        }
        for item in results
    ]
    return results
