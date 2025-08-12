#!/usr/bin/env python3
"""
Simple test script for the FastAPI PDF Analyzer.
Tests the API with the sample PDF file.
"""

import requests
import os
from pathlib import Path

def test_api():
    """Test the API with the sample PDF."""
    
    
    # Test PDF upload
    pdf_path = Path(__file__).parent / "sample-pdf.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Sample PDF not found at {pdf_path}")
        return False
    
    print(f"📄 Testing with: {pdf_path.name}")
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'file': (pdf_path.name, pdf_file, 'application/pdf')}
            response = requests.post("http://localhost:8000/analyze-pdf", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF analysis successful!")
            print(f"📁 Filename: {result['filename']}")
            print(f"📊 Status: {result['status']}")
            print("📋 Extracted data:")
            print(result['extracted_fields'])
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing PDF Analyzer API...")
    print("=" * 40)
    
    success = test_api()
    
    print("=" * 40)
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("💥 Test failed!")
