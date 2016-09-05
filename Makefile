clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +;
	find . -type f -name "*~" -delete

install:
	pip install -e .
	pip install -r requirements-dev.txt
	rm -rf oandav20.egg-info/

release:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	rm -rf build/ dist/ oandav20.egg-info/

update-meta:
	python setup.py register
	rm -rf oandav20.egg-info/
