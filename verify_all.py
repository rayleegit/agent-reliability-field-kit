import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parent


def run(command: List[str], relative_directory: str) -> None:
    directory = ROOT / relative_directory
    print(f"\n$ {' '.join(command)}  # {relative_directory}", flush=True)
    subprocess.run(command, cwd=str(directory), check=True)


def main() -> None:
    node = shutil.which("node")
    if not node:
        raise SystemExit("Node.js is required for the identity-gateway tests")

    run([sys.executable, "run_demo.py"], "eval-lab")
    run([sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"], "eval-lab")
    run([node, "--test", "test/policy.test.mjs"], "identity-gateway")
    run([node, "demo.mjs"], "circle-agent-spend-guard")
    run([node, "--test", "test/policy.test.mjs"], "circle-agent-spend-guard")
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"],
        "codex-delivery-harness",
    )
    run([sys.executable, "scripts/verify.py"], "codex-delivery-harness")
    run([sys.executable, "run_demo.py"], "exa-grounded-research")
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"],
        "exa-grounded-research",
    )
    run([sys.executable, "run_demo.py"], "typed-decision-lab")
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"],
        "typed-decision-lab",
    )
    run([sys.executable, "run_demo.py"], "neo4j-graphrag-workshop")
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"],
        "neo4j-graphrag-workshop",
    )
    print("\nAll seven demos verified and every release gate succeeded.")


if __name__ == "__main__":
    main()
