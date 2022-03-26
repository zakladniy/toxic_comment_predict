import warnings
from pathlib import Path, PurePath
from typing import List

import numpy as np
import torch
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from transformers import (
    AutoTokenizer,
    BertForSequenceClassification,
)

from .api_models import Comments
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


# Paths
project_dir: Path = Path(__file__).parent.parent.parent.resolve()
model_dir: PurePath = PurePath(project_dir, 'model')
BERT_MODEL: str = str(PurePath(model_dir, 'bert_toxic_predict'))
BERT_TOKENIZER: str = str(PurePath(model_dir, 'tokenizer'))

MAX_LENGTH = 275

# Set number of threads for BERT inference
torch.set_num_threads(1)

# Load BERT tokenizer and model from file
bert_model = BertForSequenceClassification.from_pretrained(
    BERT_MODEL, num_labels=2).to('cpu')
bert_tokenizer = AutoTokenizer.from_pretrained(BERT_TOKENIZER)


app_desc = """<h2>API for predict probability of toxicity russian comment</h2>
<br>by Zakladniy Anton"""

app = FastAPI(
    title='Web application for predict probability of toxicity russian '
          'comment',
    description=app_desc,
)


@app.get('/')
def redirect_to_docs() -> RedirectResponse:
    """Autoredirect to docs page.

    @return: RedirectResponse
    """
    return RedirectResponse('/docs')


def get_prediction(texts: List[str], tokenizer: AutoTokenizer,
                   model: BertForSequenceClassification,
                   max_length: int = MAX_LENGTH) -> List[dict]:
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
    ).to('cpu')
    outputs = model(**inputs)
    probas = outputs.logits.softmax(1).detach().numpy()
    toxic_probas = list(probas[:, 1])
    classes_num = list(np.argmax(probas, axis=1))
    classes = ['Toxic' if class_ == 1 else 'Not toxic' for class_ in
               classes_num]
    results = list(zip(classes, toxic_probas, texts))
    results = [{'class': item[0], 'toxic_proba': float(item[1]),
                'input_text': item[2]} for item in results]
    return results


@app.post('/api/toxic_predict')
def product_group_predict(data: Comments):
    """API endpoint for predict toxicity of russian comment.

    @param data: russian texts/comments for predict
    @return: label and toxic probability
    """
    predictions = get_prediction(
        texts=data.comments,
        tokenizer=bert_tokenizer,
        model=bert_model,
    )
    for pred in predictions:
        logger.info(f"Input_text: {pred['input_text']}, "
                    f"class: {pred['class']}, "
                    f"toxic_proba: {pred['toxic_proba']}")
    return {
        'data': predictions,
    }
