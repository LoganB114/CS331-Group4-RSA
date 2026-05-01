import csv
import os

"""
Dedicated class for Evaluation Metrics.
Logs the time it takes to crack keys of different bit lengths.
"""
def log_crack_time(modulus_bit_length, rounds, elapsed_ms, success):
    """
    Logs the cracking attempt to a CSV file.
    
    Args:
        modulus_bit_length (int): The bit length of the target modulus (n)
        rounds (int): The number of rounds used in the cracking attempt
        elapsed_ms (float): How long the crack took in milliseconds
        success (bool): Whether the crack was successful or not
    """
    filename = "cracking_metrics.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write headers if the file is brand new
        if not file_exists:
            writer.writerow(["Modulus Bit Length", "Rounds", "Time Elapsed (ms)", "Success"])
        
        # Log the data
        writer.writerow([modulus_bit_length, rounds, elapsed_ms, success])
        
    print(f"Metrics logged to {filename}")