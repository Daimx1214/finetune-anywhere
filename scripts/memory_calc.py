"""Estimate memory, not hardware compatibility or speed. All units are decimal GB."""

import argparse


def estimate(params, bits, context, layers=28, kv_heads=4, head_dim=128, batch=1):
    weights = params * {4: 0.55, 8: 1, 16: 2}[bits]
    kv = 2 * layers * kv_heads * head_dim * context * batch * 2 / 1e9
    overhead = 1.5
    return weights, kv, overhead


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--params", type=float, required=True, help="billions of parameters")
    p.add_argument("--bits", type=int, choices=[4, 8, 16], default=4)
    p.add_argument("--context", type=int, default=4096)
    p.add_argument("--layers", type=int, default=28)
    p.add_argument("--kv-heads", type=int, default=4)
    p.add_argument("--head-dim", type=int, default=128)
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--train", action="store_true")
    a = p.parse_args()
    if any(
        getattr(a, name) <= 0 for name in ["params", "context", "layers", "kv_heads", "head_dim", "batch"]
    ):
        p.error("sizes, dimensions and batch must be positive")
    w, kv, overhead = estimate(a.params, a.bits, a.context, a.layers, a.kv_heads, a.head_dim, a.batch)
    print(f"Weights: {w:.2f} GB (parameters × bytes: 16-bit=2, 8-bit=1, 4-bit≈0.55)")
    print(
        f"KV cache: {kv:.2f} GB (2 × {a.layers} layers × {a.kv_heads} KV heads × "
        f"{a.head_dim} head dimension × {a.context} tokens × {a.batch} batch × 2 bytes)"
    )
    total = w + kv + overhead
    print(f"Runtime allowance: {overhead:.2f} GB. Inference total: {total:.2f} GB.")
    print("KV uses FP16. Replace architecture defaults with your model config. OS needs extra memory.")
    if a.train:
        # Explicit budgeting heuristic, not an activation estimator.
        adapter = a.params * 0.01 * 16
        activation = 2 * a.context / 2048 * a.batch
        print(
            "Training heuristic: 1% trainable parameters at 16 bytes each, plus "
            "2 GB activations per 2048 tokens per microbatch and 1.5 GB runtime."
        )
        print(
            f"LoRA: {a.params * 2 + adapter + activation + overhead:.2f} GB; "
            f"QLoRA: {a.params * 0.55 + adapter + activation + overhead:.2f} GB."
        )
        print("Training excludes KV cache; actual activations depend on checkpointing and kernels.")
    for ram in [8, 16, 32]:
        verdict = "likely fits inference" if total <= ram * 0.7 else "tight or too large; reduce size/context"
        print(f"{ram} GB machine: {verdict} (reserve 30% for OS/apps).")
    print("Estimates only. GPU VRAM and system RAM are separate on discrete GPUs.")


if __name__ == "__main__":
    main()
