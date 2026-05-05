.PHONY: all clean install

all:
	py RsaGui.py

clean:
	rm -rf private_key.tsv public_key.tsv cracking_metrics.csv __pycache__

install:
	pip install -r requirements.txt
