"""
This module provides a function as a template to write a transformer.
"""
from pyspark.sql import DataFrame
from pyspark.sql import functions as f

def divide_transformer(
    data: DataFrame,
    numerator_col: str,
    denominator_col: str,
    result_col: str
) -> DataFrame:
    """Main function to transform auditlog records

    Parameters
    ----------
    data: DataFrame
        preprocessed data
    numerator_col: str
        the name of numerator column
    denominator_col: str
        the name of denominator column
    result_col: str
        the name of result column

    Returns
    -------
    result: DataFrame
        transformed data

    Examples
    --------
    >>> from pyspark.sql import SparkSession
    >>> from package_template.transform import divide_transformer
    >>> spark = SparkSession.builder.appName(
    ...     "test_transform"
    ... ).getOrCreate()
    >>> df = spark.createDataFrame([['001', 2, 10],['002', 5, 100],],
    ...                         ['users', 'qty', 'sales'])
    >>> result = divide_transformer(
    ... df=df,
    ... numerator_col='sales',
    ... denominator_col='qty',
    ... result_col='price')
    >>> result.show()
    +-----+---+-----+-----+
    |users|qty|sales|price|
    +-----+---+-----+-----+
    |  001|  2|   10|  5.0|
    |  002|  5|  100| 20.0|
    +-----+---+-----+-----+
    """

    result = data.withColumn(result_col, f.col(numerator_col) / f.col (denominator_col))
    return result