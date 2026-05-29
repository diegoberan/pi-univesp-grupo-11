#!/usr/bin/env python3
import subprocess
import sys

files = [
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega do relatório final _ UNIVESP.pdf",
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega do vídeo _ UNIVESP.pdf",
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega da Avaliação Colaborativa _ UNIVESP.pdf",
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega do relatório final e do vídeo _ UNIVESP.pdf",
]

for i, f in enumerate(files, 1):
    print(f"\n{'='*80}")
    print(f"PDF {i}: {f.split('/')[-1]}")
    print(f"{'='*80}")
    try:
        # Try pdftotext
        result = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            print(result.stdout)
        else:
            print(f"pdftotext failed: {result.stderr}")
            # Try python with PyPDF2
            try:
                import PyPDF2
                with open(f, 'rb') as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            print(text)
            except ImportError:
                print("PyPDF2 not available, trying pdfminer...")
                try:
                    from pdfminer.high_level import extract_text
                    text = extract_text(f)
                    print(text)
                except ImportError:
                    print("No PDF extraction library available")
    except Exception as e:
        print(f"Error: {e}")
