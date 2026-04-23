import tkinter as tk
from tkinter import ttk, messagebox
import time
from rsaKey import KeyGenerator
from FermatCracker import crack

class RSA_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Key Cracking Suite - CS 331")
        self.root.geometry("650x550")

        # Create a Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # --- Initialize Tabs ---
        self.setup_generation_tab()
        self.setup_cipher_tab()
        self.setup_cracker_tab()

    def setup_generation_tab(self):
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text="1. Key Generation")

        ttk.Label(gen_frame, text="Bit Length (max 4096):").pack(pady=5)
        self.bit_length_var = tk.StringVar(value="1024")
        ttk.Entry(gen_frame, textvariable=self.bit_length_var).pack(pady=5)

        self.close_primes_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(gen_frame, text="Generate Close Primes (For Fermat Demo)", 
                        variable=self.close_primes_var).pack(pady=10)

        ttk.Button(gen_frame, text="Generate RSA Keys", command=self.on_generate_keys).pack(pady=10)
        
        self.gen_output = tk.Text(gen_frame, height=15, width=70)
        self.gen_output.pack(pady=10)

    def setup_cipher_tab(self):
        cipher_frame = ttk.Frame(self.notebook)
        self.notebook.add(cipher_frame, text="2. Encrypt / Decrypt")

        ttk.Label(cipher_frame, text="Enter ASCII Message or Ciphertext:").pack(pady=5)
        self.message_input = tk.Text(cipher_frame, height=5, width=70)
        self.message_input.pack(pady=5)

        btn_frame = ttk.Frame(cipher_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Encrypt", command=self.on_encrypt).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Decrypt", command=self.on_decrypt).pack(side="left", padx=5)

        self.cipher_output = tk.Text(cipher_frame, height=12, width=70)
        self.cipher_output.pack(pady=10)

    def setup_cracker_tab(self):
        crack_frame = ttk.Frame(self.notebook)
        self.notebook.add(crack_frame, text="3. Fermat Cracker")

        ttk.Label(crack_frame, text="Target Public Modulus (n):").pack(pady=5)
        self.target_n_var = tk.StringVar()
        ttk.Entry(crack_frame, textvariable=self.target_n_var, width=60).pack(pady=5)

        ttk.Button(crack_frame, text="Crack with Fermat's Method", command=self.on_crack).pack(pady=10)

        self.crack_output = tk.Text(crack_frame, height=15, width=70)
        self.crack_output.pack(pady=10)

    # --- Integration Methods ---

    def on_generate_keys(self):
        try:
            bit_length = int(self.bit_length_var.get())
            if bit_length > 4096:
                messagebox.showwarning("Warning", "Bit length limited to 4096 per project scope.")
                return
                
            close_primes = self.close_primes_var.get()
            
            self.gen_output.delete("1.0", tk.END)
            self.gen_output.insert(tk.END, f"Generating {bit_length}-bit keys...\n")
            self.gen_output.insert(tk.END, f"Close Primes flag: {close_primes}\n")
            self.gen_output.insert(tk.END, "Please wait, finding primes...\n\n")
            self.root.update() # Force GUI to update before the math locks the thread

            # Call Calvin's backend code
            generated_key = KeyGenerator.generate_keypair(bit_length, close_primes)
            
            # Display the returned data
            key_data = generated_key.to_dict()
            self.gen_output.insert(tk.END, "--- KEY GENERATION SUCCESSFUL ---\n\n")
            self.gen_output.insert(tk.END, f"Modulus (n):\n{key_data['n']}\n\n")
            self.gen_output.insert(tk.END, f"Public Exponent (e): {key_data['e']}\n\n")
            self.gen_output.insert(tk.END, f"Private Key (d):\n{key_data['d']}\n")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for bit length.")

    def on_encrypt(self):
        message = self.message_input.get("1.0", tk.END).strip()
        self.cipher_output.delete("1.0", tk.END)
        self.cipher_output.insert(tk.END, "Notice for Team:\nRSACipher backend not yet implemented in rsaKey.py.\n")
        self.cipher_output.insert(tk.END, "Once RSACipher is written, connect it in the 'on_encrypt' function of the GUI.")

    def on_decrypt(self):
        ciphertext = self.message_input.get("1.0", tk.END).strip()
        self.cipher_output.delete("1.0", tk.END)
        self.cipher_output.insert(tk.END, "Notice for Team:\nRSACipher backend not yet implemented in rsaKey.py.\n")
        self.cipher_output.insert(tk.END, "Once RSACipher is written, connect it in the 'on_decrypt' function of the GUI.")

    def on_crack(self):
        try:
            target_n = int(self.target_n_var.get().strip())
            
            self.crack_output.delete("1.0", tk.END)
            self.crack_output.insert(tk.END, f"Attempting Fermat Factorization...\n")
            self.root.update()

            # Start timer
            start_time = time.perf_counter_ns()
            
            # Call Logan's backend code
            cracked_key = crack(target_n)
            
            # End timer
            end_time = time.perf_counter_ns()
            elapsed_ms = (end_time - start_time) / 1_000_000 # Convert nanoseconds to milliseconds

            if cracked_key:
                self.crack_output.insert(tk.END, f"\n--- CRACKED SUCCESSFULLY ---\n")
                self.crack_output.insert(tk.END, f"Time Elapsed: {elapsed_ms:.4f} ms\n\n")
                self.crack_output.insert(tk.END, f"Found p: {cracked_key.p}\n\n")
                self.crack_output.insert(tk.END, f"Found q: {cracked_key.q}\n\n")
                self.crack_output.insert(tk.END, f"Recovered Private Key (d):\n{cracked_key.d}\n")
            else:
                self.crack_output.insert(tk.END, f"\nFailed to crack within round limit.\n")
                self.crack_output.insert(tk.END, f"Time Elapsed: {elapsed_ms:.4f} ms\n")
                self.crack_output.insert(tk.END, "Try generating a key with the 'Close Primes' box checked!\n")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the Modulus (n).")

if __name__ == "__main__":
    root = tk.Tk()
    app = RSA_GUI(root)
    root.mainloop()