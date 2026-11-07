"""CLI for agent-byzantine-fault-arbiter."""
import sys
import argparse
from .arbiter import ByzantineFaultArbiter


def main():
    parser = argparse.ArgumentParser(description="Agent Byzantine Fault Arbiter")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        arbiter = ByzantineFaultArbiter(total_nodes=4)
        print(f"BFT initialized: Total Nodes=4, Max Faulty Nodes (f)={arbiter.f}, Quorum={arbiter.quorum_threshold}")
        arbiter.record_vote(1, "node_1", "hash_valid")
        arbiter.record_vote(1, "node_2", "hash_valid")
        arbiter.record_vote(1, "node_3", "hash_rogue")  # Hallucinated vote
        res = arbiter.record_vote(1, "node_4", "hash_valid")
        print(f"Consensus Result: {res}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
