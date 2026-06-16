# backend/rag/test_pipeline.py
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from rag.pipeline import answer_query

test_questions = [
    "What are my rights as a tenant under RERA?",
    "How do I file a consumer complaint against a company?",
    "What is the minimum wage for workers in India?",
    "What protection does POCSO provide to children?",
    "How can I file an RTI application?",
]

for i, question in enumerate(test_questions):
    print(f"\n{'='*50}")
    print(f"Q: {question}")
    print("-" * 50)
    result = answer_query(question)
    print(f"A: {result['answer']}")
    print(f"\nSources: {result['sources']}")
    print(f"Category: {result['category']}")
    
    # Wait between questions to avoid rate limit
    if i < len(test_questions) - 1:
        print("\nWaiting 10 seconds before next question...")
        time.sleep(10)