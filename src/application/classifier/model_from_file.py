"""Module with paths and load model from file."""
import warnings
from pathlib import Path, PurePath

from transformers import (
    AutoTokenizer,
    BertForSequenceClassification,
)

warnings.filterwarnings("ignore")

PROJECT_DIR: Path = Path(__file__).parent.parent.parent.parent.resolve()
MODEL_DIR: PurePath = PurePath(PROJECT_DIR, "model")

BERT_MODEL: str = str(PurePath(MODEL_DIR, "bert_toxic_predict"))
BERT_TOKENIZER: str = str(PurePath(MODEL_DIR, "tokenizer"))


def load_model_from_file() -> tuple[BertForSequenceClassification,
                                    AutoTokenizer]:
    """Load model from file.

    @return: BERT-model, BERT-tokenizer
    """
    # Load BERT tokenizer and model from file
    bert_model: BertForSequenceClassification = (
        BertForSequenceClassification.from_pretrained(
            BERT_MODEL,
            num_labels=2
        ).to("cpu")
    )
    bert_model.eval()
    bert_tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(
        BERT_TOKENIZER
    )
    return bert_model, bert_tokenizer
