"""Tests for agent-byzantine-fault-arbiter."""
import unittest
from agent_byzantine_fault_arbiter.arbiter import ByzantineFaultArbiter


class TestByzantineArbiter(unittest.TestCase):
    def setUp(self):
        self.arbiter = ByzantineFaultArbiter(total_nodes=4)

    def test_quorum_commit_with_isolated_byzantine(self):
        self.arbiter.record_vote(1, "node_1", "hash_A")
        self.arbiter.record_vote(1, "node_2", "hash_A")
        self.arbiter.record_vote(1, "node_3", "hash_FAULTY")
        res = self.arbiter.record_vote(1, "node_4", "hash_A")

        self.assertEqual(res["status"], "committed")
        self.assertEqual(res["canonical_hash"], "hash_A")
        self.assertIn("node_3", res["isolated_byzantine_nodes"])

    def test_isolated_node_rejected(self):
        self.arbiter._isolated_nodes.add("bad_node")
        res = self.arbiter.record_vote(1, "bad_node", "hash_X")
        self.assertEqual(res["status"], "rejected")
