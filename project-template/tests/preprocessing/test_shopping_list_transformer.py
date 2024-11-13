"""
Unit Test for Shopping List Transformer.
"""
import pandas as pd
import pytest
from package_template.preprocessing import ShoppingListTransformer
from package_template.utils import check_log
from pyspark.sql import SparkSession


class TestShoppingListTransformer:
    spark = SparkSession.builder.appName("test_shopping_list_transformer").getOrCreate()
    sc = spark.sparkContext
    df = pd.DataFrame(
        [["T1", "I1"], ["T1", "I2"], ["T1", "I3"], ["T2", "I1"], ["T2", "I2"]],
        columns=["trans_id", "item_id"],
    )

    df = spark.createDataFrame(df)
    pickleRdd = sc.pickleFile(
        "tests/data/test_shopping_list_transformer_result"
    ).collect()
    target_output = spark.createDataFrame(pickleRdd)

    def test_transformer(self):
        # Define transformer
        transformer = ShoppingListTransformer(
            transaction_col="trans_id",
            item_col="item_id",
            output_col="shopping_list",
        )
        # transform data into shopping-list format.
        result = transformer.transform(self.df)
        assert (
            result.subtract(self.target_output).collect() == []
        ), "result not correct."

    # Test log
    def test_log(self):
        ShoppingListTransformer(
            transaction_col="trans_id",
            item_col="item_id",
            output_col="shopping_list",
        ).transform(self.df)

        assert check_log(class_func="ShoppingListTransformer.__init__")
        assert check_log(class_func="ShoppingListTransformer._transform")


if __name__ == "__main__":
    pytest.main()
