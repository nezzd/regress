# decision-kit

Decision tree classifier from scratch implementation with branching criteria based on Gini impurity.
Below a snapshot of the result I obtained.

```python
from decisionkit.tree._tree import DecisionTree as decisionkit_tree
from sklearn.tree import DecisionTreeClassifier as sklearn_tree

# processing data...

scikit_learn_tree = sklearn_tree()
my_decision_tree = decisionkit_tree()

scikit_learn_tree.fit(xtrain, ytrain)
my_decision_tree.build(header, xtrain, ytrain)

scikit_learn_accuracy = accuracy(scikit_learn_tree.predict(xtest), ytest)
my_decision_tree_accuracy = accuracy(my_decision_tree.predict(header, xtest), ytest)

print(f'Scikit-learn accuracy: {scikit_learn_accuracy}')
print(f'My decision tree accuracy: {my_decision_tree_accuracy}')
```
```bash
Scikit-learn accuracy: 0.838
My decision tree accuracy: 0.822
```
