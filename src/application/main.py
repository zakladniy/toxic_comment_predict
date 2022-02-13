from typing import Tuple

import gradio as gr
import torch
from transformers import (
    AutoTokenizer,
    BertForSequenceClassification,
)

from text_preprocessing import TextPreprocessing

BERT_MODEL = '../../model/bert_toxic_predict'
BERT_TOKENIZER = '../../model/tokenizer'
MAX_LENGTH = 41


cleaner = TextPreprocessing()


# Set number of threads for BERT inference
torch.set_num_threads(1)


# Load BERT tokenizer and model from file
bert_model = BertForSequenceClassification.from_pretrained(BERT_MODEL, num_labels=2).to('cpu')
bert_tokenizer = AutoTokenizer.from_pretrained(BERT_TOKENIZER)


def get_prediction(text: str) -> Tuple[str, float]:
    """Predict toxic comment

    :param text: input comment
    :return: label and probability
    """
    # Clean and lemmatize text
    text = cleaner.text_preprocessing(text)
    # Tokenize preprocessed text
    inputs = bert_tokenizer(
        [text],
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    ).to('cpu')
    # BERT raw outputs
    outputs = bert_model(**inputs)
    # Probabilities
    probs = outputs[0].softmax(1).to('cpu').detach().numpy()
    proba = probs[0]
    return 'Toxic' if proba[1] > 0.5 else 'Non toxic', float(proba[1])


if __name__ == "__main__":
    # Create GUI
    iface = gr.Interface(
      fn=get_prediction,
      inputs=gr.inputs.Textbox(
          lines=2,
          placeholder="Enter text...",
          label="Comment for prediction",
      ),
      outputs=[
          gr.outputs.Textbox(label="Predicted label"),
          gr.outputs.Textbox(label="Probability of toxic comment"),
      ],
    )
    iface.launch()
