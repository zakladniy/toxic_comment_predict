import warnings
from pathlib import Path, PurePath

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from transformers import (
    AutoTokenizer,
    BertForSequenceClassification,
)

from .api_models import Comments
from .classifier.predict_tools import get_prediction

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


# Load BERT tokenizer and model from file
bert_model = BertForSequenceClassification.from_pretrained(
    BERT_MODEL, num_labels=2).to('cpu')
bert_model.eval()
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
        logger.info(f"input_text: {pred['input_text']}, "
                    f"class: {pred['class']}, "
                    f"toxic_proba: {pred['toxic_proba']}")
    return {
        'data': predictions,
    }
