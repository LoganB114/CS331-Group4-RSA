import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import time
import KeyGenerator
from FermatCracker import crack
from rsaKey import rsaKey
from MetricsManage import MetricsManage

class RSA_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Key Cracking Suite - CS 331")
        self.root.geometry("680x720") 

        # --- UI Styling  ---
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
        style.configure("TCheckbutton", font=("Segoe UI", 10))
        self.mono_font = ("Consolas", 10)
        self.output_bg = "#f4f6f9"

        # Create a Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # --- Initialize Tabs ---
        self.setup_generation_tab()
        self.setup_cipher_tab()
        self.setup_cracker_tab()

    def setup_generation_tab(self):
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text=" 1. Key Generation ")

        ttk.Label(gen_frame, text="Bit Length (max 4096):").pack(pady=(15, 2))
        self.bit_length_var = tk.StringVar(value="1024")
        ttk.Entry(gen_frame, textvariable=self.bit_length_var, font=self.mono_font).pack(pady=2)

        ttk.Label(gen_frame, text="Custom Prime p (Optional):").pack(pady=(10, 2))
        self.p_var = tk.StringVar()
        ttk.Entry(gen_frame, textvariable=self.p_var, width=60, font=self.mono_font).pack(pady=2)

        ttk.Label(gen_frame, text="Custom Prime q (Optional):").pack(pady=(10, 2))
        self.q_var = tk.StringVar()
        ttk.Entry(gen_frame, textvariable=self.q_var, width=60, font=self.mono_font).pack(pady=2)

        self.close_primes_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(gen_frame, text="Generate Close Primes (Overrides Custom Primes)", 
                        variable=self.close_primes_var).pack(pady=15)

        btn_frame = ttk.Frame(gen_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Generate RSA Keys", command=self.on_generate_keys).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save Keys to File", command=self.on_save_keys).pack(side="left", padx=5)
        
        # Output box set to disabled/read-only by default
        self.gen_output = tk.scrolledtext.ScrolledText(gen_frame, height=14, width=75, font=self.mono_font, 
                                  bg=self.output_bg, state=tk.DISABLED, wrap="word")
        self.gen_output.pack(pady=15, padx=10)


    def setup_cipher_tab(self):
        cipher_frame = ttk.Frame(self.notebook)
        self.notebook.add(cipher_frame, text=" 2. Encrypt / Decrypt ")

        ttk.Label(cipher_frame, text="Enter ASCII Message or Ciphertext:").pack(pady=(15, 5))
        self.message_input = tk.scrolledtext.ScrolledText(cipher_frame, height=6, width=75, font=self.mono_font, wrap="word")
        self.message_input.pack(pady=5, padx=10)

        btn_frame = ttk.Frame(cipher_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Encrypt", command=self.on_encrypt).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Decrypt", command=self.on_decrypt).pack(side="left", padx=5)
        
        ttk.Button(cipher_frame, text="Load Keys from File", command=self.on_load_keys).pack(pady=5)

        self.cipher_output = tk.scrolledtext.ScrolledText(cipher_frame, height=13, width=75, font=self.mono_font, 
                                     bg=self.output_bg, state=tk.DISABLED, wrap="word")
        self.cipher_output.pack(pady=15, padx=10)

    def setup_cracker_tab(self):
        crack_frame = ttk.Frame(self.notebook)
        self.notebook.add(crack_frame, text=" 3. Fermat Cracker ")

        ttk.Label(crack_frame, text="Target Public Modulus (n):").pack(pady=(15, 5))
        self.target_n_var = tk.StringVar()
        ttk.Entry(crack_frame, textvariable=self.target_n_var, width=70, font=self.mono_font).pack(pady=5)

        ttk.Label(crack_frame, text="Public Exponent (e):").pack(pady=(10, 5))
        self.target_e_var = tk.StringVar(value="65537")
        ttk.Entry(crack_frame, textvariable=self.target_e_var, width=70, font=self.mono_font).pack(pady=5)

        ttk.Label(crack_frame, text="Number of rounds:").pack(pady=(10, 5))
        self.rounds_var = tk.StringVar(value="100000")
        ttk.Entry(crack_frame, textvariable=self.rounds_var, width=70, font=self.mono_font).pack(pady=5)

        ttk.Button(crack_frame, text="Crack with Fermat's Method", command=self.on_crack).pack(pady=20)

        self.crack_output = tk.scrolledtext.ScrolledText(crack_frame, height=16, width=75, font=self.mono_font, 
                                    bg=self.output_bg, state=tk.DISABLED, wrap="word")
        self.crack_output.pack(pady=10, padx=10)

    # --- Integration Methods ---

    def on_generate_keys(self):
        try:
            bit_length = int(self.bit_length_var.get())
            if bit_length > 4096:
                messagebox.showwarning("Warning", "Bit length limited to 4096 per project scope.")
                return
                
            close_primes = self.close_primes_var.get()
            
            p_input = self.p_var.get().strip()
            q_input = self.q_var.get().strip()
            p = int(p_input) if p_input else None
            q = int(q_input) if q_input else None
            
            self.gen_output.config(state=tk.NORMAL)
            self.gen_output.delete("1.0", tk.END)
            self.gen_output.insert(tk.END, f"Generating keys... Please wait.\n")
            self.gen_output.config(state=tk.DISABLED) # Relock
            self.root.update()

            self.public_key, self.private_key = KeyGenerator.generate_keypair(
                bit_length, p=p, q=q, close_primes=close_primes
            )
            
            self.gen_output.config(state=tk.NORMAL)
            self.gen_output.delete("1.0", tk.END)
            self.gen_output.insert(tk.END, "--- KEY GENERATION SUCCESSFUL ---\n\n")
            self.gen_output.insert(tk.END, f"Modulus (n):\n{self.public_key.n}\n\n")
            self.gen_output.insert(tk.END, f"Public Exponent (e): {self.public_key.e}\n\n")
            self.gen_output.insert(tk.END, f"Private Key (d):\n{self.private_key.e}\n")
            self.gen_output.config(state=tk.DISABLED)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def on_save_keys(self):
        if not hasattr(self, 'public_key') or not hasattr(self, 'private_key'):
            messagebox.showerror("Error", "Please generate keys first!")
            return
        try:
            self.public_key.save_to_file("public_key.tsv")
            self.private_key.save_to_file("private_key.tsv")
            messagebox.showinfo("Success", "Keys saved to 'public_key.tsv' and 'private_key.tsv' in the current directory.")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred: {str(e)}")

    def on_load_keys(self):
        try:
            self.public_key = rsaKey.load_from_file("public_key.tsv")
            self.private_key = rsaKey.load_from_file("private_key.tsv")
            messagebox.showinfo("Success", "Keys successfully loaded from 'public_key.tsv' and 'private_key.tsv'!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Key files not found! Please generate and save keys first.")
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred: {str(e)}")

    def on_encrypt(self):
        message = self.message_input.get("1.0", tk.END).strip()
        
        self.cipher_output.config(state=tk.NORMAL)
        self.cipher_output.delete("1.0", tk.END)
        
        if not hasattr(self, 'public_key'):
            messagebox.showerror("Error", "Please generate or load RSA keys first!")
            self.cipher_output.config(state=tk.DISABLED)
            return
        try:
            encrypted_bytes = self.public_key.encrypt(message)
            encrypted_text = encrypted_bytes.decode('utf-8')
            self.cipher_output.insert(tk.END, "--- ENCRYPTED CIPHERTEXT (Base64) ---\n\n")
            self.cipher_output.insert(tk.END, encrypted_text)
        except Exception as e:
            messagebox.showerror("Encryption Error", f"An error occurred: {str(e)}")
            
        self.cipher_output.config(state=tk.DISABLED)

    def on_decrypt(self):
        ciphertext = self.message_input.get("1.0", tk.END).strip()
        
        self.cipher_output.config(state=tk.NORMAL)
        self.cipher_output.delete("1.0", tk.END)
        
        if not hasattr(self, 'private_key'):
            messagebox.showerror("Error", "Please generate or load RSA keys first!")
            self.cipher_output.config(state=tk.DISABLED)
            return
        try:
            decrypted_text = self.private_key.decrypt(ciphertext)
            self.cipher_output.insert(tk.END, "--- DECRYPTED PLAINTEXT ---\n\n")
            self.cipher_output.insert(tk.END, decrypted_text)
        except Exception as e:
            messagebox.showerror("Decryption Error", "Failed to decrypt. Ensure the input is valid Base64 ciphertext created by this key.")
            
        self.cipher_output.config(state=tk.DISABLED)

    def on_crack(self):
        try:
            target_n = int(self.target_n_var.get().strip())
            target_e = int(self.target_e_var.get().strip())
            rounds = int(self.rounds_var.get().strip())
            
            n_bit_length = target_n.bit_length()
            
            self.crack_output.config(state=tk.NORMAL)
            self.crack_output.delete("1.0", tk.END)
            self.crack_output.insert(tk.END, f"Attempting Fermat Factorization...\n")
            self.crack_output.config(state=tk.DISABLED)
            self.root.update()

            start_time = time.perf_counter_ns()
            cracked_key = crack(target_n, target_e, rounds)
            end_time = time.perf_counter_ns()
            elapsed_ms = (end_time - start_time) / 1_000_000 

            success = cracked_key is not None
            MetricsManage.log_crack_time(n_bit_length, elapsed_ms, success)

            self.crack_output.config(state=tk.NORMAL)
            if success:
                self.crack_output.insert(tk.END, f"\n--- CRACKED SUCCESSFULLY ---\n")
                self.crack_output.insert(tk.END, f"Time Elapsed: {elapsed_ms:.4f} ms\n\n")
                self.crack_output.insert(tk.END, f"Recovered Modulus (n):\n{cracked_key.n}\n\n")
                self.crack_output.insert(tk.END, f"Recovered Private Key (d):\n{cracked_key.e}\n") 
            else:
                self.crack_output.insert(tk.END, f"\nFailed to crack within round limit.\n")
                self.crack_output.insert(tk.END, f"Time Elapsed: {elapsed_ms:.4f} ms\n")
                self.crack_output.insert(tk.END, "Try generating a key with the 'Close Primes' box checked!\n")
            self.crack_output.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for both Modulus (n) and Exponent (e).")

if __name__ == "__main__":
    root = tk.Tk()
    app = RSA_GUI(root)
    root.mainloop()