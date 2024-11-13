"""
unit tests for reader_template
"""

import os
import pytest
from package_template.extract import spark_read
from pandas import DataFrame
from pyspark.sql import SparkSession

class TestSparkReader:
    """
    unit tests for reader_template
    """

    spark = SparkSession.builder.appName("test_spark_read").getOrCreate()
    expected_df = DataFrame(
        [
            ["a", 1],
            ["b", 2],
        ],
        columns=["col1", "col2"],
    )

    def test_parquet(self):
        df = spark_read(
            spark=self.spark,
            file_path="tests/data/test_spark_load_parquet",
            file_format="parquet",
        )
        df = df.toPandas().sort_values("col1").reset_index(drop=True)
        assert self.expected_df.equals(df)
    def test_parquet_error(self):
        e = spark_read(
            spark=self.spark,
            file_path="tests/data/test_spark_load_parquet2",
            file_format="parquet",
        )

        dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        expected_result = ("Error reading file from tests/data/test_spark_load_parquet2 "
            "proceeding with error: [PATH_NOT_FOUND] Path does not exist: "
            f"file:{dir_path}/test_spark_load_parquet2.")
        assert (e == expected_result)

if __name__ == "__main__":
    pytest.main()