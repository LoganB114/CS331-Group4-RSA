.PHONY: all clean install

# Start the program
all:
	py RsaGui.py

# Remove generated files
clean:
	rm -rf private_key.tsv public_key.tsv cracking_metrics.csv __pycache__

# Install dependencies
install:
	pip install -r requirements.txt

# Remove installed dependencies
uninstall:
	pip uninstall -r requirements.txt
