
import datetime as dt
import datatable
from datatable import f, by
import difflib
import numpy as np


if False:
    # Sample Datatable Usages
    dt_table = datatable.Frame({"x1": [100, 100, 3], "x2": [100, None, 3], "y": ["1", "1", "2"], "wgt": [8, 8, 5]})
    dt_table[:, {"wgt_total": datatable.sum(f["wgt"])}, by(["x1", "y"])]  # group by and sum up
    dt_table[:, {"wgt_total": datatable.rowsum(f["wgt", "x2"])}, by(["x1", "y"])]  # add up columns wgt and x2 for each row


def to_vals(dt_table: datatable.Frame, col: str) -> np.ndarray:
    """ Get the value of datatable into np.array

    Parameters
    ----------
    dt_table : datatable.Frame
        The datatable
    col : str
        The column to query

    Returns
    -------
    np.ndarray

    Examples
    --------
    >>> dt_table = datatable.Frame({"x":[1,2,3],"y":["a","b","c"],"z":["d","e","f"]})
    >>> to_vals(dt_table, "x")
    """
    return dt_table[col].to_numpy().reshape(-1,)


def rename_cols(dt_table: datatable.Frame, column_mappings: dict, inplace: bool = True):
    """ Rename datatable column names

    Parameters
    ----------
    dt_table : datatable.Frame
        datatable
    column_mappings : dict
        The mapping of column names to new column names
    inplace : bool, optional
        In-place operation or not on the datatable. The default is True.

    Returns
    -------
    tb : datatable
        updated datatable with new names

    Examples
    --------
    >>> dt_table = datatable.Frame({"x":[1,2,3],"y":["a","b","c"],"z":["d","e","f"]})
    >>> column_mappings = {"x":"x2", "z":"z2","a":"b"}
    >>> rename_cols(dt_table, column_mappings, inplace=False)
    """
    keys = list(column_mappings.keys())
    names = dt_table.names
    if inplace:
        tb = dt_table
    else:
        tb = dt_table[:, :]
    for k in keys:
        if k not in names:
            column_mappings.pop(k)
    if column_mappings == {}:
        return tb
    else:
        tb.names = column_mappings
        return tb


def force_col_type(dt_table: datatable.Frame, col: str, col_type: type, inplace: bool = True):
    """ Enforce the column date type for datatable

    Parameters
    ----------
    dt_table : datatable.Frame
        datatable
    col : str
        column name
    col_type : type
        the column type to force, it has to be one of str, int and dt.date
    inplace : bool, optional
        inplace operation or not. The default is True.

    Returns
    -------
    datatable.Frame
        resulting datatable

    Examples
    --------
    >>> dt_table = datatable.Frame({"x":[100000000000,200,3],"y":["1","2","3"],"z":["2020-11-12", "2020-11-01", "2020-02-12"]})
    >>> col = "y"
    >>> col_type = int
    >>> force_col_type(dt_table, col, col_type, inplace=False)
    >>> col = "z"
    >>> col_type = dt.date
    >>> force_col_type(dt_table, col, col_type, inplace=True)
    """
    if dt_table.nrows == 0:
        return dt_table
    if col_type not in [str, int, float, dt.date]:
        raise ValueError("Column type {} is NOT one of [str, int, float, dt.date]".format(str(col_type)))
    if inplace:
        tb = dt_table
    else:
        tb = dt_table[:, :]
    x = tb[col]
    x2 = x[:1, :]
    if col_type == dt.date:
        col_type = datatable.stype.date32
    if x2.stype != x2[:, datatable.as_type(x2, col_type)].stype:
        tb[:, datatable.update(**{col: datatable.as_type(f[col], col_type)})]
    return tb


