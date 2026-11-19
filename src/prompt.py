prompt_template = """
You are an expert at creating technical interview and examination questions.

Based ONLY on the provided document, generate clear and relevant
questions that test the reader's understanding.

Requirements:
1. Generate at least 10 questions.
2. Cover all important concepts in the document.
3. Include conceptual and technical questions.
4. Each question must be a standalone question.
5. Do not provide answers.
6. Do not explain your question-generation process.
7. Do not write introductory or concluding paragraphs.

Document:
--------------
{text}
--------------

Return ONLY the numbered questions.
"""

refine_template = """
You are an expert at generating technical examination questions.

Existing questions:
{existing_answer}

Additional document context:
--------------
{text}
--------------

Instructions:
1. Refine the existing questions using the new context.
2. Add new questions if the context introduces important concepts.
3. Remove duplicate questions.
4. Keep every question clear and technically accurate.
5. Do not provide answers.
6. Do not describe your refinement process.
7. Do not include introductory or concluding paragraphs.

Return ONLY the complete numbered question list.
STRICT OUTPUT FORMAT:

1. Return only numbered questions.
2. Start directly with question number 1.
3. Do not include introductory sentences.
4. Do not include explanations or summaries.
5. Do not include blank question entries.
6. Every numbered entry must be a complete question.
7. Preserve all existing relevant questions.
8. Add new questions only when supported by the new context.
"""