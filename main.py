import io
import os
import uvicorn
import PyPDF2
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key=os.getenv('OPENAI_API_KEY')
)


@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and extract structured data using LLMs
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read PDF content
        pdf_content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
        # Extract text from all pages
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No text content found in PDF")
        
        # Analyze with OpenAI
        response = client.chat.completions.create(
            model=os.getenv('MODEL_NAME'),
            messages=[
                {
                    "role": "system", 
                    "content": "You are a document analyzer. Extract key information from the provided text and return it as structured JSON with fields like: name, email, phone, company, date, amount, description, etc. Only include fields that are clearly present in the text."
                },
                {
                    "role": "user", 
                    "content": f"Analyze this document and extract structured information:\n\n{text_content[:4000]}"
                }
            ],
            temperature=0.1
        )
        
        extracted_data = response.choices[0].message.content
        
        return JSONResponse(content={
            "filename": file.filename,
            "extracted_fields": extracted_data,
            "status": "success"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
