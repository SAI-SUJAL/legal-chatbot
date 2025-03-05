
# import os
# import faiss
# import numpy as np
# import pickle
# from sentence_transformers import SentenceTransformer
# import fitz  # PyMuPDF

# class VectorDatabase:
#     """
#     Manages vector-based document retrieval for legal research
#     """
#     def __init__(self, embedding_model="all-MiniLM-L6-v2", base_path=None):
#         """
#         Initialize vector database
        
#         Args:
#             embedding_model (str): Sentence transformer model name
#             base_path (str): Base path for saving/loading index and mappings
#         """
#         # Set base path for saving/loading
#         self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))
        
#         # Paths for index and mapping files
#         self.index_path = os.path.join(self.base_path, 'faiss_index.bin')
#         self.mapping_path = os.path.join(self.base_path, 'id_to_text.pkl')
        
#         # Initialize embedder
#         self.embedder = SentenceTransformer(embedding_model)
#         self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        
#         # Try to load existing index and mapping
#         self.index = self._load_index()
#         self.id_to_text = self._load_mapping()
    
#     def _load_index(self):
#         """
#         Load existing FAISS index or create a new one
        
#         Returns:
#             faiss.Index: FAISS index for vector search
#         """
#         try:
#             if os.path.exists(self.index_path):
#                 print("Loading existing FAISS index...")
#                 return faiss.read_index(self.index_path)
#             else:
#                 print("Creating new FAISS index...")
#                 return faiss.IndexFlatL2(self.embedding_dim)
#         except Exception as e:
#             print(f"Error loading index: {e}")
#             return faiss.IndexFlatL2(self.embedding_dim)
    
#     def _load_mapping(self):
#         """
#         Load existing text mapping or return empty dict
        
#         Returns:
#             dict: Mapping of document IDs to text
#         """
#         try:
#             if os.path.exists(self.mapping_path):
#                 print("Loading existing text mapping...")
#                 with open(self.mapping_path, 'rb') as f:
#                     return pickle.load(f)
#             else:
#                 print("Creating new text mapping...")
#                 return {}
#         except Exception as e:
#             print(f"Error loading mapping: {e}")
#             return {}
    
#     def _save_index(self):
#         """
#         Save FAISS index to file
#         """
#         try:
#             faiss.write_index(self.index, self.index_path)
#             print(f"FAISS index saved to {self.index_path}")
#         except Exception as e:
#             print(f"Error saving index: {e}")
    
#     def _save_mapping(self):
#         """
#         Save text mapping to file
#         """
#         try:
#             with open(self.mapping_path, 'wb') as f:
#                 pickle.dump(self.id_to_text, f)
#             print(f"Text mapping saved to {self.mapping_path}")
#         except Exception as e:
#             print(f"Error saving mapping: {e}")
    
#     def load_pdfs(self, pdf_paths):
#         """
#         Load and index PDF documents
        
#         Args:
#             pdf_paths (list): List of PDF file paths
#         """
#         # Start with current max doc_id if mapping exists
#         doc_id = max(self.id_to_text.keys()) + 1 if self.id_to_text else 0
        
#         for pdf_path in pdf_paths:
#             print(f"Processing PDF: {pdf_path}")
#             pages = self._extract_text_from_pdf(pdf_path)
            
#             for page_text in pages:
#                 # Create embedding
#                 embedding = self._normalize_vector(
#                     self.embedder.encode(page_text).astype(np.float32)
#                 )
                
#                 # Add to FAISS index
#                 self.index.add(embedding.reshape(1, -1))
#                 self.id_to_text[doc_id] = page_text
#                 doc_id += 1
        
#         # Save updated index and mapping
#         self._save_index()
#         self._save_mapping()
        
#         print(f"Indexed {len(self.id_to_text)} document sections")
    
#     def _normalize_vector(self, vec):
#         """
#         Normalize vector to unit length
        
#         Args:
#             vec (np.ndarray): Input vector
        
#         Returns:
#             np.ndarray: Normalized vector
#         """
#         return vec / np.linalg.norm(vec)
    
#     def _extract_text_from_pdf(self, pdf_path):
#         """
#         Extract text from PDF pages
        
#         Args:
#             pdf_path (str): Path to PDF file
        
#         Returns:
#             list: List of extracted text sections
#         """
#         doc = fitz.open(pdf_path)
#         extracted_text = []
        
#         for page_num in range(len(doc)):
#             text = doc[page_num].get_text("text").strip()
#             if text:
#                 extracted_text.append(f"Page {page_num + 1}: {text}")
        
