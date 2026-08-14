import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
from typing import Optional, List, Dict, Any
import chromadb
from core.models.node import GraphNode
from core.memory.embedder import OllamaEmbedder

class HybridStore:
    """
    Abstrakcja bazy hybrydowej (Zastąpiłoby Neo4j + Milvus w produkcji).
    Obecnie symulowane jako in-memory dla łatwych testów architektury GraphMindOS.
    """
    def __init__(self, db_path: str = "./chroma_data"):
        self._nodes: Dict[str, GraphNode] = {}
        self.embedder = OllamaEmbedder()
        
        # Inicjalizacja ChromaDB (Pamięć Długotrwała)
        try:
            self.chroma_client = chromadb.PersistentClient(path=db_path)
            self.collection = self.chroma_client.get_or_create_collection(name="graphmind_nodes")
            self.chroma_active = True
            print("[STORE] ChromaDB Vector Backend Initialized.")
        except Exception as e:
            print(f"[STORE] Failed to initialize ChromaDB: {e}. Falling back to In-Memory only.")
            self.chroma_active = False
        
    def add_node(self, node: GraphNode):
        self._nodes[node.nodeId] = node
        
        # Węzły długotrwałe zapisujemy w Chroma jako pamięć RAG z wektorami
        if self.chroma_active and not node.entropy.is_ephemeral:
            # Tworzymy wektor jeśli węzeł ma jakiś semantyczny payload (np zawartość pliku)
            content_to_embed = node.execution.payload.get("text_content", "") if node.execution else ""
            
            # Wektoryzacja
            if content_to_embed and not node.vector:
                node.vector = self.embedder.get_embedding(content_to_embed)
                
            if node.vector:
                # Zamiana obj na string by weszło do chromy
                meta = {"kind": node.kind, "processor": node.execution.processor_ref or "none"}
                
                self.collection.add(
                    ids=[node.nodeId],
                    embeddings=[node.vector],
                    documents=[content_to_embed],
                    metadatas=[meta]
                )
                print(f"[STORE-RAG] Indexed semantic node {node.nodeId}")
        
        print(f"[STORE] Added node {node.nodeId} ({node.kind})")
        
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)
        
    def update_node(self, node: GraphNode):
        if node.nodeId in self._nodes:
            self._nodes[node.nodeId] = node
            
    def query_semantic(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Przeszukuje Prawą Półkulę (RAG) o najbardziej trafne węzły."""
        if not self.chroma_active:
             return []
             
        query_emb = self.embedder.get_embedding(query_text)
        if not query_emb:
            return []
            
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        
        # Zwracamy listę sformatowanych wyników
        matches = []
        if results and results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                matches.append({
                    "nodeId": results['ids'][0][i],
                    "document": results['documents'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else 0.0
                })
        return matches

    def remove_node(self, node_id: str):
        if node_id in self._nodes:
            # Jeżeli to wciąż RAM weź usuń, Chroma trzyma trwale dopóki explicit intent nie usunie
            # (można dodać też self.collection.delete, ale zazwyczaj efemeryczne i tak tam nie trafiają)
            del self._nodes[node_id]
            print(f"[STORE - ENTROPY] Node {node_id} removed (decayed).")

    def process_entropy(self):
        """
        System Garbage Collection uaktywniany np. co tick / zdarzenie.
        """
        nodes_to_remove = []
        for n_id, node in self._nodes.items():
            if node.entropy.is_ephemeral and node.entropy.decay_rate > 0:
                node.entropy.lifespan -= node.entropy.decay_rate
                if node.entropy.lifespan <= 0:
                    nodes_to_remove.append(n_id)
        
        for n_id in nodes_to_remove:
            self.remove_node(n_id)

