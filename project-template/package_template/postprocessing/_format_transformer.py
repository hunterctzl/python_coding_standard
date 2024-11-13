import pyspark


def format_output_result(
    df: pyspark.sql.DataFrame,
    output_format: str,
    dict_key: str,
):
    """
    Transform output format into "json", "dict", or "dataframe"

    Parameters
    ----------
    df: pyspark.sql.DataFrame. The recommendation result
    output_format: str. The output format. Should be "json", "dict", or "dataframe"
    dict_key: str. The column name in df that will be used as dictionary key

    Returns
    -------
    The formatted recommendation result
    """
    if output_format == "json":
        df = df.toPandas().to_dict("records")
    elif output_format == "dict":
        df = df.toPandas()
        df.index = df[dict_key]
        df.drop(dict_key, inplace=True, axis=1)
        df = df.to_dict("index")
    return df
