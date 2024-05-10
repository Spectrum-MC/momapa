init:
	python -m pip install -r requirements-dev.txt

test:
	python setup.py pytest

flake8:
	python -m flake8 momapa/

release:
	python setup.py sdist bdist_wheel
	twine upload dist/*