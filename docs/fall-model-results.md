# Fall-Detection Experiment Results

## Evaluation protocol

The supplied `Train.csv` was divided into an internal stratified training and
validation split. Model selection used validation F1-score. After selection,
each candidate was retrained using all rows in `Train.csv` and evaluated once
on the untouched supplied `Test.csv`.

The models are transparent NumPy reference implementations rather than
scikit-learn estimators:

- gradient-descent logistic regression;
- linear hinge-loss SVM;
- bootstrapped lightweight random forest.

## Test-set results

| Model | Accuracy | Precision | Fall recall | F1 | Specificity |
|---|---:|---:|---:|---:|---:|
| Random Forest Lite | 96.91% | 94.38% | 98.69% | 96.49% | 95.57% |
| Logistic Regression | 96.07% | 94.27% | 96.73% | 95.48% | 95.57% |
| Linear SVM | 95.79% | 93.13% | 97.39% | 95.21% | 94.58% |

The validation rule selected Random Forest Lite. Its test confusion matrix was:

| | Predicted non-fall | Predicted fall |
|---|---:|---:|
| Actual non-fall | 194 | 9 |
| Actual fall | 2 | 151 |

## Interpretation

Fall recall is the most safety-relevant metric because a false negative may
prevent an emergency alert. The selected model detected 151 of 153 fall records
in the supplied test set, while producing 9 false fall alerts among 203
non-fall records.

## Limitation

The derived CSV files do not contain participant identifiers. Consequently,
participant-independent splitting cannot be reconstructed, and performance may
be optimistic if correlated samples from the same people occur across the
publisher-provided train and test files. This limitation must accompany every
reported performance claim.
