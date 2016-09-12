online_tests:
	pytest -v tests/online/test_*.py

offline_tests:
	pytest -v tests/offline/test_*.py

tests: offline_tests
	pytest -v tests/test_*.py

clean:
	rm -f fnapy/*.pyc
	rm -f tests/*.pyc
	rm -f tests/online/*.pyc
	rm -f tests/offline/*.pyc

tags:
	ctags -R **/*.py


.PHONY: clean tags tests