def weighted_avg(dt_table: datatable.Frame, groupby_cols: list, cols: list, weight_col: str = None, ignore_missing_val: bool = True) -> datatable.Frame:
    """ Weighted Average for datatable

    Parameters
    ----------
    dt_table : datatable.Frame
        datatable for aggregate.
    groupby_cols : list<str>
        list of column names to group by.
    cols : list<str>
        list of column names to calculate weighted average.
    weight_col : str, optional
        the column name of weights. The default is None. When weight is None, it calculates straight average
    ignore_missing_val: bool, optional
        If aggregate variable has missing, this indicator removes the value in the calculation.

    Returns
    -------
    datatable.Frame
        The resulting weighted average datatable

    Examples
    --------
    >>> dt_table = datatable.Frame({"x1":[100,200,3],"x2":[100,None,3],"y":["1","1","2"],
        "z":["2020-11-12", "2020-11-12", "2020-02-12"], "wgt":[8,4,5]})
    >>> groupby_cols = ["y","z"]
    >>> cols = ["x1", "x2"]
    >>> weight_col = None
    >>> weighted_avg(dt_table, groupby_cols, cols, weight_col=None)
    >>> weighted_avg(dt_table, groupby_cols, cols, weight_col="wgt")
    """
    allcols = cols + groupby_cols
    allcols = allcols if weight_col is None else allcols + [weight_col]
    tb = dt_table[:, list(set(allcols))]
    if weight_col is None:
        weight_col = "_zwgzgw"
        tb[weight_col] = 1.
    tb[f[weight_col] == None, weight_col] = 0
    tb[:, datatable.update(**{weight_col: datatable.as_type(f[weight_col], float)})]  # convert weight to float
    # get the formula for weighted average
    if ignore_missing_val:
        cal_formula = {c+"_avg": datatable.sum((f[c] * f[weight_col]))/datatable.sum(f[weight_col] * (1.-datatable.isna(f[c]))) for c in cols}
    else:
        cal_formula = {c+"_avg": datatable.sum((f[c] * f[weight_col]))/datatable.sum(f[weight_col]) for c in cols}
    if weight_col != "_zwgzgw":
        cal_formula.update({weight_col: datatable.sum(f[weight_col])})
    return tb[:, cal_formula, by(groupby_cols)]


def sort_values(dt_table: datatable.Frame, by: list, ascending: list = None):
    """ Sort datatable by columns specified in ascending or descending order

    Parameters
    ----------
    dt_table : datatable.Frame
        The source datatable
    by : list
        The list of columns datatable to sort by
    ascending : list, optional
        The list of True or False to specify which column is sorted ascending order or descending order. The default is None.

    Returns
    -------
    datatable.Frame
        The sorted datatable.

    Examples
    -------
        >>> dt_table = datatable.Frame({"x1":[100,100,3],"x2":[100,None,3],"y":["1","1","2"], "z":["2020-11-12", "2020-11-12", "2020-02-12"], "wgt":[8,4,5]})
        >>> sort_values(dt_table, by=["x1", "wgt"], ascending=[False, False])
    """
    if ascending is None:
        ascending = [True] * len(by)
    cols2sort = tuple([f[c] if ascending[i] else -f[c] for i, c in enumerate(by)])
    return dt_table[:, :, datatable.sort(*cols2sort)]


def join_table(tb1: datatable.Frame, tb2: datatable.Frame, on: list = None, how: str = "left", inplace: bool = False):
    """ This is the same as pd.merge for merging two tables tb1, tb2 based on the joint columns

    Parameters
    ----------
    tb1 : datatable.Frame
        Main datatable
    tb2 : datatable.Frame
        The second datatable (served on the right side of join) to join on main table tb1
    on : list, optional
        The list of columns used as key to join tables
    how : str, optional
        Specify whether it's left join or inner join. The default is "left".
    inplace : bool, optional
        Whether the operations are in place, this will change the source tables. The default is False.

    Returns
    -------
    datatable.Frame
        The resulting datatable

    Examples
    -------
        >>> tb1 = datatable.Frame({"x1":[100,200,3],"x2":[100,None,3],"y":["1","1","2"], "z":["2020-11-12", "2020-11-12", "2020-02-12"], "wgt":[8,4,5]})
        >>> tb2 = datatable.Frame({"x1":[100,200], "wgt2":[8,4]})
        >>> join_table(tb1, tb2, how="left")
    """
    if on is None:
        on = list(set(tb1.names) & set(tb2.names))
    if how not in ["left", "inner"]:
        assert ValueError("The how parameter in the table joins must be one of ['left','inner']")
    if inplace:
        tb1c, tb2c = tb1, tb2
    else:
        tb1c, tb2c = tb1[:, :], tb2[:, :]
    if isinstance(on, str):
        on = [on]
    tb2c.key = tuple(on)
    try:
        tb1c.key = tuple(on)
    except ValueError:
        pass  # this means the table 1 tb1 are not row-unique for columns for columns in list `on`
    if how == "inner":
        tb2c["___zwgzgw"] = 1
    if how == "left":
        return tb1c[:, :, datatable.join(tb2c)]
    elif how == "inner":
        out_tb = tb1c[datatable.g["___zwgzgw"] == 1, :, datatable.join(tb2c)][:, f[:].remove(f["___zwgzgw"])]
        if inplace:
            del tb2c[:, "___zwgzgw"]
        return out_tb


