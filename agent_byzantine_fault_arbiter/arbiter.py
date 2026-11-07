"""Core Byzantine Fault Arbiter implementation."""
from typing import Dict, List, Set, Any, Optional


class NodeVote:
    def __init__(self, node_id: str, round_num: int, value_hash: str):
        self.node_id = node_id
        self.round_num = round_num
        self.value_hash = value_hash


class ByzantineFaultArbiter:
    def __init__(self, total_nodes: int):
        self.total_nodes = total_nodes
        self.f = (total_nodes - 1) // 3  # Max tolerated faulty nodes
        self.quorum_threshold = 2 * self.f + 1
        self._votes: Dict[int, Dict[str, str]] = {}
        self._isolated_nodes: Set[str] = set()

    def record_vote(self, round_num: int, node_id: str, value_hash: str) -> Dict[str, Any]:
        if node_id in self._isolated_nodes:
            return {"status": "rejected", "reason": "node_isolated"}

        if round_num not in self._votes:
            self._votes[round_num] = {}

        self._votes[round_num][node_id] = value_hash

        # Evaluate consensus
        votes = self._votes[round_num]
        hash_counts: Dict[str, int] = {}
        for nid, vhash in votes.items():
            hash_counts[vhash] = hash_counts.get(vhash, 0) + 1

        for vhash, count in hash_counts.items():
            if count >= self.quorum_threshold:
                # Flag dissenting nodes as potentially Byzantine
                for nid, other_hash in votes.items():
                    if other_hash != vhash:
                        self._isolated_nodes.add(nid)

                return {
                    "status": "committed",
                    "round_num": round_num,
                    "canonical_hash": vhash,
                    "vote_count": count,
                    "isolated_byzantine_nodes": list(self._isolated_nodes)
                }

        return {
            "status": "pending_quorum",
            "current_votes": len(votes),
            "needed": self.quorum_threshold
        }

    def get_isolated_nodes(self) -> List[str]:
        return sorted(list(self._isolated_nodes))
