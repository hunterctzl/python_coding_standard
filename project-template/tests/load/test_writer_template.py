"""
unit tests for writer_template
"""
import shutil
import pytest
from package_template.load import spark_write
from pandas import DataFrame
from pyspark.sql import SparkSession

class TestSparkWriter:
    """
    unit tests for writer_template
    """

    spark = SparkSession.builder.appName("test_spark_read").getOrCreate()
    df = spark.createDataFrame(
        [
            ["a", 1],
            ["b", 2],
        ],
        ["col1", "col2"],
    )

    expected_df = DataFrame(
        [
            ["a", 1],
            ["b", 2],
        ],
        columns=["col1", "col2"],
    )

    def test_parquet(self):
        spark_write(
            data=self.df,
            file_path="tests/data/test_spark_write_parquet",
            file_format="parquet",
        )
        result_df = self.spark.read.format("parquet").load(
            "tests/data/test_spark_write_parquet"
        )
        result_df = result_df.toPandas().sort_values("col1").reset_index(drop=True)
        shutil.rmtree("tests/data/test_spark_write_parquet")
        assert self.expected_df.equals(result_df)

if __name__ == "__main__":
    pytest.main()