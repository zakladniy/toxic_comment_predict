run:
	uvicorn src.application.main:app --reload

test:
	pytest -v tests