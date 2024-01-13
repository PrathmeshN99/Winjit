def fun(user_query):
    import pdfplumber
    import re
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    def extract_text_from_document(file_path):
        try:
            with pdfplumber.open(file_path) as pdf_doc:
                text_content = []
                for page_num, page in enumerate(pdf_doc.pages, start=1):
                    text_content.append(page.extract_text())
            full_text = " ".join(text_content)
            return full_text
        except Exception as e:
            print(f"Error: {e}")
            return None

    document_text = extract_text_from_document('rbi_guidelines.pdf')

    # Load Sentence Transformer model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Function to generate embeddings for text sections
    def generate_embeddings(text_sections):
        try:
            embeddings = model.encode(text_sections)
            return embeddings
        except Exception as e:
            print(f"Error: {e}")
            return None

    sections = re.split(r'\nChapter [IVXLC]+\s?-.*\n', document_text)
    sections = list(filter(None, sections))
    embeddings = generate_embeddings(sections)

    # Function to calculate similarity scores
    def calculate_similarity(user_query_embedding, guideline_embeddings):
        try:
            similarities = cosine_similarity([user_query_embedding], guideline_embeddings)[0]
            return similarities
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Function to get the most relevant section
    def get_most_relevant_section(user_query, guideline_sections, guideline_embeddings):
        try:
            user_query_embedding = model.encode(user_query)
            similarities = calculate_similarity(user_query_embedding, guideline_embeddings)
            most_similar_index = np.argmax(similarities)
            most_relevant_section = guideline_sections[most_similar_index]
            return most_relevant_section
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Get the most relevant section for the provided query
    relevant_section = get_most_relevant_section(user_query, sections, embeddings)
    return relevant_section


# Example usage
user_query = "What is reversal of a loan?"
result = fun(user_query)
print("Most Relevant Section:\n", result)


# import json
# import sys

# def process_query(query):
#     # Process the query as needed
#     result = {"response": f"Received query: {query}", "status": "success"}
#     return result

# if __name__ == "__main__":
#     # Read the query from command-line arguments
#     query = sys.argv[1] if len(sys.argv) > 1 else None

#     # Process the query
#     response = process_query(query)
#     # Print the JSON response
#     print(json.dumps(response))
