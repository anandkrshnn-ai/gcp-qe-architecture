.PHONY: demo setup test clean

setup:
	pip install -r requirements.txt

demo:
	python run_demo.py

test:
	pytest tests/

clean:
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
