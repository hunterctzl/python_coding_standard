# Python Coding Standard

## Purpose
This document specifies coding standards for Python applications and
provides general guidelines on best practices.
Follow numpy and offifical [PEP 8](https://www.python.org/dev/peps/pep-0008/)
style guide for other cases.

## 1. Naming Conventions
The following naming styles are commonly distinguished:
- `b` (single lowercase letter)
- `B` (single uppercase letter)
- `lowercase`
- `lower_case_with_underscores`
- `UPPERCASE`
- `UPPER_CASE_WITH_UNDERSCORES`
- `CapitalizeWords` (or CapWords or CamelCase). This is also sometimes known as StudyCaps.
Note: When using acronyms in CapWords, capitalize all the letters of the acronym.
Thus, HTTPServerError is better than HttpServerError
- `Capitalized_Words_With_Underscores` (ugly!)

### 1.1 General Naming:
In general, we use `lower_case_with_underscores` to name modules, packages, methods,
functions, and variables. For example:
- `module_name`,
- `package_name`,
- `method_name`,
- `function_name`,
- `instance_var_name`,
- `function_parameter_name`,
- `local_var_name`.

We use `CapitalizeWords` to name class and exceptions. For example:
- `ClassName`,
- `ExceptionName`,

We use `UPPER_CASE_WITH_UNDERSCORES` to name global variables. For example:
- `GLOBAL_VAR_NAME`

#### 1.1.1 Column name as a parameter
To define a column name, we use `_col` as suffix.

singular:
```
item_col = “item”
```

plural:
```
item_cols = [“year”, “month”, “day”]
```

#### 1.1.2 DataFrame as a parameter
pandas dataframe parameters use `_df` as suffix:
e.g., `item_df`.


### 1.2 Naming with underscores
In addition, the following special forms using leading or trailing underscores
are recognized (these can generally be combined with any case convention):

- `_single_leading_underscore`: weak “internal use” indicator.
E.g. from M import * does not import objects whose names start with an underscore.
- `single_trailing_underscore_`: used by convention to avoid conflicts with Python keyword, e.g. :
```
tkinter.Toplevel(master, class_='ClassName')
```
- `__double_leading_underscore`: when naming a class attribute,
invokes name mangling (inside class FooBar, `__boo` becomes `_FooBar__boo`; see below).
- `__double_leading_and_trailing_underscore__`: “magic” objects or attributes that
live in user-controlled namespaces. E.g. `__init__`, `__import__` or `__file__`.
Never invent such names; only use them as documented.

#### 1.2.1 Support and private functions
Support functions need single underscores as prefix:

e.g., ```_support_function_name()```.

Private functions need double underscores as prefix:

e.g., ```__private_function_name()```.

## 2. Documentation
Use docstring and comments to document your code.

### 2.1 docstring
Write docstrings for all public modules, functions, classes, and methods.
Docstrings are not necessary for non-public methods,
bout you should have comment that describes what the method does.
[PEP 257](https://peps.python.org/pep-0257/) describes good docstring conventions.

The instruction to use numpy docstring is here.
At the very beginning of your .py file, use docstring to define to purpose of this file. For example:
```
"""
This module provides ALS and SVD models.
"""
```

In each class or function, use docstring to define parameters, returns, and example.
For each parameter and return object, specify the type.
If having a default value, specify the default value.
In the example, generate sample data if possible and provide the expected output.
```
"""
At the beginning describe the purpose of this function.

Parameters
----------
pandas_df: Pandas DataFrame
    explain this parameter
bool_param: boolean, default=True
    explain this parameter
str_param: str, default=""
    explain this parameter
int_param: int, default=None
    explain this parameter
list_param: list, default=None
    explain this parameter

Returns
-------
result: pandas DataFrame
    explain this object

Example
-------
>>> import pandas as pd
>>> from recommender.clean.text import text_cleaning
>>> data = pd.DataFrame(["This is a sample sentence",],
>>>                     columns=["text"],)
>>> function(data)
               text
0  [sampl, sentenc]
"""
```

### 2.2 Block and inline Comments
Block comments generally apply to some (or all) code that follows them,
and are indented to the same level as that code.
Each line fo a block comment starts with a `#` and a single space
(unless it is indented text inside the comment).

An inline comment is a comment on the same line as a statement.
Inline comments should be separated by at least two spaces from the statement.
They should start with a `#` and a single space.
```
# This is a block comment
def test_function(x): y = x + 5 # This is an inline comment
    return y
```

Always use human-readable language as comments to explain your code. For example:
```
# multiply a and b
c = a * b
```

## 3. Define parameters
When defining a parameter in a function, we should specify its type.
If this parameter needs a default value, specify the default value as well. For example:
```
def function(pandas_df: pd.DataFrame,
              bool_param: bool = True,
              str_param: str = "",
              int_param: int = 1,
              list_param: list = None) -> pd.DataFrame:
```

### 3.1 Avoid hardcoding
One purpose of using parameters is to avoid hardcoding.
Do not hardcode any dataframe, bool, str, int, float, or list in your code.
For example, calling a column of a dataframe, first define a column parameter,
and then use `df[column]`. Do not directly use `df[“column_name“]` in your code.

## 4. Assertion
The type hint does not check if you pass a correct type.
For example: you define a function below and specify the typ e of each param.
But if you use wrong types, such as `function(str_param=1, int_param='abc')`,
the function will not return an error.
```
def function(str_param: str = "", int_param: int = 0):
    return
```
Thus, we must use assertion to make sure the parameters are in the right format
and value and return errors to help users to modify their parameters.
For example, if you specify an str parameter and only have three options and
an int parameter, do:
```
def function(str_param: str = "option1", int_param: int = 0):
    assert str_param == "option1" or "option2" or "option3",
                    "str_param must be option1 or option2 or option3"
    assert isinstance(int_param), "int_param must be int"
```

## 5. Unit test
We use pytest as the framework to run unit tests.
Unit test is always the first thing we need to code when developing.
A basic test case can help developers to define the input and output of the function.
In the basic test case, generate the minimum required input data and the expected output
and assert the function output with expected output.
If the function’s output can change based on parameters,
your need to include test cases to cover all conditions.
For example: this function has two conditions, bool_param is True or False.
```
def sample_function(bool_param: bool = True) -> int:
    if bool_param:
        return 1
    else:
        return 0
```
We need two unit test to cover all conditions:
```
import pytest

Class TestSampleFcuntion:
    """
    Unit test for sample_function
    """
    def test_bool_param_is_true(self):
        expected_result = 1
        result = sample_function(bool_param = True)
        assert result == expected_result

    def test_bool_param_is_false(self):
        expected_result = 0
        result = sample_function(bool_param = False)
        assert result == expected_result
if __name__ == "__main__":
    pytest.main()
```

## 6. Streamline code

### 6.1 Identify repeating code snippets and group them into a function
Don't repeat yourself (DRY), if you need to repeat your code,
always write that code into a function.
For example, instead of writing a regex expression for keyword
matching every time, we can create a function:
```
def build_regex_exp_from_terms(terms):
    """Build regex expression for parsing list of terms
    Parameters
    ----------
    terms : iterable string
    List of key terms for building the regex expression. Each of the term will
    then be checked for punctuation prefix and suffix, striped and converted to lowercase.
    Returns
    -------
    Raw String
    Raw string for regex
    """
    return (
            r"\b"
            + r"\b|\b".join(t.strip(" " + string.punctuation).lower() for t in terms)
            + r"\b"
            )
```

### 6.2 Remove redundant cells, lines and variables
Always simplify your code by removing redundant code such as:
```
df_temp = df.copy()
gc.collect()
temp = df.some_columns.unique()
```

### 6.3 Moving all import to the beginning
Define everything you need upfront, and you will never need to worry about where to find them

### 6.4 Make better use of Python’s standard libraries
Always use python’s built-in functions to simplify your code.

Example 1: collection.Counter for counting occurrences
```
# instead of this
counter = dict()
for item in my_list:
    counter[item] = counter.get(item, 0) + 1

# do this
from collections import Counter
counter = Counter(my_list)
```

Example 2: bisect.insort for maintaining a sorted list
```
# just do this
from bisect import insort
my_sorted_list = []
for i in (1, 324, 52, 568, 24, 12, 8):
    insort(my_sorted_list, i)
```

## 7. Maximize Efficiency
Improve your code’s time and space efficiency.

### 7.1 Vectorize for loops using NumPy
A good practice is to vectorize any for loops using NumPy.
This is because a lot of NumPy is written in C, under the hood,
and C is a much faster language than Python. For example,
consider the problem of summing a vector containing one billion ones,
which we have attempted to solve in two different ways,
the first version using a for loop and the second version using the NumPy sum() function.
```
import numpy as np
import time
x = np.ones(1000000000)

# For loop version
t0 = time.time()
total1 = 0
for i in range(len(x)):
    total1 += x[i]
t1 = time.time()
print('For loop run time:', t1 - t0, 'seconds')

# Numpy version
t2 = time.time()
total2 = np.sum(x)
t3 = time.time()
print('Numpy run time:', t3 - t2, 'seconds')
```
Using a for loop, this problem takes 275 seconds (over 4 1/2 minutes) to solve. However, using the NumPy sum function, the run time reduces to 15.7 seconds. That is, the for loop takes 17.5 times longer than the NumPy summation.
