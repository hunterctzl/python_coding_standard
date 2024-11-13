"""
This module provides a function as a template to write a writer to load data.
"""
from pyspark.sql import DataFrame


def spark_write(
    data: DataFrame, file_path: str, file_format: str = "parquet", mode: str = "append"
):
    """A function to write pyspark DataFrame into Hadoop
    Parameters
    ----------
    data: DataFrame
        The data to write into Hadoop
    file_path: str
        file path
    file_format: str, default = 'parquet'
        file format, for example 'parquet', 'com.databricks.spark.avro'
    mode: str, default = 'append'
        writing mode, for example 'append'

    Returns
    -------

    Examples
    --------
    >>> from pyspark.sql import SparkSession
    >>> from package_template.load import spark_write
    >>> spark = SparkSession.builder.appName(
    ...     "test_spark_write"
    ... ).getorCreate(
    >>> df = spark.createDataFramel(
    ...     [["a", 1], ["b", 2]],
    ...     ["col1", "col2"])
    >>> spark_write(
    ...     data=df,
    ...     file_path="/tests/path",
    ...     file_format="parquet")
    """

    # assertion
    assert isinstance(data, DataFrame), "df must be pyspark DataFrame"
    assert isinstance(file_path, str), "file_path must be str"
    assert isinstance(file_format, str), "file_format must be str"
    assert isinstance(mode, str), "mode must be str"
    data.write.mode(mode).format(file_format).save(file_path)
