"""
This module provides a function as a template to write a reader to extract data.
"""
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException


def spark_read(
    spark: SparkSession,
    file_path: str,
    file_format: str = "parquet",
) -> DataFrame:
    """A function to read different Hadoop formats data into pyspark DataFrame

    Parameters
    ----------
    spark: SparkSession
        define SparkSession
    file_path: str
        file path
    file_format: str，default = 'parquet'
        file format, for example 'parquet', 'com.databricks.spark.avro'

    Returns
    -------
    df:DataFrame
        The Hadoop data in DataFrame format
    Examples
    --------
    >>> from pyspark.sql import SparkSession
    >>> from package_template.extract import spark_read
    >>> spark = SparkSession.builder.appNameC
    ... "test_spark_write"
    ... ). getorCreate()
    >>> df = spark_read(
    ... spark=spark,
    ... file_path="../../tests/data/test_spark_load_parquet",
    ... file_format="parquet")
    >>> df.show()
    +----+----+
    |col1|col2|
    +----+----+
    |   b|   2|
    |   a|   1|
    +----+----+
    """

    # assertion
    assert isinstance(spark, SparkSession), "df must be SparkSession"
    assert isinstance(file_path, str), "file_path must be str"
    assert isinstance(file_format, str), "file_format must be str"

    try:
        return spark.read.format(file_format).load(file_path)
    except AnalysisException as e:
        return f"Error reading file from {file_path} proceeding with error: {str(e)}"
