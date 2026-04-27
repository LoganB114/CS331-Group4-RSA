import csv
import os

class MetricsManage:
    """
    Dedicated class for Evaluation Metrics.
    Logs the time it takes to crack keys of different bit lengths.
    """
    @staticmethod
    def log_crack_time(modulus_bit_length, elapsed_ms, success):
        """
        Logs the cracking attempt to a CSV file.
        
        Args:
            modulus_bit_length (int): The bit length of the target modulus (n)
            elapsed_ms (float): How long the crack took in milliseconds
            success (bool): Whether the crack was successful or not
        """
        filename = "cracking_metrics.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            # Write headers if the file is brand new
            if not file_exists:
                writer.writerow(["Modulus Bit Length", "Time Elapsed (ms)", "Success"])
            
            # Log the data
            writer.writerow([modulus_bit_length, elapsed_ms, success])
            
        print(f"Metrics logged to {filename}")