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
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"],
        "codex-delivery-harness",
    )
    run([sys.executable, "scripts/verify.py"], "codex-delivery-harness")
    print("\nAll demos verified: 13 tests passed and both release gates succeeded.")


if __name__ == "__main__":
    main()
