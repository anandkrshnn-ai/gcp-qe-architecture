.PHONY: demo setup test clean verify

setup:
	pip install -r requirements.txt

demo:
	python run_demo.py

test:
	$env:PYTHONPATH = "src"; python -m pytest tests/test_safety_core.py

verify: test demo

clean:
	Remove-Item -Recurse -Force __pycache__, .pytest_cache -ErrorAction SilentlyContinue
	Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
