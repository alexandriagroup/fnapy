online_test:
	pytest -v tests/online/test_fnapy_manager.py


offline_test:
	pytest -v tests/offline/test_offers.py


clean:
	rm -f fnapy/*.pyc
	rm -f tests/*.pyc
	rm -f tests/online/*.pyc
	rm -f tests/offline/*.pyc


.PHONY: clean
