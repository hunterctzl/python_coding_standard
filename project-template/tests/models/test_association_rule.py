"""
Unit Test for Association Rule.
"""
import pandas as pd
import pytest
from package_template.models import AssociationRuleModel
from package_template.utils import check_log
from pyspark.sql import SparkSession


class TestAssociationRuleRecommender:
    spark = SparkSession.builder.appName("test_association_rule").getOrCreate()
    df = spark.createDataFrame(
        pd.DataFrame(
            [
                (6, ["B", "A"]),
                (5, ["B", "A"]),
                (1, ["C", "B", "A"]),
                (3, ["C", "A"]),
                (2, ["B", "A"]),
                (4, ["C", "E", "D"]),
            ],
            columns=["trans_key", "shopping_list"],
        )
    )

    # case 1: json format
    def test_json_format(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            provide_score=True,
            candidate_count=3,
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {
                "item_id": "A",
                "recommendations": ["B", "C"],
                "score": [1.2000000000000002, 0.8],
            },
            {"item_id": "B", "recommendations": ["A"], "score": [1.2]},
            {"item_id": "C", "recommendations": ["A"], "score": [0.7999999999999999]},
        ] == prediction, "result not correct."

    # case 2: dataframe format
    def test_dataframe_format(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            provide_score=True,
            candidate_count=3,
            output_format="dataframe",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert (
            prediction.subtract(
                self.spark.createDataFrame(
                    pd.DataFrame(
                        [
                            ("B", ["A"], [1.2]),
                            ("C", ["A"], [0.7999999999999999]),
                            ("A", ["B", "C"], [1.2000000000000002, 0.8]),
                        ],
                        columns=["item_id", "recommendations", "score"],
                    )
                )
            ).collect()
            == []
        ), "result not correct."

    # case 3: dataframe format with target_item
    def test_dataframe_format_with_target_item(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            provide_score=True,
            candidate_count=3,
            output_format="dataframe",
            target_item="A",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert (
            prediction.subtract(
                self.spark.createDataFrame(
                    pd.DataFrame(
                        [("A", ["B", "C"], [1.2000000000000002, 0.8])],
                        columns=["item_id", "recommendations", "score"],
                    )
                )
            ).collect()
            == []
        ), "result not correct."

    # case 4: json format with target_item
    def test_json_format_with_target_item(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            provide_score=True,
            candidate_count=3,
            output_format="json",
            target_item="A",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {
                "item_id": "A",
                "recommendations": ["B", "C"],
                "score": [1.2000000000000002, 0.8],
            }
        ] == prediction, "result not correct."

    # case 5: json format with target_item and more than 1 recommendations.
    def test_json_format_with_target_item_more_rec(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.02,
            min_confidence=0.2,
            provide_score=True,
            candidate_count=5,
            output_format="json",
            target_item="E",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {"item_id": "E", "recommendations": ["D", "C"], "score": [6.0, 2.0]}
        ] == prediction, "result not correct."

    # case 6: json format with target_item and 1 recommendation.
    def test_json_format_with_target_item_1_rec(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.02,
            min_confidence=0.2,
            provide_score=True,
            candidate_count=1,
            target_item="E",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {"item_id": "E", "recommendations": ["D"], "score": [6.0]}
        ] == prediction, "result not correct."

    # case 7: json format with target_item and No Score.
    def test_json_format_with_target_item_no_score(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.02,
            min_confidence=0.2,
            provide_score=False,
            candidate_count=5,
            target_item="E",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {"item_id": "E", "recommendations": ["D", "C"]}
        ] == prediction, "result not correct."

    # case 8: json format and No Score.
    def test_json_format_no_score(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.02,
            min_confidence=0.2,
            min_lift=0.5,
            provide_score=False,
            candidate_count=5,
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        print(prediction)
        assert [
            {"item_id": "A", "recommendations": ["B", "C"]},
            {"item_id": "B", "recommendations": ["A", "C"]},
            {"item_id": "C", "recommendations": ["D", "E", "A", "B"]},
            {"item_id": "D", "recommendations": ["E", "C"]},
            {"item_id": "E", "recommendations": ["D", "C"]},
        ] == prediction, "result not correct."

    # case 9: json format and change column name
    def test_json_format_change_column_name(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.02,
            min_confidence=0.2,
            min_lift=0.4,
            item_col="item",
            rec_col="rec",
            score_col="sco",
            provide_score=True,
            candidate_count=5,
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {"item": "A", "rec": ["B", "C"], "sco": [1.2000000000000002, 0.8]},
            {"item": "B", "rec": ["A", "C"], "sco": [1.2, 0.5]},
            {
                "item": "C",
                "rec": ["D", "E", "A", "B"],
                "sco": [2.0, 2.0, 0.7999999999999999, 0.5],
            },
            {"item": "D", "rec": ["E", "C"], "sco": [6.0, 2.0]},
            {"item": "E", "rec": ["D", "C"], "sco": [6.0, 2.0]},
        ] == prediction, "result not correct."

    # case 10: json format and change test_num_limit_in_cart
    def test_num_limit_in_cart(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.02,
            min_confidence=0.2,
            min_lift=0.5,
            item_col="item",
            rec_col="rec",
            score_col="sco",
            provide_score=True,
            candidate_count=5,
            num_limit_in_cart=2,
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        assert [
            {"item": "A", "rec": ["B", "C"], "sco": [1.0, 1.0]},
            {"item": "B", "rec": ["A"], "sco": [1.0]},
            {"item": "C", "rec": ["A"], "sco": [1.0]},
        ] == prediction, "result not correct."

    # case 11: dict format
    def test_dict_format(self):
        # Define Association Rule Recommender
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.2,
            min_confidence=0.2,
            min_lift=0.5,
            provide_score=True,
            candidate_count=3,
            output_format="dict",
        )
        #  fit and provide recommendations
        prediction = model.fit(self.df).transform(self.df)
        expected = {
            "A": {
                "recommendations": ["B", "C"],
                "score": [1.2000000000000002, 0.8],
            },
            "B": {"recommendations": ["A"], "score": [1.2]},
            "C": {"recommendations": ["A"], "score": [0.7999999999999999]},
        }
        assert expected == prediction, "result not correct."

    # Test log
    def test_log(self):
        model = AssociationRuleModel(
            item_list_col="shopping_list",
            min_support=0.2,
            min_confidence=0.2,
            provide_score=True,
            candidate_count=3,
            output_format="dict",
            verbosity_level=1,
        )
        #  fit and provide recommendations
        model.fit(self.df).transform(self.df)

        assert check_log(class_func="AssociationRuleModel.__init__")
        assert check_log(class_func="AssociationRuleModel._fit")
        assert check_log(class_func="AssociationRuleModelTransformer.__init__")
        assert check_log(class_func="AssociationRuleModelTransformer._transform")


if __name__ == "__main__":
    pytest.main()
