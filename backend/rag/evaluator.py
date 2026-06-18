# backend/rag/evaluator.py
import sys, os, json, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from rag.retriever import retrieve, rerank
from rag.pipeline import answer_query
from sentence_transformers import SentenceTransformer, util

embedder = SentenceTransformer("all-MiniLM-L6-v2")

TEST_CASES = [
    # Housing Laws (5)
    {
        "question": "What are the rights of an allottee under RERA?",
        "ground_truth": "Under RERA allottees have right to information about project, right to possession, right to refund with interest if developer fails to deliver, and right to necessary documents after possession.",
        "expected_category": "housing_laws"
    },
    {
        "question": "What protection does RERA provide to homebuyers?",
        "ground_truth": "RERA protects homebuyers by requiring promoters to register projects, maintain separate accounts, provide stage wise completion schedule and give possession on time.",
        "expected_category": "housing_laws"
    },
    {
        "question": "What are tenant obligations under tenancy law?",
        "ground_truth": "Under tenancy law a tenant cannot deny the landlord title to the property during continuance of tenancy and must maintain property properly.",
        "expected_category": "housing_laws"
    },
    {
        "question": "What happens if a promoter fails to give possession under RERA?",
        "ground_truth": "If a promoter fails to give possession under RERA the allottee is entitled to claim refund of amount paid with interest at prescribed rate or compensation as provided under the Act.",
        "expected_category": "housing_laws"
    },
    {
        "question": "What documents must a promoter provide to allottee under RERA?",
        "ground_truth": "Under RERA a promoter must provide allottee with all necessary documents and plans including those of common areas after physical possession has been handed over.",
        "expected_category": "housing_laws"
    },

    # Consumer Laws (4)
    {
        "question": "How can a consumer file a complaint against a company?",
        "ground_truth": "A consumer can file a complaint before the District Commission, State Commission or National Commission depending on value of goods or services and nature of defect or deficiency.",
        "expected_category": "consumer_laws"
    },
    {
        "question": "What is a consumer dispute under Consumer Protection Act?",
        "ground_truth": "A consumer dispute means a dispute where the person against whom a complaint has been made denies or disputes the allegations in the complaint regarding defective goods or deficient services.",
        "expected_category": "consumer_laws"
    },
    {
        "question": "What are unfair trade practices under Consumer Protection Act?",
        "ground_truth": "Unfair trade practices include false representation of goods or services, misleading advertisements, deceptive practices in sale and provision of unsafe goods under Consumer Protection Act 2019.",
        "expected_category": "consumer_laws"
    },
    {
        "question": "What is the role of Central Authority under Consumer Protection Act?",
        "ground_truth": "The Central Authority under Consumer Protection Act 2019 protects consumer rights, prevents unfair trade practices and false advertisements and can investigate complaints and impose penalties.",
        "expected_category": "consumer_laws"
    },

    # Labour Laws (4)
    {
        "question": "What is the minimum wage structure under the Minimum Wages Act?",
        "ground_truth": "Under Minimum Wages Act 1948 the minimum rate of wages may consist of basic rate of wages and special allowance. The appropriate government fixes minimum rates for scheduled employments.",
        "expected_category": "labour_laws"
    },
    {
        "question": "What are the provisions for EPF contribution?",
        "ground_truth": "Under EPF Act 1952 both employer and employee contribute to provident fund. Employer must deposit contributions within prescribed time and maintain proper accounts.",
        "expected_category": "labour_laws"
    },
    {
        "question": "What are worker rights under labour laws?",
        "ground_truth": "Workers have right to receive minimum wages, right to safe working conditions, right to EPF contributions from employer, and right to file complaints against violations.",
        "expected_category": "labour_laws"
    },
    {
        "question": "What protection does POSH Act provide to women at workplace?",
        "ground_truth": "POSH Act 2013 protects women from sexual harassment at workplace by requiring employers to constitute internal complaints committee and provide safe working environment.",
        "expected_category": "labour_laws"
    },

    # Criminal Laws (4)
    {
        "question": "What offences does the POCSO Act cover?",
        "ground_truth": "POCSO Act 2012 covers offences of sexual assault, sexual harassment and pornography against children and provides for special courts for trial of such offences.",
        "expected_category": "criminal_laws"
    },
    {
        "question": "What are the key provisions of BNS 2023?",
        "ground_truth": "Bharatiya Nyaya Sanhita 2023 replaced Indian Penal Code and provides updated definitions and punishments for criminal offences including murder, theft, assault and other crimes.",
        "expected_category": "criminal_laws"
    },
    {
        "question": "What does BNSS 2023 replace and what does it cover?",
        "ground_truth": "BNSS 2023 replaced Code of Criminal Procedure and governs the procedure for investigation, inquiry and trial of criminal offences in India.",
        "expected_category": "criminal_laws"
    },
    {
        "question": "What is the Bharatiya Sakshya Adhiniyam about?",
        "ground_truth": "Bharatiya Sakshya Adhiniyam 2023 replaced Indian Evidence Act and provides rules for admissibility of evidence including documentary evidence, electronic records and witness testimony.",
        "expected_category": "criminal_laws"
    },

    # Cyber Laws (2)
    {
        "question": "What are the penalties under IT Act for hacking?",
        "ground_truth": "Under Information Technology Act 2000 unauthorized access and hacking are punishable offences with imprisonment and fines depending on nature and severity of the cybercrime.",
        "expected_category": "cyber_laws"
    },
    {
        "question": "What does the IT Act say about electronic records?",
        "ground_truth": "IT Act 2000 recognizes electronic records and digital signatures as legally valid. Electronic records are admissible as evidence and have same legal effect as paper records.",
        "expected_category": "cyber_laws"
    },

    # Central Laws (2)
    {
        "question": "What is RTI and how to apply?",
        "ground_truth": "RTI is Right to Information Act 2005 which allows citizens to request information from public authorities by applying to the Public Information Officer with prescribed fee.",
        "expected_category": "central_laws"
    },
    {
        "question": "Who is a Public Information Officer under RTI Act?",
        "ground_truth": "A Public Information Officer under RTI Act 2005 is an officer designated by each public authority to receive and process applications for information from citizens.",
        "expected_category": "central_laws"
    },

    # Personal Laws (2)
    {
        "question": "What does Hindu Succession Act say about inheritance?",
        "ground_truth": "Hindu Succession Act 1956 governs inheritance and succession among Hindus. It provides equal rights to daughters in ancestral property and specifies heirs in different classes.",
        "expected_category": "personal_laws"
    },
    {
        "question": "What are the rights of legal heirs under succession law?",
        "ground_truth": "Under Hindu Succession Act legal heirs have right to inherit property of deceased. Class I heirs have first priority and include spouse, children and mother of deceased.",
        "expected_category": "personal_laws"
    },

    # Mixed/Cross-category (2)
    {
        "question": "What legal recourse does a victim of workplace harassment have?",
        "ground_truth": "A victim of workplace harassment can file complaint with Internal Complaints Committee under POSH Act, approach labour commissioner, or file criminal complaint under BNS for relevant offences.",
        "expected_category": "labour_laws"
    },
    {
        "question": "What are the rights of a person arrested under BNSS?",
        "ground_truth": "Under BNSS 2023 an arrested person has right to be informed of grounds of arrest, right to legal representation, right to be produced before magistrate within 24 hours and right to bail in bailable offences.",
        "expected_category": "criminal_laws"
    }
]

