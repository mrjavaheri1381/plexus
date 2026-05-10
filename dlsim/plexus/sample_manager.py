import hashlib
from typing import List, Dict

from dlsim.core.peer_manager import PeerManager


class SampleManager:
    """
    The SampleManager class is responsible for deriving samples and determine who the aggregators in a particular
    sample are.
    """

    def __init__(self, peer_manager: PeerManager, sample_size: int, candidate_size: int, num_aggregators: int):
        self.peer_manager: PeerManager = peer_manager
        self.sample_size = sample_size
        self.candidate_size = candidate_size
        self.num_aggregators = num_aggregators
        self.sample_cache: Dict[int, List[bytes]] = {}
        self.graph = {}

    def create_graph(self, candidates: List[bytes], round: int, other_nodes_bws: Dict[bytes, int] = None,
                     other_nodes_computations: Dict[bytes, float] = None):
        """
        Create a graph representation of the candidates with their weights.
        """
        self.graph = {}
        for peer_pk in candidates:
            # Placeholder for node weights
            bandwidth = other_nodes_bws.get(peer_pk, 0) if other_nodes_bws else 0
            compute_power = other_nodes_computations.get(peer_pk, 0) if other_nodes_computations else 0
            last_participated = self.peer_manager.get_last_participated(peer_pk)
            distance_from_last = round - last_participated

            self.graph[peer_pk] = {
                "bandwidth": bandwidth,
                "compute_power": compute_power,
                "distance_from_last": distance_from_last,
                "data_similarity": 0  # Placeholder
            }

    def solve_selection_problem(self) -> List[bytes]:
        """
        Solve the selection problem based on the built graph.
        Currently returns the first sample_size candidates as a stub.
        """
        return list(self.graph.keys())[:self.sample_size]

    def get_ordered_sample_list(self, round: int, peers: List[bytes]) -> List[bytes]:
        peers = sorted(peers)
        hashes = []
        for peer_id in peers:
            h = hashlib.md5(b"%s-%d" % (peer_id, round))
            hashes.append((peer_id, h.digest()))
        hashes = sorted(hashes, key=lambda t: t[1])
        return [t[0] for t in hashes]
