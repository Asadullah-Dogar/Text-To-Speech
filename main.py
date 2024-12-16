import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfReader
from google.cloud import texttospeech


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def text_to_speech(text, output_file, audio_format):
    """Converts text to speech using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()

    # Set up the input text
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio output format
    audio_encoding = texttospeech.AudioEncoding.MP3 if audio_format == "MP3" else texttospeech.AudioEncoding.LINEAR16
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    # Perform text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to '{output_file}'")


def main_ui():
    def select_pdf():
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            pdf_path_entry.delete(0, tk.END)
            pdf_path_entry.insert(0, file_path)

    def generate_audio():
        pdf_path = pdf_path_entry.get()
        output_file = output_file_entry.get()
        audio_format = format_var.get()

        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("Error", "PDF file not found. Please select a valid file.")
            return

        if not output_file:
            messagebox.showerror("Error", "Please provide a name for the output audio file.")
            return

        if not output_file.endswith(f".{audio_format.lower()}"):
            output_file += f".{audio_format.lower()}"

        try:
            messagebox.showinfo("Processing", "Extracting text from PDF...")
            text = extract_text_from_pdf(pdf_path)

            if not text.strip():
                messagebox.showerror("Error", "No text found in the PDF!")
                return

            messagebox.showinfo("Processing", "Converting text to speech...")
            text_to_speech(text, output_file, audio_format)

            messagebox.showinfo("Success", f"Audio file saved as {output_file}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the main window
    root = tk.Tk()
    root.title("PDF to Audiobook Converter")

    # Styling options
    root.geometry("800x600")
    root.state("zoomed")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 14), padding=10)
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("Header.TLabel", font=("Helvetica", 20, "bold"), foreground="#4CAF50")

    # Header
    header_frame = ttk.Frame(root, padding=20)
    header_frame.pack(fill="x")
    ttk.Label(header_frame, text="PDF to Audiobook Converter", style="Header.TLabel").pack()

    # Main Frame
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True, fill="both")

    ttk.Label(main_frame, text="Select PDF File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    pdf_path_entry = ttk.Entry(main_frame, width=50)
    pdf_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    ttk.Button(main_frame, text="Browse", command=select_pdf).grid(row=0, column=2, padx=10, pady=10)

    ttk.Label(main_frame, text="Output Audio File:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    output_file_entry = ttk.Entry(main_frame, width=50)
    output_file_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ttk.Label(main_frame, text="Select Format:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    format_var = tk.StringVar(value="MP3")
    format_menu = ttk.OptionMenu(main_frame, format_var, "MP3", "MP3", "WAV")
    format_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ttk.Button(main_frame, text="Convert to Audiobook", command=generate_audio).grid(row=3, column=0, columnspan=3,
                                                                                     pady=20)

    # Footer
    footer = ttk.Label(root, text="Powered by Google Text-to-Speech API", font=("Helvetica", 10))
    footer.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_ui()