def compute_relevancy(answer: str, ground_truth: str) -> float:
    """Semantic similarity between answer and ground truth"""
    emb1 = embedder.encode(answer, convert_to_tensor=True)
    emb2 = embedder.encode(ground_truth, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()
    return round(score, 4)

def compute_retrieval_accuracy(question: str, expected_category: str) -> float:
    """Check if top retrieved chunks are from expected category"""
    retrieved = retrieve(question, top_k=5)
    correct = sum(1 for r in retrieved if r["metadata"]["category"] == expected_category)
    return round(correct / len(retrieved), 4)

def run_evaluation():
    print("=" * 60)
    print("NYAY AI — Custom RAG Evaluation")
    print("=" * 60)
    print(f"\nEvaluating {len(TEST_CASES)} test questions...\n")

    results = []
    total_relevancy = 0
    total_retrieval = 0
    errors = 0

    for i, tc in enumerate(TEST_CASES):
        print(f"[{i+1}/{len(TEST_CASES)}] {tc['question'][:55]}...")
        try:
            start = time.time()
            result = answer_query(tc["question"])
            latency = round(time.time() - start, 2)

            relevancy = compute_relevancy(result["answer"], tc["ground_truth"])
            retrieval_acc = compute_retrieval_accuracy(tc["question"], tc["expected_category"])
            category_correct = result["category"] == tc["expected_category"]

            total_relevancy += relevancy
            total_retrieval += retrieval_acc

            results.append({
                "question": tc["question"],
                "answer_preview": result["answer"][:150] + "...",
                "answer_relevancy": relevancy,
                "retrieval_accuracy": retrieval_acc,
                "category_correct": category_correct,
                "latency_seconds": latency,
                "sources": result["sources"]
            })

            print(f"  Relevancy: {relevancy:.3f} | Retrieval: {retrieval_acc:.3f} | Latency: {latency}s")
            time.sleep(3)  # avoid rate limiting

        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    successful = len(TEST_CASES) - errors
    avg_relevancy = round(total_relevancy / successful, 4) if successful > 0 else 0
    avg_retrieval = round(total_retrieval / successful, 4) if successful > 0 else 0

    print("\n" + "=" * 60)
    print("FINAL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Questions evaluated:     {successful}/{len(TEST_CASES)}")
    print(f"Avg Answer Relevancy:    {avg_relevancy:.4f} ({avg_relevancy*100:.1f}%)")
    print(f"Avg Retrieval Accuracy:  {avg_retrieval:.4f} ({avg_retrieval*100:.1f}%)")
    print("=" * 60)

    # Save results
    output = {
        "summary": {
            "total_questions": len(TEST_CASES),
            "successful": successful,
            "avg_answer_relevancy": avg_relevancy,
            "avg_retrieval_accuracy": avg_retrieval,
            "model": "llama-3.1-8b-instant via Groq",
            "embedding_model": "all-MiniLM-L6-v2",
            "reranker": "Cohere rerank-english-v3.0",
            "vector_store": "FAISS IndexFlatIP",
            "total_indexed_chunks": 6324
        },
        "per_question_results": results
    }

    with open("rag/evaluation_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDetailed results saved to rag/evaluation_results.json")
    return output

if __name__ == "__main__":
    run_evaluation()