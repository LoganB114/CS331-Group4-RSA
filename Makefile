.PHONY: all clean

all:
	py RsaGui.py

clean:
	rm -rf private_key.tsv public_key.tsv cracking_metrics.csv __pycache__
