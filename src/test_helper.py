
from src.helper import file_processing

pdf_path = "static/docs/1706.03762v7.pdf"

question_docs, answer_docs = file_processing(pdf_path)

print("PDF processing successful!")

print("Question generation chunks:", len(question_docs))
print("Answer generation chunks:", len(answer_docs))

print("\nFirst extracted chunk:")
print(question_docs[0].page_content[:500])

