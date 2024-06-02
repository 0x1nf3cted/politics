# Business logic for collections
def calculate_similarity(embeddings):
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(embeddings)
