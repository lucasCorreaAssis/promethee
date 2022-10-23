# Promethee

This repository has the focus of implementing an object-oriented framework for Promethee - Multi Criteria Decision Method.

## How to add to your git existing project

```
git submodule add <URL_TO_THIS_REPOSITORY>
```

## How to use?

To use it's very simple. I'll guide you with an easy example.

We'll build a decision method based on promethee with the fallowing criterias:

|Criteria|First Criteria|Second Criteria|
|---|---|---|
|Weight|1.0|1.0|
|Goal|max|min|
|Preference Curve|Usual Curve|Gaussian Curve [s=0.6]|

With these alternatives and values:

|Alternatives|First Criteria|Second Criteria|
|---|---|---|
|First Alternative| 10 | 9 |
|Second Alternative| 22 | 98 |

First you need to create a class to represent your decision, such as:

```python
from promethee import Promethee

class MyDecision(Promethee):
    pass
```

Then you may want to inject your alternatives through the constructor:

```python
from typing import List
from promethee import Promethee

class MyDecision(Promethee):
    def __init__(self, alternatives: List[str]):
        pass
```

Now you can instantiate your custom criterias in the constructor:

```python
from typing import List
from promethee import Promethee

class MyDecision(Promethee):
    def __init__(self, alternatives: List[str]):
        criterias = self.__set_criterias()

    def __set_criterias(): List[Criteria]:
        criterias = list()

        first_criteria = Criteria(
            name='First Criteria',
            weight=1.0,
            goal='max',
            curve=UsualCurve()
        )
        criterias.append(first_criteria)

        second_criteria = Criteria(
            name='Second Criteria',
            weight=1.0,
            goal='min',
            curve=GaussianCurve(0.5)
        )
        criterias.append(second_criteria)

        # You could have as many criterias you want

        return criterias
```

Now you can call the constructor from `Promethee` base class, injecting the alternatives and criterias:

```python
from typing import List
from promethee import Promethee, Criteria, UsualCurve

class MyDecision(Promethee):
    def __init__(self, alternatives: List[str]):
        criterias = self.__set_criterias()
        super().__init__(alternatives, criterias)

    def __set_criterias(): List[Criteria]:
        criterias = list()

        first_criteria = Criteria(
            name='First Criteria',
            weight=1.0,
            goal='max',
            curve=UsualCurve()
        )
        criterias.append(first_criteria)

        second_criteria = Criteria(
            name='Second Criteria',
            weight=1.0,
            goal='min',
            curve=GaussianCurve(0.5)
        )
        criterias.append(second_criteria)

        # You could have as many criterias you want

        return criterias
```

Now you're all done to use your decision method in other components, for example in a new `main.py` file:

```python
from .mydecision import MyDecision

alternatives = [
    'First Alternative',
    'Second Alternative'
]

my_decision = MyDecision(alternatives)

first_criteria_values = [10, 22]
second_criteria_values = [9, 98]

values = np.array([
    first_criteria_values,
    second_criteria_values
])

output = my_decision.prioritize(values)
```