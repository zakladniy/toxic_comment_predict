import warnings
from pathlib import Path, PurePath
from typing import Tuple

import torch
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from transformers import (
    AutoTokenizer,
    BertForSequenceClassification,
)

from .text_preprocessing import text_preprocessing

warnings.filterwarnings('ignore')

# Logs configuration
logger.add(
    'info_api.log',
    format='{time} {level} {message}',
    level='INFO',
    rotation='100 KB',
    compression='zip',
)


app_desc = """<h2>API for predict probability of toxicity russian comment</h2>
<br>by Zakladniy Anton"""


# Paths
project_dir: Path = Path(__file__).parent.parent.parent.resolve()
model_dir: PurePath = PurePath(project_dir, 'model')
BERT_MODEL: str = str(PurePath(model_dir, 'bert_toxic_predict'))
BERT_TOKENIZER: str = str(PurePath(model_dir, 'tokenizer'))


MAX_LENGTH = 512


# Set number of threads for BERT inference
torch.set_num_threads(1)


# Load BERT tokenizer and model from file
bert_model = BertForSequenceClassification.from_pretrained(
    BERT_MODEL, num_labels=2).to('cpu')
bert_tokenizer = AutoTokenizer.from_pretrained(BERT_TOKENIZER)


app = FastAPI(
    title='Web application for predict probability of toxicity russian comment',
    description=app_desc,
)


resp_example = {
    200: {
        "description": "Success response",
        "content": {
            "application/json": {
                "example": {
                    'data': {
                        "preprocessed_text": "str",
                        },
                    },
                },
            },
        },
}


@app.get('/')
def redirect_to_docs() -> RedirectResponse:
    """Autoredirect to docs page

    @return: RedirectResponse
    """
    return RedirectResponse('/docs')


def get_prediction(text: str, tokenizer: AutoTokenizer,
                   model: BertForSequenceClassification,
                   max_length: int = MAX_LENGTH) -> Tuple[str, float]:
    """Predict label and toxic probability by input text

    @param text: input text
    @param tokenizer: BERT tokenizer
    @param model: BERT model
    @param max_length: sequence maximum length
    @return: label and toxic probability
    """
    # Clean input text
    text = text_preprocessing(text)
    # Tokenize preprocessed text
    inputs = tokenizer(
        [text],
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    ).to('cpu')
    # BERT raw outputs
    outputs = model(**inputs)
    # Probabilities
    probs = outputs[0].softmax(1).to('cpu').detach().numpy()
    proba = probs[0]
    return 'Toxic' if proba[1] > 0.5 else 'Non toxic', float(proba[1])


@app.get('/api/toxic_predict')
def product_group_predict(text: str):
    """API endpoint for predict toxicity of russian comment.

    @param text: russian text/comment for predict
    @return: label and toxic probability
    """
    predictions = get_prediction(
        text=text,
        tokenizer=bert_tokenizer,
        model=bert_model,
    )
    logger.info(f"Is ours predict: input: {text}, "
                f"is ours: {predictions[0]}, proba: {predictions[1]}")
    return {
        'data':
            {
                'label': predictions[0],
                'proba_of_toxic': predictions[1],
            },
    }