def drop_cols(dt_table: datatable.Frame, cols2drop: list):
    """ Drop the columns in the datatable. If the columns do not exist, skip

    Parameters
    ----------
    dt_table : datatable.Frame
        datatable to drop
    cols2drop : list<str>
        list of column names to drop
    inplace: bool, optional
        specify the in-place optional or not

    Returns
    -------
    datatable.Frame
        The resulting datatable.
    """
    cols2drop = list(set(cols2drop) & set(dt_table.names))
    if len(cols2drop) == 0:
        return dt_table
    else:
        return dt_table[:, f[:].remove(f[cols2drop])]


def drop_duplicates(dt_table: datatable.Frame, subset: list = None, inplace: bool = True):
    """ The same as pandas drop duplicates operation. Based on the subset column, drop any row that is duplicate of the subset column, only keep
        the first row when there are duplicates.

    Parameters
    ----------
    dt_table : datatable.Frame
        The datatable to operate on
    subset : list, optional
        The subset of the columns where we'll drop the duplicate rows if the same subset column values appear. If None, then we drop duplicate of all table columns. The default is None.
    inplace : bool, optional
        Specify it's inplace operation or not. The default is True.

    Returns
    -------
    datatable.Frame
        The resulting datatable

    Examples
    -------
        >>> dt_table = datatable.Frame({"x1":[100,100,3],"x2":[100,None,3],"y":["1","1","2"], "z":["2020-11-12", "2020-11-12", "2020-02-12"], "wgt":[8,4,5]})
        >>> drop_duplicates(dt_table, subset=["x1"])
        >>> drop_duplicates(rbind(dt_table,dt_table))
    """
    cols = list(dt_table.names)
    if subset is None:
        return dt_table[:, datatable.count(), by(f[cols])][:, :-1]
    if inplace:
        tb = dt_table
    else:
        tb = dt_table[:, :]
    tb["___zdpaiof"] = np.arange(tb.shape[0])
    t2 = join_table(tb, tb[:, datatable.min(f["___zdpaiof"]), by(subset)], how="inner")
    if inplace:
        del tb[:, "___zdpaiof"]
    t2 = t2[:, f[:].remove(f["___zdpaiof"])]
    return t2[:, cols]


def rbind(tb1: datatable.Frame, tb2: datatable.Frame, force: bool = False, bynames: bool = True, force_same_col_type: bool = True, inplace: bool = True):
    """ Datatable row bind. This is equivalent to pd.concat((df1, df2)).

    Parameters
    ----------
    tb1 : datatable.Frame
        First datatable in the row bind
    tb2 : datatable.Frame
        Second datatable in the row bind
    force : bool, optional
        Whether to force to join. In case if columns are different, force=True will create all possible columns.
        This is option from datatable.rbind. The default is False.
    bynames : bool, optional
        Whether to row combine by names. This is option from datatable.rbind. The default is True.
    force_same_col_type : bool, optional
        This forces columns that are different types like num vs char to char. The default is True.
    inplace: bool, optional
        This defines it's inplace option or not

    Returns
    -------
    datatable.Frame

    """
    if inplace:
        tb1c, tb2c = tb1, tb2
    else:
        tb1c, tb2c = tb1[:, :], tb2[:, :]
    if not force_same_col_type:
        return datatable.rbind(tb1c, tb2c, force=force, bynames=bynames)
    commonnames = list(set(tb1.names) & set(tb2.names))
    chartypes = [datatable.stype.str32, datatable.stype.str64]
    for c in commonnames:
        type1, type2 = tb1c[c].stype, tb2c[c].stype
        if type1 == type2:
            continue
        else:
            if type1 in chartypes:
                tb2c[:, datatable.update(**{c: datatable.as_type(f[c], str)})]
            if type2 in chartypes:
                tb1c[:, datatable.update(**{c: datatable.as_type(f[c], str)})]
    return datatable.rbind(tb1c, tb2c, force=force, bynames=bynames)


