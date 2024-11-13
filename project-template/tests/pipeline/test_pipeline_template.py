"""
unit tests for pipeline_template
"""
import pandas as pd
import pytest
from package_template.pipeline import pipeline_template
from pyspark.sql import SparkSession


class TestPipelineTemplate:
    """
    unit tests for pipeline_template
    """

    spark = SparkSession.builder.appName("test_pipeline").getOrCreate()
    expected_df = pd.DataFrame(
        [
            [30, 3, 30, 10.0],
            [40, 12, 300, 25.0],
        ],
        columns=["age", "sum(qty)", "sum(sales)", "avg_price"],
    )

    def test_pipeline_template(self):
        df = self.spark.createDataFrame(
            [
                ["001", 30, 10, 1],
                ["002", 40, 100, 4],
                ["003", 30, 20, 2],
                ["004", 40, 200, 8],
            ],
            ["users", "age", "sales", "qty"],
        )

        preprocess_args = {
            "group_cols": ["age"],
            "expression": {"sales": "sum", "qty": "sum"},
        }
        transform_args = {
            "numerator_col": "sum(sales)",
            "denominator_col": "sum(qty)",
            "result_col": "avg_price",
        }

        result = pipeline_template(
            data=df, preprocess_args=preprocess_args, transform_args=transform_args
        )
        result_df = result.toPandas().sort_values("age").reset_index(drop=True)

        assert self.expected_df.equals(result_df)


if __name__ == "__main__":
    pytest.main()
