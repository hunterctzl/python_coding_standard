"""
Purchase together pipeline in pyspark.
Covert code in to Pipeline.
"""
from package_template.preprocessing import ShoppingListTransformer
from package_template.models import AssociationRuleModel
from package_template.postprocessing import ScoreNormalization
from pyspark.ml import Pipeline
from pyspark.ml import Estimator
from pyspark.ml.param import Param
from pyspark.ml.param import Params
from pyspark import keyword_only

from package_template.utils import logger


class PurchaseTogetherPipeline(Estimator):
    """
    Provide ShoppingListTransformer, AssociationRuleModel, and ScoreNormalization
    to provide recommendations for purchased together pipeline.
    """

    # use Param function to define parameters
    transaction_col = Param(
        Params._dummy(),
        "transaction_col",
        "Provide the name of the column of transaction",
    )
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
    # @logger
    def __init__(
        self,
        transaction_col: str,
        item_list_col: str,
        min_support: float = 0.002,
        min_confidence: float = 0.2,
        min_lift: float = 1.2,
        candidate_count: int = 50,
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
        transaction_col: str
            Provide the name of the column of transaction.
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
        >>> from package_template.pipeline import PurchaseTogetherPipeline
        >>> spark = SparkSession.builder.appName("test_purchase_together_pipeline").getOrCreate()
        >>> df = spark.createDataFrame(
        ...    [
        ...       [1, 'A'],
        ...       [1, 'B'],
        ...       [1, 'C'],
        ...       [2, 'A'],
        ...       [2, 'B'],
        ...       [3, 'A'],
        ...       [3, 'C'],
        ...       [4, 'C'],
        ...       [4, 'D'],
        ...       [4, 'E'],
        ...       [5, 'A'],
        ...       [5, 'B'],
        ...       [6, 'A'],
        ...       [6, 'B']
        ...   ],
        ...   ['trans_id', 'item_id']
        ... )
        >>> pipeline = PurchaseTogetherPipeline(
        ...        transaction_col="trans_id",
        ...        item_list_col="shopping_list",
        ...        item_col="item_id",
        ...        min_support=0.2,
        ...        min_confidence=0.2,
        ...        min_lift=0.5,
        ...        rec_col = "recommendations",
        ...        output_format="dataframe",
        ...        provide_score=True,
        ...        candidate_count=3,
        ...    )
        >>> result = pipeline.fit(df).transform(df)
        >>> result.show()
        +-------+---------------+----------+
        |item_id|recommendations|     score|
        +-------+---------------+----------+
        |      A|         [B, C]|[1.0, 0.0]|
        |      B|            [A]|     [1.0]|
        |      C|            [A]|     [0.0]|
        +-------+---------------+----------+

        """
        super(PurchaseTogetherPipeline, self).__init__()

        self._setDefault(min_support=0.002)
        self._setDefault(min_confidence=0.2)
        self._setDefault(min_lift=1.2)
        self._setDefault(candidate_count=5)
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
        transaction_col,
        item_list_col,
        min_support=0.002,
        min_confidence=0.2,
        min_lift=1.2,
        candidate_count=5,
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
        Fits a pipeline to the input dataset.
        This is called by the default implementation of fit.
        Parameters
        ----------
        df: pyspark.sql.DataFrame
            Input transaction dataset with transaction id and shopping list.
        """
        # prepare params
        transaction_col = self.getOrDefault("transaction_col")
        item_list_col = self.getOrDefault("item_list_col")
        min_support = self.getOrDefault("min_support")
        min_confidence = self.getOrDefault("min_confidence")
        min_lift = self.getOrDefault("min_lift")
        candidate_count = self.getOrDefault("candidate_count")
        item_col = self.getOrDefault("item_col")
        rec_col = self.getOrDefault("rec_col")
        score_col = self.getOrDefault("score_col")
        provide_score = self.getOrDefault("provide_score")
        output_format = self.getOrDefault("output_format")
        num_limit_in_cart = self.getOrDefault("num_limit_in_cart")
        verbosity_level = self.getOrDefault("verbosity_level")


        transformer = ShoppingListTransformer(
            transaction_col=transaction_col,
            item_col=item_col,
            output_col=item_list_col,
            verbosity_level=verbosity_level,
        )
        model = AssociationRuleModel(
            item_list_col=item_list_col,
            min_support=min_support,
            min_confidence=min_confidence,
            min_lift=min_lift,
            output_format="dataframe",
            provide_score=True,
            candidate_count=candidate_count,
            num_limit_in_cart=num_limit_in_cart,
            verbosity_level=verbosity_level,
        )
        score_transformation = ScoreNormalization(
            group_col=item_col,
            rec_col=rec_col,
            score_col=score_col,
            output_format=output_format,
            provide_score=provide_score,
            transformation_method='log',
            verbosity_level=verbosity_level,
        )
        # return Pipeline model
        return Pipeline(stages=[transformer, model, score_transformation]).fit(df)

