# Smart Forest Dynamic Threat Assessment

Software-only M.Tech thesis prototype using public datasets as virtual IoT sensor inputs.

## Reduced scope

The project models three evidence streams:

1. acoustic threat: background, gunshot, chainsaw;
2. environmental threat: normal versus fire risk;
3. ranger safety: normal activity versus fall/distress.

Their classifier outputs are converted into virtual IoT events and fused into an
explainable 0–100 Dynamic Threat Index (DTI). No physical sensor deployment is
claimed.

## Repository layout

```text
config/          DTI and virtual-zone configuration
data/raw/        downloaded datasets (not committed)
data/processed/  cleaned model-ready data (not committed)
docs/            project specification and dataset register
models/          trained model files (not committed)
notebooks/       exploratory and model-development notebooks
results/         generated experiment outputs
src/smart_forest core Python package
tests/           automated tests
```

## Run the current prototype

```bash
python3 -m src.smart_forest.simulator
python3 -m unittest discover -s tests -v
```

Train and compare the fall models with the bundled compatible Python runtime:

```bash
python3 scripts/train_fall_models.py
```

The training script selects a model using an internal validation split of
`Train.csv`, refits each candidate on all training records, and evaluates once
on the untouched supplied `Test.csv`.

The simulator currently demonstrates the DTI rules with synthetic classifier
outputs. It does not fabricate model accuracy or experimental results.

## Next milestone

Select and audit suitable public datasets for acoustic and environmental risk,
then connect all three classifier outputs to the virtual event simulator.

Review 1 presentation guidance and claim boundaries are recorded in
`docs/review-1-readiness.md`.
