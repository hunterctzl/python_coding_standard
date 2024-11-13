"""
unit tests for transformer_template
"""
import pandas as pd
import pytest
from package_template.transform import divide_transformer
from pyspark.sql import SparkSession


class TestDivideTransform:
    """
    unit tests for transformer_template

    """

    spark = SparkSession.builder.appName("test_transform").getOrCreate()
    expected_df = pd.DataFrame(
        [
            ["001", 2, 10, 5.0],
            ["002", 5, 100, 20.0],
        ],
        columns=["users", "qty", "sales", "price"],
    )

    def test_divide_transformer(self):
        df = self.spark.createDataFrame(
            [
                ["001", 2, 10],
                ["002", 5, 100],
            ],
            ["users", "qty", "sales"],
        )
        result = divide_transformer(
            data=df, numerator_col="sales", denominator_col="qty", result_col="price"
        )

        result_df = result.toPandas().reset_index(drop=True)
        assert self.expected_df.equals(result_df)


if __name__ == "__main__":
    pytest.main()
