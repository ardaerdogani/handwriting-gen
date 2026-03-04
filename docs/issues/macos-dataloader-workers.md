# Issue Draft: Classifier and DCGAN training can hang on macOS when `num_workers > 0`

## Summary

`src.train_classifier` and `src.train_dcgan` default to `--num-workers 2`, but `src.train_rnn` already forces `num_workers=0` on macOS to avoid `DataLoader` worker hangs. The same macOS guard is missing from the classifier and DCGAN entrypoints.

## Impact

- Training can stall or hang on macOS before or during the first epoch.
- The behavior is inconsistent across training scripts.
- Saved configs do not currently record the effective worker count when a fallback is applied.

## Reproduction

Run either command on macOS:

```bash
python -m src.train_classifier --data-dir data --out-dir runs/classifier
python -m src.train_dcgan --data-dir data --out-dir runs/dcgan
```

With PyTorch worker multiprocessing on macOS, these jobs may hang unless `--num-workers 0` is passed manually.

## Expected Behavior

All training entrypoints should behave consistently on macOS and automatically fall back to `num_workers=0`, while keeping the effective worker count visible in saved configs.

## Proposed Fix

- Add a shared runtime helper that resolves macOS-safe worker counts.
- Use it in `src.train_classifier`, `src.train_dcgan`, and `src.train_rnn`.
- Persist `effective_num_workers` in `config.json` and checkpoints.
