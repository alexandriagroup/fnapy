online_test:
	pytest -v tests/online/test_fnapy_manager.py


clean:
	rm -f fnapy/*.pyc
	rm -f tests/*.pyc
	rm -f tests/online/*.pyc


.PHONY: clean
