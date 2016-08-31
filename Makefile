test:
	pytest -v fnapy/test_client.py


clean:
	rm -f fnapy/*.pyc


.PHONY: clean
