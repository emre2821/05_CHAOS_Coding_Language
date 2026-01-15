"""
Run every .sn in artifacts/corpus_sn/ through the runtime.
"""
import glob
import os

from chaos_language import run_chaos, validate_chaos


def main():
    for path in glob.glob(os.path.join("artifacts", "corpus_sn", "*.sn")):
        with open(path, "r", encoding="utf-8") as handle:
            src = handle.read()
        try:
            validate_chaos(src)
            env = run_chaos(src)
            print(f"[OK] {path} -> keys={list(env.keys())}")
        except Exception as exc:
            print(f"[FAIL] {path} -> {exc}")


if __name__ == "__main__":
    main()
