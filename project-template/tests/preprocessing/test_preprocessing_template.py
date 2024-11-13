"""
unit tests for preprocessing-template
"""
import pandas as pd
import pytest
from package_template.preprocessing import agg_preprocessor
from pyspark.sql import SparkSession

class TestAggPreprocessor:
    """
    unit tests for preprocessing_template
    """

    spark = SparkSession.builder.appName("test_preprocessing").getOrCreate()
    expected_df = pd.DataFrame(
        [
            [30, 15.0],
            [40, 150.0],
        ],
        columns=["age", "avg(sales)"],
    )

    def test_agg_preprocessor(self):
        df = self.spark.createDataFrame(
            [
                ["001", 30, 10],
                ["002", 40, 100],
                ["003", 30, 20],
                ["004", 40, 200],
            ],
            ["users", "age", "sales"],
        )

        result = agg_preprocessor(
            data=df, group_cols=["age"], expression={"sales": "avg"}
        )
        result = result.toPandas().reset_index(drop=True)
        assert self.expected_df.equals(result)

if __name__ == "__main__":
    pytest.main()