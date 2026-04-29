import pandas as pd
import matplotlib.pyplot as plt

def create_performance_graphs():
    try:
        # Load the data we recorded
        data = pd.read_csv('cracking_metrics.csv')
        
        # only graph successful cracks
        successes = data[data['Success'] == True]

        # Create a window with 2 graphs side-by-side (1 row, 2 columns)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # --- Graph 1: Time vs. Bit Length ---
        ax1.scatter(successes['Modulus Bit Length'], successes['Time Elapsed (ms)'], color='blue', s=60)
        ax1.plot(successes['Modulus Bit Length'], successes['Time Elapsed (ms)'], linestyle='--', color='blue', alpha=0.4)
        ax1.set_title('RSA Fermat Cracking: Time vs Key Size', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Key Bit Length', fontsize=10)
        ax1.set_ylabel('Time Elapsed (ms)', fontsize=10)
        ax1.grid(True, linestyle=':', alpha=0.7)

        # --- Graph 2: Time vs. Number of Rounds ---
        if 'Rounds' in successes.columns:
            ax2.scatter(successes['Rounds'], successes['Time Elapsed (ms)'], color='darkred', s=60)
            ax2.plot(successes['Rounds'], successes['Time Elapsed (ms)'], linestyle='--', color='darkred', alpha=0.4)
            ax2.set_title('RSA Fermat Cracking: Time vs Loops/Rounds', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Number of Fermat Rounds', fontsize=10)
            ax2.set_ylabel('Time Elapsed (ms)', fontsize=10)
            ax2.grid(True, linestyle=':', alpha=0.7)
        else:
            ax2.text(0.5, 0.5, "Column 'Rounds' not found in CSV.", 
                     fontsize=12, color='red', ha='center', va='center')
            ax2.set_title('RSA Fermat Cracking: Time vs Loops/Rounds')

        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No metrics file found. Run some cracks first!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_performance_graphs()