# decision-kit

Decision tree from scratch, implementation and accuracy comparison with branching criteria based on Gini impurity.

Gini = 1 - Σ (Pi)² for i=1 to number of classes

```python
from decisionkit.utils.helper import accuracy
from decisionkit.tree._tree import DecisionTree

classifier = DecisionTree()
classifier.build(header, xtrain, ytrain)
predicted_val = classifier.predict(header, xtest)
acc = accuracy(predicted_val, ytest)
print(acc)
```
