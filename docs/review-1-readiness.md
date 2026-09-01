# Review 1 Readiness

## Use these materials

- Presentation: `Review-1-A4-Portrait-Smart-Forest-Proposal.pptx`
- Project definition: `docs/project-specification.md`
- Dataset evidence: `docs/dataset-register.md`
- Preliminary result: `docs/fall-model-results.md`
- Live proof of concept: `python3 -m src.smart_forest.simulator`
- Verification: `python3 -m unittest discover -s tests -v`

Do not present `Review-1-Smart-Forest-Thesis.pptx`. It describes the earlier
hardware-heavy scope and is retained only as an archive.

## What is complete

- Literature review and explicit research gap
- Problem statement, aim, objectives and research questions
- Dataset-driven methodology and 22-week work plan
- Resource and cost plan for an individual software project
- Explainable Dynamic Threat Index baseline
- Downloaded and audited ranger-fall dataset
- Preliminary ranger-fall classifier comparison
- Working DTI scenarios and automated tests

## Evidence that may be stated in the review

- The ranger-fall data contains 1,428 supplied training records and 356 supplied
  test records.
- The selected preliminary Random Forest Lite baseline achieved 96.91% test
  accuracy, 98.69% fall recall and 96.49% F1-score.
- This result is preliminary and applies only to the supplied split.
- The dataset does not provide participant identifiers; therefore,
  subject-independent validation cannot be claimed.
- Acoustic and environmental models are planned work, not completed results.
- No physical IoT deployment, LoRa range, battery life or hardware energy result
  is claimed.

## Five-minute presentation flow

1. Explain that independent detectors do not prioritize combined emergencies.
2. Show the three evidence streams: acoustic, environmental and ranger safety.
3. State the contribution: confidence-aware, zone-aware Dynamic Threat Index.
4. Explain the dataset-to-model-to-virtual-event-to-DTI workflow.
5. Show the preliminary ranger-fall result as feasibility evidence.
6. Run the local DTI demonstration and explain the three threat levels produced.
7. Close with the 22-week plan, zero-cost software stack and expected outcomes.

## Likely viva questions

**Where is IoT if no hardware is used?**  The framework preserves IoT event
fields such as node, zone, timestamp, event type and confidence. Public records
are replayed as virtual node events so that fusion and prioritization can be
evaluated reproducibly. Physical deployment is future validation.

**What is novel?**  The individual classifiers are supporting modules. The main
contribution is the explainable cross-domain threat assessment and response
prioritization layer.

**Why not deploy online now?**  Review 1 assesses the proposal and feasibility.
The proof of concept runs locally; a local Streamlit dashboard is scheduled for
the integration stage. Online hosting is optional and is not a research result.

**Is 96.91% the final thesis accuracy?**  No. It is a preliminary result for the
ranger-fall module on the dataset's supplied test split. Final conclusions will
include all modules, DTI evaluation, robustness tests and limitations.

## Review 1 decision

Review 1 is ready. The next stage is to acquire and audit the acoustic and
environmental datasets, train their baseline models, and connect their outputs
to the existing virtual event and DTI pipeline.
