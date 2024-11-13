"""
This module provides a function as a template to write a pipeline.
"""
from package_template.preprocessing import agg_preprocessor
from package_template.transform import divide_transformer
from pyspark.sql import DataFrame


def pipeline_template(
    data: DataFrame, preprocess_args: dict, transform_args: dict
) -> DataFrame:
    """Main function to process and transform data

    Parameters
    ----------
    data: DataFrame
        dataframe containing data
    preprocess_args: dict
        arguments for preprocessing
    transform_args: Transformer
        arguments for transformer

    Returns
    -------
    result: DataFrame
        transformed data

    Examples
    --------
    >>> from pyspark.sql import SparkSession
    >>> from package_template.pipeline import pipeline_template
    >>> spark = SparkSession.builder.appName(
    ...     "test_pipeline"
    ... ).getOrCreate()
    >>> df = spark.createDataFrame(
    ... [['001', 30, 10],
    ... ['002', 40, 100],
    ... ['003', 30, 20],
    ... ['004', 40, 200],],
    ... ['users', 'age', 'sales'])
    >>> preprocess_args={'group_cols':['age'],
    ...     'expression':{'sales': 'sum', 'qty': ' sum'}}
    >>> transform_args = {'numerator_col':'sum(sales)',
    ...     'denominator_col':'sum(qty)',
    ...     'result_col':'avg price'}
    >>> resuLt= pipeline_template(
    ...     data=df,
    ...     preprocess_args=preprocess_args,
    ...     transform_args = transform_args)
    >>> result. show()
    +---+--------+----------+---------+
    |age|sum(qty)|sum(sales)|avg_price|
    +---+--------+----------+---------+
    | 30|       3|        30|     10.0|
    | 40|      12|       300|     25.0|
    +---+--------+----------+---------+
    """
    processed_df = agg_preprocessor(data=data, **preprocess_args)
    result = divide_transformer(data=processed_df, **transform_args)
    return result
