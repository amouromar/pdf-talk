from flask import Flask, request, render_template, send_file
import pdfplumber
from gtts import gTTS
import os

app = Flask(__name__)


def pdf_to_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def text_to_audio(text, audio_path):
    if text.strip():  # Check if the text is not empty or only contains whitespace
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)
        return True
    return False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf_file = request.files["pdf"]
        if pdf_file:
            pdf_path = os.path.join("uploads", pdf_file.filename)

            # Remove existing file if it exists
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

            pdf_file.save(pdf_path)
            audio_path = os.path.join("uploads", "output.mp3")
            text = pdf_to_text(pdf_path)
            if text_to_audio(text, audio_path):
                return send_file(audio_path, as_attachment=True)
            else:
                return "Error: No text found in the PDF file."
    return render_template("index.html")


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