def is_column_in_datatable(dt_table: datatable.Frame, col: str) -> bool:
    """ Check if column excists in the data, even column exists but all values are None, then drop it

    Parameters
    ----------
    dt_table : datatable.Frame
        datatable to drop
    col : str
        The column to check its existence

    Returns
    -------
    bool
        is column in the data or not
    """
    if col not in dt_table.names:
        return False
    if dt_table[f[col] == None, :].shape[0] == dt_table.shape[0]:
        return False
    try:
        if dt_table[f[col] == "", :].shape[0] == dt_table.shape[0]:
            return False
    except:
        pass
    return True


def clear_df_column_names(x):
    """ Universal method for clearing the data frame column names

    Args:
        x (str): column name
    Returns:
        str: Cleared column name
    """
    x = x.replace("(", "_").replace(")", "_").replace(
        "/", "").replace("'", "").replace("'", "").replace('"', "").replace("&", "").replace("%", "")
    x = x.lower().strip().replace("  ", " ").replace("  ", " ").replace(
        " ", "_").replace("-", "_").replace(")", "")
    x = x.replace("__", "_").strip()
    if x.endswith("_"):
        x = x[:-1]
    return x


def find_closest_variable(dt_table: datatable.Frame, col: str, similarity_cutoff: float = 0.8) -> str:
    """ Find the closest variable name for the datatable for a given column name col

    Parameters
    ----------
    dt_table : datatable.Frame
        The source datatable.
    col : str
        The column name to find in datatable dt_table with closest match
    similarity_cutoff : str, optional
        The similiarity cutoff search. 0-1, where 1 being 100% match. The default is 0.8.

    Returns
    -------
    str
        The actual column name that is closed to the reference column name

    Examples
    --------
    >>> col = "CIO Line of Business"
    >>> dt_table = datatable.Frame({"cio line of busi":["a","b"],"cio line":[1,2]})
    >>> find_closest_variable(dt_table, col, similarity_cutoff=0.8)
    """
    cols_actu = dt_table.names
    cols_clean = [clear_df_column_names(x).replace("_", "").strip() for x in cols_actu]
    col = clear_df_column_names(col).replace("_", "").strip()
    col_match = difflib.get_close_matches(col, cols_clean, cutoff=similarity_cutoff)
    if len(col_match) > 0:
        try:
            col_actual = cols_actu[cols_clean.index(col_match[0])]
            return col_actual
        except:
            pass
    return None


def default_nullval_to_blank(dt_table: datatable.Frame, blank_val="", inplace: bool = True):
    """ Default the NULL values in the string column to blank ''

    Parameters
    ----------
    dt_table : datatable.Frame
        source datatable

    Returns
    -------
    datatable.Frame
        resulting datatable with corrected null values in string column.
    """
    if not inplace:
        tb = dt_table[:, :]
    else:
        tb = dt_table
    if blank_val not in ["", 0]:
        raise ValueError("The blank_val for the default null value needs to be one of ['', 0]")
    if blank_val == "":
        for col in tb.names:
            try:
                blank_expr = (f[col] == "None") | (f[col] == None) | (f[col] == "#N/A") | (f[col] == "none") | (f[col] == "#NA") | (f[col] == "nan") | (f[col] == "NULL") | (f[col] == "N/A")
                tb[blank_expr, col] = blank_val
            except TypeError:
                #print(f"Column `{col}` is not a string column")
                pass
    elif blank_val == 0:
        for col in tb.names:
            try:
                tb[datatable.isna(f[col]), col] = blank_val
            except TypeError:
                #print(f"Column `{col}` is not a string column")
                pass
    return tb
