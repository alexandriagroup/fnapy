install:
	@echo "Install from Pypi"
	@pipenv install

dev_install:
	@echo "Install local package"
	@pipenv run pip install -e .

uninstall:
	@pipenv run pip uninstall fnapy
	
online_tests:
	@pipenv run pytest -vs tests/online/test_*.py

offline_tests:
	@pipenv run pytest -vs tests/offline/test_*.py

tests: offline_tests
	@pipenv run pytest -vs tests/test_*.py

clean:
	rm -rf dist build fnapy.egg-info __pycache__
	rm -rf .cache
	rm -rf fnapy/*.pyc fnapy/__pycache__
	rm -rf tests/*.pyc tests/__pycache__
	rm -rf tests/online/*.pyc tests/online/__pycache__
	rm -rf tests/offline/*.pyc tests/offline/__pycache__

tags:
	@ctags --exclude=docs --exclude=build --exclude=build -R .
	@echo 'Updated the tags file.'

release:
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: clean tags tests
