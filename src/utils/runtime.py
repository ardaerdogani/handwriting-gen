from __future__ import annotations

import platform


def resolve_num_workers(num_workers: int, *, log_prefix: str) -> int:
    """Use single-process data loading on macOS to avoid worker hangs."""
    if num_workers > 0 and platform.system() == "Darwin":
        print(f"[{log_prefix}] For macOS, setting num_workers=0 to avoid DataLoader worker hangs.")
        return 0
    return num_workers
