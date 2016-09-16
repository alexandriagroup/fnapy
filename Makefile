online_tests:
	pytest -v tests/online/test_*.py

offline_tests:
	pytest -v tests/offline/test_*.py

tests: offline_tests
	pytest -v tests/test_*.py

clean:
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
