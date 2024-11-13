"""
Shopping List Transformer
Transform the input dataset to the format that FP Growth accept.
"""
from package_template.utils import logger
from pyspark import keyword_only
from pyspark.ml import Transformer
from pyspark.ml.param import Param
from pyspark.ml.param import Params
from pyspark.sql import functions as f


class ShoppingListTransformer(Transformer):
    """
    Transform the input dataset to shopping list format that FP Growth accept.
    It contains trainsaction id and list of items in the transaction.
    """

    # use Param function to define parameters
    transaction_col = Param(
        Params._dummy(),
        "transaction_col",
        "Provide the name of the column of transaction",
    )
    item_col = Param(
        Params._dummy(),
        "item_col",
        "Provide the name of the column of item ID",
    )
    output_col = Param(
        Params._dummy(), "output_col", "Provide the name of the output shopping list"
    )
    verbosity_level = Param(
        Params._dummy(),
        "verbosity_level",
        "verbosity_level to control logger",
    )

    # initiate parameters
    @keyword_only
    @logger
    def __init__(
        self,
        transaction_col: str,
        item_col: str,
        output_col: str,
        verbosity_level: int = 1,
    ):
        """
        initialize parameters

        Parameters
        ----------
        transaction_col: str
            Provide the name of the column of transaction.
        item_col: str
            Provide the name of the column of item ID.
        output_col: str
            Provide the name of the output shopping list
        verbosity_level: int, default=1
            an int parameter to control the log information
            only log running time when verbosity_level is 1

        Example
        -------
        >>> from pyspark.sql import SparkSession
        >>> from pyspark_recommender.features import ShoppingListTransformer
        >>> import pandas as pd
        >>> spark = SparkSession.builder.appName("test_association_rule").getOrCreate()
        >>> df = pd.DataFrame([['T1', 'I1'], ['T1', 'I2'], ['T1', 'I3'],
        ... ['T2', 'I1'], ['T2', 'I2']], columns=['trans_id', 'item_id'])
        >>> df = spark.createDataFrame(df)
        >>> transformer = ShoppingListTransformer(transaction_col="trans_id",
        ...                        item_col="item_id", output_col="shopping_list")
        >>> result = transformer.transform(df)
        >>> result.show(truncate=False)
        +--------+-------------+
        |trans_id|shopping_list|
        +--------+-------------+
        |      T1| [I2, I3, I1]|
        |      T2|     [I2, I1]|
        +--------+-------------+
        """
        # inherit init from parent class
        super(ShoppingListTransformer, self).__init__()
        self._setDefault(verbosity_level=1)
        # enable kwargs
        kwargs = self._input_kwargs
        self._set(**kwargs)

    # inherit the setParams function, users can change parameters
    @keyword_only
    def setParams(
        self,
        transaction_col,
        item_col,
        output_col,
        verbosity_level,
    ):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    # define the transform function, write your main function here.
    @logger
    def _transform(self, df):
        """
        perform transformation of input dataset to desired format.

        Parameters
        ----------
        df: pyspark.sql.DataFrame
            input dataset.

        Returns
        -------
        result: pyspark.sql.DataFrame
            shopping-list format dataframe.
            e.g.
            +--------+-------------+
            |trans_id|shopping_list|
            +--------+-------------+
            |      T1| [I2, I3, I1]|
            |      T2|     [I2, I1]|
            +--------+-------------+
        """
        # prepare params
        transaction_col = self.getOrDefault("transaction_col")
        item_col = self.getOrDefault("item_col")
        output_col = self.getOrDefault("output_col")

        # aggregation function
        result = df.groupby(transaction_col).agg(
            f.collect_set(item_col).alias(output_col)
        )

        return result
