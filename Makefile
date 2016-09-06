online_tests:
	pytest -v tests/online/test_*.py


offline_tests:
	pytest -v tests/offline/test_offers.py
	pytest -v tests/offline/test_orders.py



clean:
	rm -f fnapy/*.pyc
	rm -f tests/*.pyc
	rm -f tests/online/*.pyc
	rm -f tests/offline/*.pyc


.PHONY: clean
