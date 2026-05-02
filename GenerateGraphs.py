import pandas as pd
import matplotlib.pyplot as plt

def create_performance_graphs():
    try:
        # Load the data we recorded
        data = pd.read_csv('cracking_metrics.csv')
        
        # Split data into successes and failures
        successes = data[data['Success'] == True]
        failures = data[data['Success'] == False]

        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(14, 10))

        # ROW 1: SUCCESSFUL CRACKS (BLUE DOTS)
        
        # --- Graph 1 (Top-Left): Success - Time vs Bit Length ---
        if not successes.empty:
            ax1.scatter(successes['Modulus Bit Length'], successes['Time Elapsed (ms)'], color='blue', s=60)
        ax1.set_title('SUCCESS: Time vs Key Size', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Key Bit Length', fontsize=10)
        ax1.set_ylabel('Time Elapsed (ms)', fontsize=10)
        ax1.grid(True, linestyle=':', alpha=0.7)

        # --- Graph 2 (Top-Center): Success - Time vs Rounds ---
        if 'Rounds' in data.columns:
            if not successes.empty:
                ax2.scatter(successes['Rounds'], successes['Time Elapsed (ms)'], color='blue', s=60)
            ax2.set_title('SUCCESS: Time vs Rounds', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Number of Fermat Rounds', fontsize=10)
            ax2.set_ylabel('Time Elapsed (ms)', fontsize=10)
            ax2.grid(True, linestyle=':', alpha=0.7)
        else:
            ax2.text(0.5, 0.5, "Column 'Rounds' not found.", color='red', ha='center', va='center')

        # --- Graph 3 (Top-Right): Success - Time vs Bit Length * Rounds ---
        if 'Rounds' in data.columns:
            if not successes.empty:
                ax3.scatter(successes['Modulus Bit Length'] * successes['Rounds'], successes['Time Elapsed (ms)'], color='blue', s=60)
            ax3.set_title('SUCCESS: Time vs Key Size * Rounds', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Key Bit Length * Number of Fermat Rounds', fontsize=10)
            ax3.set_ylabel('Time Elapsed (ms)', fontsize=10)
            ax3.grid(True, linestyle=':', alpha=0.7)
        else:
            ax3.text(0.5, 0.5, "Column 'Rounds' not found.", color='red', ha='center', va='center')

        # ROW 2: FAILED CRACKS (RED X's)

        # --- Graph 4 (Bottom-Left): Failure - Time vs Bit Length ---
        if not failures.empty:
            ax4.scatter(failures['Modulus Bit Length'], failures['Time Elapsed (ms)'], color='red', s=60, marker='x')
        ax4.set_title('FAILURE: Time vs Key Size', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Key Bit Length', fontsize=10)
        ax4.set_ylabel('Time Elapsed (ms)', fontsize=10)
        ax4.grid(True, linestyle=':', alpha=0.7)

        # --- Graph 5 (Bottom-Center): Failure - Time vs Rounds ---
        if 'Rounds' in data.columns:
            if not failures.empty:
                ax5.scatter(failures['Rounds'], failures['Time Elapsed (ms)'], color='red', s=60, marker='x')
            ax5.set_title('FAILURE: Time vs Rounds', fontsize=12, fontweight='bold')
            ax5.set_xlabel('Number of Fermat Rounds', fontsize=10)
            ax5.set_ylabel('Time Elapsed (ms)', fontsize=10)
            ax5.grid(True, linestyle=':', alpha=0.7)
        else:
            ax5.text(0.5, 0.5, "Column 'Rounds' not found.", color='red', ha='center', va='center')

        # --- Graph 6 (Bottom-Right): Failure - Time vs Bit Length * Rounds ---
        if 'Rounds' in data.columns:
            if not failures.empty:
                ax6.scatter(failures['Modulus Bit Length'] * failures['Rounds'], failures['Time Elapsed (ms)'], color='red', s=60, marker='x')
            ax6.set_title('FAILURE: Time vs Key Size * Rounds', fontsize=12, fontweight='bold')
            ax6.set_xlabel('Key Bit Length * Number of Fermat Rounds', fontsize=10)
            ax6.set_ylabel('Time Elapsed (ms)', fontsize=10)
            ax6.grid(True, linestyle=':', alpha=0.7)
        else:
            ax6.text(0.5, 0.5, "Column 'Rounds' not found.", color='red', ha='center', va='center')

        fig.suptitle('RSA Fermat Cracking Performance Metrics', fontsize=16, fontweight='bold')

        plt.tight_layout(pad=2.0, w_pad=2.0, h_pad=3.0)
        
        fig.subplots_adjust(top=0.92)

        plt.show()

    except FileNotFoundError:
        print("No metrics file found. Run some cracks first!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_performance_graphs()