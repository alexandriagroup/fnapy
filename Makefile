install:
	@echo "Install from Pypi"
	pip install -U fnapy

dev_install:
	@echo "Install local package"
	pip install -e .

uninstall:
	pip uninstall fnapy
	
online_tests:
	pytest -v tests/online/test_*.py

offline_tests:
	pytest -v tests/offline/test_*.py

tests: offline_tests
	pytest -v tests/test_*.py

clean:
	rm -rf dist build fnapy.egg-info
	rm -rf fnapy/{*.pyc,__pycache__}
	rm -rf tests/{*.pyc,__pycache__}
	rm -rf tests/online/{*.pyc,__pycache__}
	rm -rf tests/offline/{*.pyc,__pycache__}

tags:
	ctags -R **/*.py

release:
	rm -r dist
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: clean tags tests
