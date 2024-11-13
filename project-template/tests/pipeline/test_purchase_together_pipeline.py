"""
unit tests for pipeline_template
"""
import pandas as pd
import pytest
from package_template.pipeline import PurchaseTogetherPipeline
from pyspark.sql import SparkSession


class TestPurchaseTogetherPipeline:
    """
    unit tests for PurchaseTogetherPipeline
    """

    spark = SparkSession.builder.appName("test_puchase_together_pipeline").getOrCreate()
    df = spark.createDataFrame(
        [
            [1, "A"],
            [1, "B"],
            [1, "C"],
            [2, "A"],
            [2, "B"],
            [3, "A"],
            [3, "C"],
            [4, "C"],
            [4, "D"],
            [4, "E"],
            [5, "A"],
            [5, "B"],
            [6, "A"],
            [6, "B"],
        ],
        ["trans_id", "item_id"],
    )
    expected_df = pd.DataFrame(
        [
            ["A", ["B", "C"], [1.0, 0.0]],
            ["B", ["A"], [1.0]],
            ["C", ["A"], [0.0]],
        ],
        columns=["item_id", "recommendations", "score"],
    )
    expected_json = [
        {"item_id": "A", "recommendations": ["B", "C"], "score": [1.0, 0.0]},
        {"item_id": "B", "recommendations": ["A"], "score": [1.0]},
        {"item_id": "C", "recommendations": ["A"], "score": [0.0]},
    ]

    def test_puchase_together_pipeline_json(self):

        pipeline = PurchaseTogetherPipeline(
            transaction_col="trans_id",
            item_list_col="shopping_list",
            item_col="item_id",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            rec_col="recommendations",
            output_format="json",
            provide_score=True,
            candidate_count=3,
        )

        result = pipeline.fit(self.df).transform(self.df)

        assert self.expected_json == result

    def test_puchase_together_pipeline_df(self):
        pipeline = PurchaseTogetherPipeline(
            transaction_col="trans_id",
            item_list_col="shopping_list",
            item_col="item_id",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            rec_col="recommendations",
            output_format="dataframe",
            provide_score=True,
            candidate_count=3,
        )

        result = pipeline.fit(self.df).transform(self.df)
        result_df = result.toPandas().sort_values("item_id").reset_index(drop=True)
        assert self.expected_df.equals(result_df)


if __name__ == "__main__":
    pytest.main()
