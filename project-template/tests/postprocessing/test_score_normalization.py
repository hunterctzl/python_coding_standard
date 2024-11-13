import math

import pandas as pd
from package_template.postprocessing import ScoreNormalization
from pyspark.sql import SparkSession


class TestRemoveSameCategoryItems:
    spark = SparkSession.builder.appName("test_filterer").getOrCreate()
    result_df = pd.DataFrame(
        data=[
            ["item1", ["item2", "item3", "item4"], [6, 5, 3]],
            ["item2", ["item4", "item3", "item5"], [5, 5, 2]],
            ["item3", ["item1", "item2", "item4"], [3, 1, 1]],
        ],
        columns=["item_id", "recommendation", "score"],
    )
    result_df = spark.createDataFrame(result_df)

    def test_score_normalization(self):
        expected_result = {
            0: {
                "item_id": "item1",
                "recommendation": ["item2", "item3", "item4"],
                "score": [1.0, 0.8982443809509277, 0.6131471991539001],
            },
            1: {
                "item_id": "item2",
                "recommendation": ["item4", "item3", "item5"],
                "score": [0.8982443809509277, 0.8982443809509277, 0.38685280084609985],
            },
            2: {
                "item_id": "item3",
                "recommendation": ["item1", "item2", "item4"],
                "score": [0.6131471991539001, 0.0, 0.0],
            },
        }

        actual_result = (
            ScoreNormalization(
                group_col="item_id",
                rec_col="recommendation",
                score_col="score",
                output_format="dataframe",
                provide_score=True,
            )
            .transform(self.result_df)
            .toPandas()
            .to_dict(orient="index")
        )

        assert actual_result == expected_result

    def test_score_normalization_with_threshold_json_output(self):
        expected_result = [
            {
                "item_id": "item1",
                "recommendation": ["item2", "item3", "item4"],
                "score": [1.0, 1.0, 0.0],
            },
            {
                "item_id": "item2",
                "recommendation": ["item4", "item3"],
                "score": [1.0, 1.0],
            },
            {"item_id": "item3", "recommendation": ["item1"], "score": [0.0]},
        ]

        actual_result = ScoreNormalization(
            group_col="item_id",
            rec_col="recommendation",
            score_col="score",
            low_threshold=math.log(3),
            high_threshold=math.log(5),
            output_format="json",
            provide_score=True,
        ).transform(self.result_df)
        assert actual_result == expected_result