#         return extracted_text
    
#     def search(self, query, top_k=5):
#         """
#         Search for relevant document sections
        
#         Args:
#             query (str): Search query
#             top_k (int): Number of top results to return
        
#         Returns:
#             list: Top matching document sections
#         """
#         # Create query embedding
#         query_embedding = self._normalize_vector(
#             self.embedder.encode(query).astype(np.float32)
#         )
        
#         # Perform search
#         distances, indices = self.index.search(
#             query_embedding.reshape(1, -1), 
#             top_k
#         )
        
#         # Retrieve matching texts
#         results = [
#             self.id_to_text[idx] 
#             for idx in indices[0] 
#             if idx in self.id_to_text
#         ]
        
#         return results

import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF

class VectorDatabase:
    """
    Manages vector-based document retrieval for legal research.
    Loads FAISS index if available, otherwise processes PDFs.
    """

    def __init__(self, embedding_model="all-MiniLM-L6-v2", base_path=None):
        """
        Initialize the vector database.

        Args:
            embedding_model (str): Sentence transformer model name.
            base_path (str): Base path for saving/loading index and mappings.
        """
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))

        # File paths for FAISS index and text mappings
        self.index_path = os.path.join(self.base_path, 'faiss_index.bin')
        self.mapping_path = os.path.join(self.base_path, 'id_to_text.pkl')

        # Initialize embedder
        self.embedder = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedder.get_sentence_embedding_dimension()

        # Load FAISS index and text mappings if they exist
        self.index = self._load_index()
        self.id_to_text = self._load_mapping()

    def _load_index(self):
        """ Load existing FAISS index or create a new one if not found. """
        if os.path.exists(self.index_path):
            print("✅ Loading existing FAISS index...")
            return faiss.read_index(self.index_path)
        print("⚡ No FAISS index found, creating a new one...")
        return faiss.IndexFlatL2(self.embedding_dim)

    def _load_mapping(self):
        """ Load existing text mappings or return an empty dictionary. """
        if os.path.exists(self.mapping_path):
            print("✅ Loading existing text mapping...")
            with open(self.mapping_path, 'rb') as f:
                return pickle.load(f)
        print("⚡ No text mapping found, creating a new one...")
        return {}

    def _save_index(self):
        """ Save FAISS index to file. """
        faiss.write_index(self.index, self.index_path)
        print(f"📌 FAISS index saved to {self.index_path}")

    def _save_mapping(self):
        """ Save text mapping to file. """
        with open(self.mapping_path, 'wb') as f:
            pickle.dump(self.id_to_text, f)
        print(f"📌 Text mapping saved to {self.mapping_path}")

    def load_pdfs(self, pdf_paths):
        """
        Load and index PDF documents. Only runs if FAISS index is empty.

        Args:
            pdf_paths (list): List of PDF file paths.
        """
        if self.index.ntotal > 0:
            print("✅ FAISS index already contains data. Skipping PDF loading.")
            return

        print("🚀 Processing PDFs and building FAISS index...")

        doc_id = max(self.id_to_text.keys(), default=-1) + 1
        all_texts = []

        for pdf_path in pdf_paths:
            print(f"📄 Processing PDF: {pdf_path}")
            pages = self._extract_text_from_pdf(pdf_path)
            all_texts.extend(pages)

        # Batch encode all text
        print("🔄 Encoding document embeddings...")
        embeddings = np.array(self.embedder.encode(all_texts, normalize_embeddings=True), dtype=np.float32)

        # Add to FAISS index in bulk
        self.index.add(embeddings)

        # Store text mappings
        for text in all_texts:
            self.id_to_text[doc_id] = text
            doc_id += 1

        # Save the updated index and mappings
        self._save_index()
        self._save_mapping()

        print(f"✅ Indexed {len(self.id_to_text)} document sections!")

    def _extract_text_from_pdf(self, pdf_path):
        """ Extract text from PDF pages. """
        doc = fitz.open(pdf_path)
        return [doc[page].get_text("text").strip() for page in range(len(doc)) if doc[page].get_text("text").strip()]

    def search(self, query, top_k=5):
        """
        Search for relevant document sections.

        Args:
            query (str): Search query.
            top_k (int): Number of top results to return.

        Returns:
            list: Top matching document sections.
        """
        query_embedding = np.array(self.embedder.encode(query, normalize_embeddings=True), dtype=np.float32)

        # Perform FAISS search
        distances, indices = self.index.search(query_embedding.reshape(1, -1), top_k)

        return [self.id_to_text[idx] for idx in indices[0] if idx in self.id_to_text]
