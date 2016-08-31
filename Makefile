test:
	pytest -v tests/test_client.py


clean:
	rm -f fnapy/*.pyc
	rm -f tests/*.pyc


.PHONY: clean
