"""
Association Rule in pyspark.
Covert code in to (Transformer, Estimator, Pipeline).
"""
import pyspark.sql.functions as f
from pyspark import keyword_only
from pyspark.ml import Estimator
from pyspark.ml.fpm import FPGrowth
from pyspark.ml.param import Param
from pyspark.ml.param import Params
from pyspark.ml.pipeline import Model
from pyspark.sql import Window
from pyspark.sql.functions import col
from pyspark.sql.functions import desc
from pyspark.sql.functions import size

from package_template.postprocessing import format_output_result
from package_template.utils import logger


class AssociationRuleModel(Estimator):
    """
    Provide Association Rule model to provide recommendations
    for purchased together.
    """

    # use Param function to define parameters
    item_list_col = Param(
        Params._dummy(),
        "item_list_col",
        "Provide the name of the column of list of item ID.",
    )
    min_support = Param(
        Params._dummy(),
        "min_support",
        "Provide the minimum support",
    )
    min_confidence = Param(
        Params._dummy(),
        "min_confidence",
        "Provide the minimum confidence",
    )
    min_lift = Param(
        Params._dummy(),
        "min_lift",
        "Provide the minimum lift",
    )
    candidate_count = Param(
        Params._dummy(), "candidate_count", "number of top candidates"
    )
    target_item = Param(
        Params._dummy(), "target_item", "Specify if want prediction for a single item"
    )
    item_col = Param(
        Params._dummy(),
        "item_col",
        "filed name for item in the output.",
    )
    rec_col = Param(
        Params._dummy(),
        "rec_col",
        "filed name for recommendations in the output.",
    )
    score_col = Param(
        Params._dummy(),
        "score_col",
        "filed name for score in the output.",
    )
    provide_score = Param(
        Params._dummy(),
        "provide_score",
        "Set to True if desire score in the output.",
    )
    output_format = Param(
        Params._dummy(),
        "output_format",
        "Declare Output format.('json', 'dataframe')",
    )

    num_limit_in_cart = Param(
        Params._dummy(),
        "num_limit_in_cart",
        "Declare the item limit number in each shopping cart.",
    )
    verbosity_level = Param(
        Params._dummy(),
        "verbosity_level",
        "verbosity_level to control logger",
    )

    @keyword_only
    @logger
    def __init__(
        self,
        item_list_col: str,
        min_support: float = 0.002,
        min_confidence: float = 0.2,
        min_lift: float = 1.2,
        candidate_count: int = 50,
        target_item: int or str = None,
        item_col: str = "item_id",
        rec_col: str = "recommendations",
        score_col: str = "score",
        provide_score: bool = False,
        output_format: str = "json",
        num_limit_in_cart: int = 20,
        verbosity_level: int = 1,
    ):
        """
        initialize parameters

        Parameters
        ----------
        item_list_col: str
            Provide the name of the column of list of item ID.
            e.g. item_list_col = "shopping_list"
        min_support: float, default = 0.002
            the minimum support for an itemset to be identified as frequent.
            For example, if an item appears 3 out of 5 transactions,
            it has a support of 3/5=0.6.
            e.g. min_support = 0.002
        min_confidence: float, default = 0.2
            minimum confidence for generating Association Rule.
            Confidence is an indication of how often an association rule
            has been found to be true.
            For example, if in the transactions itemset X appears 4 times,
            X and Y co-occur only 2 times,
            the confidence for the rule X => Y is then 2/4 = 0.5.
            The parameter will not affect the mining for frequent itemsets,
            but specify the minimum confidence for
            generating association rules from frequent itemsets.
        min_lift: float, default = 1.2
            minimum lift for generating Association Rule.
            lift is the rise in probability of having {Y} on the
            cart with the knowledge of {X} being present over the
            probability of having {Y} on the cart
            without any knowledge about presence of {X}
            Lift(X-->Y) = support(X U Y) / support(X).support(Y)
        candidate_count: int, default = 10
            number of top candidates
        target_item: int or str, default = None
            Specify if want prediction for a single item.
        item_col: str, default = "item_id"
            filed name for item in the output.
        rec_col: str, default = "recommendations"
            filed name for recommendations in the output.
        score_col: str, default = "score"
            filed name for score in the output.
        provide_score: bool, default = False
            Set to True if desire score in the output.
        output_format: str， default = "json"
            Declare Output format.("json", "dataframe")
        num_limit_in_cart: int, default = 20
            Item limit number in each shopping cart. If this value too big, the fit will
            be very slow.
        verbosity_level: int, default=1
            an int parameter to control the log information
            only log running time when verbosity_level is 1

        Example
        -------
        >>> from pyspark.sql import SparkSession
        >>> from package_template.models import AssociationRuleModel
        >>> spark = SparkSession.builder.appName("test_association_rule").getOrCreate()
        >>> df = spark.createDataFrame(
        >>> pd.DataFrame(
        ...         [
        ...         (6, ["B", "A"]),
        ...         (5, ["B", "A"]),
        ...         (1, ["C", "B", "A"]),
        ...         (3, ["C", "A"]),
        ...         (2, ["B", "A"]),
        ...        (4, ["C", "E", "D"]),
        ...     ],
        ...     columns=["trans_key", "shopping_list"],
        ...   )
        ... )
        >>> model = AssociationRuleModel(
        ...        item_list_col="shopping_list",
        ...        min_support=0.2,
        ...        min_confidence=0.2,
        ...        min_lift = 0.5,
        ...        provide_score=True,
        ...        candidate_count=3,
        ...    )
        >>> result = model.fit(self.df).transform(self.df)
        >>> print(result)
        {"item_id": "B", "recommendations": ["A"], "score": [1.2]},
        {"item_id": "C", "recommendations": ["A"], "score": [0.7999999999999999]},
        {
                "item_id": "A",
                "recommendations": ["B", "C"],
                "score": [1.2000000000000002, 0.8],
        }
        """
        super(AssociationRuleModel, self).__init__()

        self._setDefault(min_support=0.002)
        self._setDefault(min_confidence=0.2)
        self._setDefault(min_lift=1.2)
        self._setDefault(candidate_count=5)
        self._setDefault(target_item=None)
        self._setDefault(item_col="item_id")
        self._setDefault(rec_col="recommendations")
        self._setDefault(score_col="score")
        self._setDefault(provide_score=False)
        self._setDefault(output_format="json")
        self._setDefault(num_limit_in_cart=20)
        self._setDefault(verbosity_level=1)

        # enable kwargs
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(
        self,
        item_list_col,
        min_support=0.002,
        min_confidence=0.2,
        min_lift=1.2,
        candidate_count=5,
        target_item=None,
        item_col="item_id",
        rec_col="recommendations",
        score_col="score",
        provide_score=False,
        output_format="json",
        num_limit_in_cart=20,
        verbosity_level=1,
    ):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    @logger
    def _fit(self, df):
        """
        Fits a model to the input dataset.
        This is called by the default implementation of fit.
        Parameters
        ----------
        df: pyspark.sql.DataFrame
            Input transaction dataset with transaction id and shopping list.
        """
        # prepare params
        item_list_col = self.getOrDefault("item_list_col")
        min_support = self.getOrDefault("min_support")
        min_confidence = self.getOrDefault("min_confidence")
        min_lift = self.getOrDefault("min_lift")
        candidate_count = self.getOrDefault("candidate_count")
        target_item = self.getOrDefault("target_item")
        item_col = self.getOrDefault("item_col")
        rec_col = self.getOrDefault("rec_col")
        score_col = self.getOrDefault("score_col")
        provide_score = self.getOrDefault("provide_score")
        output_format = self.getOrDefault("output_format")
        num_limit_in_cart = self.getOrDefault("num_limit_in_cart")
        verbosity_level = self.getOrDefault("verbosity_level")

        # filter based on num_limit_in_cart.
        df = df.where(size(col(item_list_col)) <= num_limit_in_cart)

        # apply FP Growth association rule model.
        fp_growth = FPGrowth(
            itemsCol=item_list_col, minSupport=min_support, minConfidence=min_confidence
        )
        model = fp_growth.fit(df)

        # return model
        return AssociationRuleModelTransformer(
            model=model,
            candidate_count=candidate_count,
            min_lift=min_lift,
            target_item=target_item,
            item_col=item_col,
            rec_col=rec_col,
            score_col=score_col,
            provide_score=provide_score,
            output_format=output_format,
            verbosity_level=verbosity_level,
        )


