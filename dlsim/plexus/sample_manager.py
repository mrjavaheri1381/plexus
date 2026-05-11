import hashlib
from typing import List, Dict

from dlsim.core.peer_manager import PeerManager


import networkx as nx

class SampleManager:
    """
    The SampleManager class is responsible for deriving samples and determine who the aggregators in a particular
    sample are.
    """

    def __init__(self, peer_manager: PeerManager, sample_size: int, num_aggregators: int, candidate_size: int = 40):
        self.peer_manager: PeerManager = peer_manager
        self.sample_size = sample_size
        self.num_aggregators = num_aggregators
        self.candidate_size = candidate_size
        self.sample_cache: Dict[int, List[bytes]] = {}
        self.candidates_graph: nx.Graph = None

    def get_ordered_sample_list(self, round: int, peers: List[bytes]) -> List[bytes]:
        peers = sorted(peers)
        hashes = []
        for peer_id in peers:
            h = hashlib.md5(b"%s-%d" % (peer_id, round))
            hashes.append((peer_id, h.digest()))
        hashes = sorted(hashes, key=lambda t: t[1])
        return [t[0] for t in hashes]

    def get_data_similarity_weight(self, peer1: bytes, peer2: bytes) -> float:
        """
        Placeholder function to compute data similarity weight between two peers.
        """
        return 1.0

    def build_candidates_graph(self, round_num: int, candidates: List[bytes], other_nodes_bws: Dict[bytes, int], other_nodes_compute: Dict[bytes, float]) -> None:
        """
        Builds a graph from the candidate peers. The nodes will have weights such as
        bandwidth, compute power, and difference from last participated round.
        Edges will have weights derived from get_data_similarity_weight.
        """
        G = nx.Graph()

        for peer_pk in candidates:
            bw = other_nodes_bws.get(peer_pk, 0)
            compute = other_nodes_compute.get(peer_pk, 0.0)
            last_participated = self.peer_manager.last_participated.get(peer_pk, 0)
            diff_participated = round_num - last_participated

            G.add_node(peer_pk, bw=bw, compute=compute, diff_participated=diff_participated)

        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                peer1 = candidates[i]
                peer2 = candidates[j]
                weight = self.get_data_similarity_weight(peer1, peer2)
                G.add_edge(peer1, peer2, weight=weight)

        self.candidates_graph = G

    def solve_candidates_graph(self) -> List[bytes]:
        """
        Solves a problem on the candidates graph and returns a final list of peers.
        This is a placeholder that simply returns the first `sample_size` nodes.
        """
        if not self.candidates_graph:
            return []

        return list(self.candidates_graph.nodes())[:self.sample_size]
