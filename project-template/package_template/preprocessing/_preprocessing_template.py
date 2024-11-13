"""
This module provides a function ds a template to write a preprocessor.
"""
from pyspark.sql import DataFrame


def agg_preprocessor(
    data: DataFrame,
    group_cols: list,
    expression: dict,
) -> DataFrame:
    """
    Parameters
    ----------
    data: DataFrame
        dataframe containing auditlog records
    group_cols: list
        A list of group by column
    expression: dict
        Aggregation expressions

    Returns
    -------
    result: DataFrame
        preprocessed data

    Examples
    --------
    >>> from pyspark.sql import SparkSession
    >>> from package_template.preprocessing import agg_preprocessor
    >>> spark = SparkSession.builder.appName(
    ...     "test_preprocessing"
    ... ).getOrCreate()
    >>> df = spark.createDataFrame(
    ... [['001', 30, 10],
    ... ['002', 40, 100],
    ... ['003', 30, 20],
    ... ['004', 40, 200],],
    ... ['users', 'age', 'sales'])
    >>> result = agg_preprocessor(
    ...     df=df,
    ...     group_cols=['age'],
    ...     expression={'sales': 'avg'})
    >>> result.show()
    +---+----------+
    |age|avg(sales)|
    +---+----------+
    | 30|      15.0|
    | 40|     150.0|
    +---+----------+

    """

    # assertion
    assert isinstance(data, DataFrame), "df must be pysaprk DataFrame"
    assert isinstance(group_cols, list), "group_cols must be list"
    assert isinstance(expression, dict), "expression must be dict"

    result = data.groupby(group_cols).agg(expression)

    return result
