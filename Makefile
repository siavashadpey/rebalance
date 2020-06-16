all:
	make test

test:
	python3 -m unittest discover -s . -p "*_test.py" -v

coverage:
	coverage run -m unittest discover -s . -p "*_test.py" -v


coverage_report:
	coverage html

