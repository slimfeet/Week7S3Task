import tkinter as tk
from tkinter import filedialog, messagebox
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3UploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S3 Uploader")
        
        # Configure layout
        self.label = tk.Label(root, text="Select a file to upload:")
        self.label.pack(pady=10)
        
        self.upload_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.upload_button.pack(pady=5)
        
        self.upload_button = tk.Button(root, text="Upload to S3", command=self.upload_file)
        self.upload_button.pack(pady=5)
        
        self.file_path = None
        self.bucket_name = "week7skillsyncbucket"  # Replace with your bucket name

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {self.file_path}")

    def upload_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(self.file_path, self.bucket_name, self.file_path.split('/')[-1])
            messagebox.showinfo("Success", f"File {self.file_path} uploaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file was not found.")
        except NoCredentialsError:
            messagebox.showerror("Error", "Credentials not available.")
        except PartialCredentialsError:
            messagebox.showerror("Error", "Incomplete credentials provided.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = S3UploaderApp(root)
    root.mainloop()