class AssociationRuleModelTransformer(Model):
    """
    AssociationRule transformer

    Attributes
    ----------
    model:
        trained association rule model.

    candidate_count: int, default = 10
        number of top candidates

    min_lift: float, default = 1.2
        minimum value of lift required for recommendations

    target_item: int or str, default = None
        Specify if want prediction for a single item.

    item_col: str, default = "item_id"
        filed name for item in the output.

    rec_col: str, default = "recommendations"
        filed name for recommendations in the output.

    score_col: str, default = "score"
        filed name for score in the output.

    provide_score: bool, default = False
        Set to True if desire score in the output.

    output_format: str， default = "json"
        Declare Output format.("json", "dataframe")

    verbosity_level: int, default=1
        an int parameter to control the log information
        only log running time when verbosity_level is 1
    """

    candidate_count = Param(
        Params._dummy(), "candidate_count", "number of top candidates"
    )
    min_lift = Param(
        Params._dummy(),
        "min_lift",
        "minimum value of lift required for recommendations",
    )
    target_item = Param(
        Params._dummy(), "target_item", "Specify if want prediction for a single item"
    )
    item_col = Param(
        Params._dummy(),
        "item_col",
        "filed name for item in the output.",
    )
    rec_col = Param(
        Params._dummy(),
        "rec_col",
        "filed name for recommendations in the output.",
    )
    score_col = Param(
        Params._dummy(),
        "score_col",
        "filed name for score in the output.",
    )
    provide_score = Param(
        Params._dummy(),
        "provide_score",
        "Set to True if desire score in the output.",
    )
    output_format = Param(
        Params._dummy(),
        "output_format",
        "Declare Output format.('json', 'dataframe')",
    )

    model = Param(Params._dummy(), "model", "trained Association Rule model.")
    verbosity_level = Param(
        Params._dummy(),
        "verbosity_level",
        "verbosity_level to control logger",
    )

    @keyword_only
    @logger
    def __init__(
        self,
        model,
        candidate_count,
        min_lift,
        target_item,
        item_col,
        rec_col,
        score_col,
        provide_score,
        output_format,
        verbosity_level,
    ):
        """
        initialize parameters
        """
        super(AssociationRuleModelTransformer, self).__init__()
        # enable kwargs
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(
        self,
        model,
        candidate_count,
        min_lift,
        target_item,
        item_col,
        rec_col,
        score_col,
        provide_score,
        output_format,
        verbosity_level,
    ):
        """Set params."""
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    @logger
    def _transform(self, dataset=None):
        """
        perform transformation of model result to desired format.

        Parameters
        ----------
        dataset: None
        """
        # prepare params
        model = self.getOrDefault(self.model)
        candidate_count = self.getOrDefault(self.candidate_count)
        min_lift = self.getOrDefault(self.min_lift)
        target_item = self.getOrDefault(self.target_item)
        item_col = self.getOrDefault(self.item_col)
        rec_col = self.getOrDefault(self.rec_col)
        score_col = self.getOrDefault(self.score_col)
        provide_score = self.getOrDefault(self.provide_score)
        output_format = self.getOrDefault(self.output_format)

        assert output_format in (
            "dict",
            "json",
            "dataframe",
        ), "The format not supported."

        # filter out rules with antecedent or consequent larger than 1 and has lift < min_lift
        rules = model.associationRules.where(
            (size(col("antecedent")) == 1)
            & (size(col("consequent")) == 1)
            & (col("lift") >= min_lift)
        )
        # convert column type from list to atomic data types.
        rules = rules.withColumn("consequent", rules.consequent[0]).withColumn(
            "antecedent", rules.antecedent[0]
        )
        # group by antecedent and collect list of (item, lift).
        w = Window.partitionBy("antecedent").orderBy(desc("lift"), "consequent")

        # generate sorted results in spark dataframe type.
        sorted_results = (
            rules.withColumn(
                rec_col, f.collect_list(col("consequent").cast("string")).over(w)
            )
            .withColumn(score_col, f.collect_list("lift").over(w))
            .groupBy("antecedent")
            .agg(f.max(rec_col).alias(rec_col), f.max(score_col).alias(score_col))
            .select(
                col("antecedent").cast("string").alias(item_col), rec_col, score_col
            )
        )

        # Keep top candidate_count candidates.
        sorted_results = sorted_results.withColumn(
            rec_col,
            f.slice(rec_col, start=1, length=candidate_count),
        ).withColumn(
            score_col,
            f.slice(score_col, start=1, length=candidate_count),
        )

        # select only the target item if target_item is specified.
        if target_item:
            assert target_item in list(
                sorted_results.select(item_col).toPandas()[item_col]
            ), "item not found"
            sorted_results = sorted_results.filter(
                sorted_results.item_id == target_item
            )

        # if provide_score is False, filter out the score column.
        if not provide_score:
            sorted_results = sorted_results.select(item_col, rec_col)

        return format_output_result(
            df=sorted_results, output_format=output_format, dict_key=item_col
        )
