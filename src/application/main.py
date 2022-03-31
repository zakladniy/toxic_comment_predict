from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from .api_models import Comments
from .classifier.model_from_file import load_model_from_file
from .classifier.predict_tools import get_prediction

# Logs configuration
logger.add(
    "info_api.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="100 KB",
    compression="zip",
)

app_desc = """<h2>API for predict probability of toxicity russian comment</h2>
<br>by Zakladniy Anton"""

app = FastAPI(
    title="Web application for predict probability "
          "of toxicity russian comments",
    description=app_desc,
)

bert_model, bert_tokenizer = load_model_from_file()


@app.get("/")
def redirect_to_docs() -> RedirectResponse:
    """Auto redirect to docs page.

    @return: RedirectResponse
    """
    return RedirectResponse("/docs")


@app.post("/api/toxic_predict")
def product_group_predict(data: Comments) -> dict[str, list[dict]]:
    """API endpoint for predict toxicity of russian comments.

    @param data: russian texts/comments for predict
    @return: label and toxic probability for each comment
    """
    predictions = get_prediction(
        texts=data.comments,
        tokenizer=bert_tokenizer,
        model=bert_model,
    )
    for pred in predictions:
        logger.info(
            f"input_text: {pred['input_text']}, "
            f"class: {pred['class']}, "
            f"toxic_proba: {pred['toxic_proba']}"
        )
    return {
        "data": predictions,
    }
