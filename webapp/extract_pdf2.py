import zlib
import re
import sys

files = [
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega do relatório final _ UNIVESP.pdf",
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega do vídeo _ UNIVESP.pdf",
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega da Avaliação Colaborativa _ UNIVESP.pdf",
    "/mnt/c/Users/diego/OneDrive/Desktop/projeto merda univesp/DRP04-Projeto Integrador em Computação I-Turma 004_ Q7 - Entrega do relatório final e do vídeo _ UNIVESP.pdf",
]

for idx, filepath in enumerate(files, 1):
    print(f"\n{'='*80}")
    print(f"PDF {idx}: {filepath.split('/')[-1]}")
    print(f"{'='*80}")
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # Find all FlateDecode streams and decompress them
        # Pattern: stream\r?\n...endstream
        stream_pattern = rb'stream\r?\n(.*?)\r?\nendstream'
        streams = re.findall(stream_pattern, data, re.DOTALL)
        
        all_text = []
        for i, stream_data in enumerate(streams):
            try:
                decompressed = zlib.decompress(stream_data)
                # Try to decode as UTF-8 or latin-1
                try:
                    text = decompressed.decode('utf-8', errors='ignore')
                except:
                    text = decompressed.decode('latin-1', errors='ignore')
                
                # Look for text operators in PDF: Tj, TJ, ', "
                # Extract text between parentheses from Tj operators
                text_ops = re.findall(r'\((.*?)\)\s*Tj', text)
                text_ops2 = re.findall(r'\[(.*?)\]\s*TJ', text)
                
                if text_ops or text_ops2:
                    print(f"\n--- Stream {i} (text content) ---")
                    for t in text_ops:
                        cleaned = t.replace('\\n', '\n').replace('\\r', '\r').replace('\\(', '(').replace('\\)', ')')
                        print(cleaned, end='')
                    
                    for tj_array in text_ops2:
                        # TJ arrays contain strings and kerning values
                        parts = re.findall(r'\((.*?)\)', tj_array)
                        for p in parts:
                            cleaned = p.replace('\\n', '\n').replace('\\r', '\r')
                            print(cleaned, end='')
                    print()
                    
            except zlib.error:
                # Not a compressed stream, try as raw text
                try:
                    text = stream_data.decode('utf-8', errors='ignore')
                    text_ops = re.findall(r'\((.*?)\)\s*Tj', text)
                    if text_ops:
                        print(f"\n--- Stream {i} (raw text) ---")
                        for t in text_ops:
                            print(t)
                except:
                    pass
            except Exception as e:
                pass
                
    except Exception as e:
        print(f"Error reading file: {e}")
