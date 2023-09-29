from fastapi import FastAPI, UploadFile, File, HTTPException
import PyPDF2
from transformers import BartForConditionalGeneration, BartTokenizer
import torch

app = FastAPI()

# Load the model and tokenizer for summarization.
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # if file.filename.split('.')[-1] != "pdf":
    #     raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # Extract text from PDF
    pdf_content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    # Summarize the extracted text
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs.input_ids, num_beams=4, min_length=30, max_length=1024, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return {"summary": summary}

# Additional necessary imports
import io

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)