# Dataset Register

Datasets are accepted only after checking provenance, licence, labels, file
structure, class balance, participant/sample leakage risk, and suitability for
the stated sensor modality.

| Module | Initial candidate | Status | Reason |
|---|---|---|---|
| Ranger fall | Smartphone Human Fall Dataset (Kaggle, CC0) | Downloaded and structurally verified | 13 activities, binary fall field, extracted inertial features, supplied train/test CSVs |
| Acoustic threat | Kaggle candidate to be verified | Pending | Must contain usable background, gunshot, and chainsaw audio with a clear licence |
| Fire risk | Kaggle tabular/sensor candidate to be verified | Pending | Must contain environmental sensor variables; image-only fire datasets are outside the reduced sensor-data design |

## Dataset acceptance checklist

- [ ] Direct dataset URL and stable citation recorded
- [ ] Licence permits academic use
- [ ] Original source/provenance identified
- [x] Files successfully downloaded and opened
- [x] Target labels verified
- [x] Sample and feature counts recorded
- [ ] Missing values and duplicates measured
- [ ] Class distribution measured
- [ ] Train/test leakage risk assessed
- [ ] Limitations documented

## Current preferred fall dataset

- URL: https://www.kaggle.com/datasets/saadmansakib/smartphone-human-fall-dataset
- Licence shown by Kaggle: CC0 Public Domain
- Reported composition: 767 fall and 1,017 non-fall samples
- Inputs: extracted accelerometer, gyroscope, and linear-acceleration features
- Important validation step: inspect how the supplied split was produced and,
  where subject identifiers are available, prefer subject-independent testing.

## Local verification record

- Downloaded files: `data/raw/fall/Train.csv` and `data/raw/fall/Test.csv`
- Training rows: 1,428 (614 fall, 814 non-fall)
- Test rows: 356 (153 fall, 203 non-fall)
- Columns: 12, including an unnamed exported index, 9 numeric predictors,
  activity `label`, and binary target `fall`
- Train SHA-256: `344d1748c88127b5a8eda77cf1dd735aac8921dd91a7bdc176026bb9e0464430`
- Test SHA-256: `46629aa5022b49c2463304cc369fbaa910369ca5641a3b2011676d62480299e0`
- Structural limitation: no participant identifier appears in the CSV files, so
  subject-independent splitting cannot be reconstructed from these derived
  files. This must be disclosed in the thesis.
