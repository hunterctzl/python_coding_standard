"""
This module provides functions to normalize the recommendation score
"""
import math

from package_template.postprocessing import format_output_result
from package_template.utils import logger
from pyspark import keyword_only
from pyspark.ml import Transformer
from pyspark.ml.param import Param
from pyspark.ml.param import Params
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType
from pyspark.sql.types import FloatType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


class ScoreNormalization(Transformer):
    """
    This class is used to transformed and normalized the score distribution
    of our recommendation results.
    """

    group_col = Param(
        Params._dummy(), "group_col", "Provide the name of the item column."
    )
    rec_col = Param(
        Params._dummy(), "rec_col", "Provide the name of the recommendation column."
    )
    score_col = Param(
        Params._dummy(), "score_col", "Provide the name of the score column."
    )
    transformation_method = Param(
        Params._dummy(), "transformation_method", "Provide method to do transformation."
    )
    low_threshold = Param(Params._dummy(), "low_threshold", "Provide low threshold.")
    high_threshold = Param(Params._dummy(), "high_threshold", "Provide high threshold.")
    output_format = Param(
        Params._dummy(),
        "output_format",
        "Provide the format of output, can be 'dataframe', 'json'.",
    )
    provide_score = Param(
        Params._dummy(),
        "provide_score",
        "If True, output scores of each recommended item.",
    )
    verbosity_level = Param(
        Params._dummy(),
        "verbosity_level",
        "verbosity_level to control logger",
    )

    # Initialize parameters
    @keyword_only
    @logger
    def __init__(
        self,
        group_col: str,
        rec_col: str,
        score_col: str,
        transformation_method: str = "log",
        low_threshold: float = float("-inf"),
        high_threshold: float = float("inf"),
        output_format: str = "json",
        provide_score: bool = False,
        verbosity_level: int = 1,
    ):
        """
        Initialize the parameters.

        Parameters
        ----------
        group_col: str
            Provide the name of the item column.
        rec_col: str
            Provide the name of the recommendation column.
        score_col: str
            Provide the name of the score column.
        transformation_method: str = 'log'
            Provide the way to do transformation.
        low_threshold: float = -inf
            Provide the low threshold after transformation. All the values smaller
            than low_threshold will be removed.
        high_threshold: float = inf
            Provide the high threshold after transformation. All the values higher
            than high_threshold will be capped at high_threshold.
        output_format: str, default = 'json'
            Provide the format of output, can be 'dataframe', 'json'.
        provide_score: bool, default = False
            If True, output scores of each recommended item.
        verbosity_level: int, default=1
            an int parameter to control the log information
            only log running time when verbosity_level is 1

        Example
        -------
        >>> from pyspark.sql import SparkSession
        >>> from pyspark_recommender.postprocessing import ScoreNormalization
        >>> spark = SparkSession.builder.appName("test_normalization").getOrCreate()
        >>> item_attributes = [
        ...         "item_id",
        ...         "recommendation",
        ...         "score",
        ...     ]
        >>> rec = [["item1", ["item2", "item3", "item4"], [5, 3, 2]],
        ... ["item2", ["item4", "item5", "item2"], [4, 2, 1]]]
        >>> rec_df = spark.createDataFrame(rec, item_attributes)
        >>> score_transformation = ScoreNormalization(
        ...             group_col="item_id",
        ...             rec_col="recommendation",
        ...             score_col="score",
        ...             output_format="dataframe",
        ...             provide_score=True,
        ...         ).transform(rec_df)
        >>> score_transformation.show(truncate=False)
        +-------+---------------------+----------------------------+
        |item_id|recommendation       |score                       |
        +-------+---------------------+----------------------------+
        |item1  |[item2, item3, item4]|[1.0, 0.6826062, 0.43067655]|
        |item2  |[item4, item5, item2]|[0.8613531, 0.43067655, 0.0]|
        +-------+---------------------+----------------------------+
        """
        super(ScoreNormalization, self).__init__()
        self._setDefault(output_format="json")
        self._setDefault(provide_score=False)
        self._setDefault(transformation_method="log")
        self._setDefault(low_threshold=float("-inf"))
        self._setDefault(high_threshold=float("inf"))
        self._setDefault(verbosity_level=1)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @logger
    def _transform(self, data):
        """
        This function transforms the score columns based
        on the transformation rules.

        Parameters
        ----------
        data: spark.sql.Dataframe
            Provide the recommendation dataframe.

        Returns
        -------
        result: spark.sql.Dataframe or json
            Provide the transformed recommendation dataframe
            or transformed data in json format
        """
        group_col = self.getOrDefault("group_col")
        rec_col = self.getOrDefault("rec_col")
        score_col = self.getOrDefault("score_col")
        transformation_method = self.getOrDefault("transformation_method")
        low_threshold = self.getOrDefault("low_threshold")
        high_threshold = self.getOrDefault("high_threshold")
        output_format = self.getOrDefault("output_format")
        provide_score = self.getOrDefault("provide_score")
        # assertions for params
        assert group_col in data.columns, "data must have the given group_col"
        assert rec_col in data.columns, "data must have the given rec_col"
        assert score_col in data.columns, "data must have the given score_col"
        assert output_format in [
            "dataframe",
            "json",
            "dict",
        ], "output_format should be 'dataframe', 'dict', or 'json'"
        assert isinstance(provide_score, bool), "provide_score must be bool"
        assert transformation_method in [
            "log",
        ], "transformation method should be 'log'"
        assert isinstance(low_threshold, float), "low_threshold must be float"
        assert isinstance(high_threshold, float), "high_threshold must be float"

        # Define UDF to do transformation and filtering
        def transformation_filtering(rec_item, rec_score):
            # Transform the recommendation score
            if transformation_method == "log":
                result_item, result_score = [], []
                for item, score in list(zip(rec_item, rec_score)):
                    # Calculate the log transformation score
                    temp = math.log(score)
                    # Cap at the high threshold
                    if temp > high_threshold:
                        result_item.append(item)
                        result_score.append(high_threshold)
                    # Keep value without change
                    elif temp >= low_threshold:
                        result_item.append(item)
                        result_score.append(temp)
                    # Remove left tail if score smaller than low threshold
                    else:
                        continue
                return result_item, result_score

        # Define and Call the UDF
        schema = StructType(
            [
                StructField("rec_item", ArrayType(StringType()), False),
                StructField("rec_score", ArrayType(FloatType()), False),
            ]
        )
        transformation_filtering_udf = F.udf(transformation_filtering, schema)
        df_transform = data.withColumn(
            "transform", transformation_filtering_udf(F.col(rec_col), F.col(score_col))
        ).select(group_col, "transform.rec_item", "transform.rec_score")

        # Get the largest and smallest value from recommendation score
        df = df_transform.select(
            F.col("rec_score")[0].alias("largest_score"),
            F.element_at(F.col("rec_score"), -1).alias("smallest_score"),
        )
        min_val, max_val = df.select(
            F.min("smallest_score"), F.max("largest_score")
        ).first()

        # Normalize the transformed score
        def normalization(score):
            for idx, num in enumerate(score):
                score[idx] = (num - min_val) / (max_val - min_val)
            return score

        normalization_udf = F.udf(normalization, ArrayType(FloatType()))

        # Select and rename column names
        result_df = (
            df_transform.withColumn(score_col, normalization_udf(F.col("rec_score")))
            .drop("rec_score")
            .withColumnRenamed("rec_item", rec_col)
        )
        # Change the output format
        return format_output_result(
            df=result_df, output_format=output_format, dict_key=group_col
        )
