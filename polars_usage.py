
import datetime as dt
import numpy as np
import polars as pl


df = pl.DataFrame({"fruits": ["banana", "banana", "apple", "apple", "banana"],
                   "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
                   "A": [1, 2, 3, 4, 5],
                   "B": [5, 4, 3, 2, 1],
                   "C": [True, True, False, True, False],
                   "birthday": pl.Series(["2000-12-01"]*5)})

#
df_pd = df.to_pandas()  # convert to the pandas dataframe
pl.from_pandas(df_pd)  # convert pandas dataframe to polars

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use columns Fruits, Cars, and create new columns in Select statement, at the end, sort rows by Cars, Fruits
df.sort(["cars", "fruits"]).select(["fruits", "cars",
                                    pl.lit("fruits!").alias("literal_string_fruits"),  # just assign "fruits!" value to the new column "literal_string_fruits"
                                    pl.col("B").filter(pl.col("cars") == "beetle").sum(),  # new column B where sum up column B values for all rows with cars==bettle
                                    # sum of column A by column cars where column B > 2, then merge data to original data on column cars
                                    pl.col("A").filter(pl.col("B") > 2).sum().over("cars").alias("sum_A_by_cars"),
                                    pl.col("A").sum().over("fruits").alias("sum_A_by_fruits"),  # sum of column A by column fruits then merge data to original data on column fruits
                                    pl.col("A").reverse().over("fruits").alias("rev_A_by_fruits"),  # reverse column A by column fruits, then merge data to the original data on column fruits
                                    pl.col("A").sort_by("B").over("fruits").alias("sort_A_by_B_by_fruits"),  # sort column A by column B by column fruits
                                    ])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
assert len(df) == df.shape[0]  # get the num of rows
df.lazy().fetch(4) == df.head(4)  # get the first 4 rows, but fetch is on lazy operation
print("Try to use .lazy() and .collect() in the code for faster optimized operation")
print("The pl.Series to_numpy operation is slow, try to stick to pl.Series for faster data processing")
df.columns  # check columns
df.dtypes  # check data types
df.select(["A", "fruits"])  # select on two columns A, fruits
df.lazy().select(["A", "fruits"]).collect()  # create lazy dataframe so that at the end using .collect() to execute in order to optimize the query
df.select(pl.col(pl.Int64))  # get all Int64 columns
df.select([pl.col(pl.Utf8)])  # get all str columns
df.select(pl.col(["fruits", "A"]).sort_by("A"))  # sort by column A and select two columns fruits, A
df["fruits"].to_numpy()  # get the value of columns into numpy array, this is slow, try to pl.Series df["fruits"] directly for calculations
df.columns = ["a", "b", "c", "d"]  # rename all columns to a,b,c,d
df.filter((pl.col("fruits").is_in(["banana", "apple"])) | (pl.col("A") > 3))  # choose either fruits=='banana' or column A > 3. Use & for and operattion
df.unique(subset=["fruits"], keep="first")  # same as pandas drop_duplicates, where we select unique row for each value in column fruits, but use first row and remove rest of duplicates
df.unique()  # drop all duplicate rows to select unique row
df.filter(pl.lit(~df.is_duplicated()))  # remove the rows that have duplicate rows
df.filter(~pl.col(["A"]).is_duplicated())  # remove the rows where column A have duplicate rows (if use column fruits, all rows are gone since banana and apple both have repeated)
df[np.arange(2), :]  # choose the index values of np.arange(1,2)
df[np.arange(2), ["fruits", "B"]]  # choose the index values of np.arange(1,2)
pl.concat((df, df)) # stack two dataframes vertically. Add optional how="horizontal", "vertical", "diagonal" for column combine, row combine and diagonal being flexible row combine
df.vstack(df) # another way to do vertical dataframe row combine, this is faster, but require same columns
df.sample(10) # get random sample of 10 rows
df2 = df.clone(); df2 = df2.cleared(); del df2 # to remove/delete the dataframe object, it's large and just del df can make memory swell
pl.DataFrame({"foo": [1, 2, 3], "bar": [6, None, 8]}).lazy().drop_nulls(subset=["bar"]).collect() # drop the rows having null values for columns, say bar in this case
df.fill_nan(99) # fill NaN values with value 99, fill_null for None values
df.insert_at_idx(1, pl.Series("rowidx", np.arange(len(df)))) # add a new column rowidx as the 2nd (index 1 there) column
df.select([pl.all(), pl.col("A").reverse().over("fruits").suffix("_reverse")]) # add A_reverse column with column A reversed by column fruits
df.slice(1,3) # get sub dataframe from row index 1 and total 3 rows, use df.slice(1,None) for getting all rows from row index 1 to end
df.with_columns([pl.col("A").diff().over("fruits").alias("A_diff_by_fruits")]) # add difference of column A from previous A value given column "fruits" current value
df.with_columns([((dt.datetime.now()-pl.col("birthday")).dt.days()/365.25).floor().cast(pl.Int64).alias("age")]) # get the age from column birthday (date)
df.with_column(pl.repeat("audi",len(df)).alias("car_new")) # create a new column (could be replacement of an old column) 'car_new' with only value "audi"

# the following are some simple pl.Series operations
s_fruits, s_cars = df["fruits"], df["cars"]
s_fruits.set(s_fruits == "banana", "orange") # reset fruits pl.Series value to 'orange' on index where fruits pl.Series == 'banana'
s_fruits.set_at_idx(np.array([2,4]), "orange") # reset fruits pl.Series value to orange on index 2,4
s_fruits.take(np.array([2,4])) # take subset of fruits pl.Series at index 2,4
s_fruits.zip_with(s_cars=="audi", s_cars) # this is little weird, take fruits pl.Series when cars pl.Series=='audi', if not 'audi', take values from another pl.Series, df["cars"]

# create a pivot table of two columns (row as foo, column as bar), aggregate column baz values by sum
df = pl.DataFrame({"foo": ["one", "one", "one", "two", "two"], "bar": ["A", "B", "A", "A", "B"], "baz": [1, 2, 3, 7, 4]})
df.pivot(values="baz", index="foo", columns="bar", aggregate_fn="sum")

# cut the age series into bins (the result is a pl.DataFrame)
s_age = pl.Series("age", [7,23,28,35,float("NaN")])
pl.cut(s_age, bins=[20,30], labels=["1) <20", "2) 20-30", "3) 30+"], category_label="age_bin") # NaN value converted to bin value None

# get the date range
pl.date_range(low=dt.datetime(2021, 12, 16), high=dt.datetime(2022, 1, 3), interval="2d") # get the list of dates for every 2 days, use interval='1mon' for every month, interval='30m' for every 30 mins

# get the rolling sum based on the date column dt, so each row is sum of values for dates within, say, 2 day window prior to current date
dates = ["2020-01-01 13:45:48", "2020-01-01 16:42:13", "2020-01-01 16:45:09", "2020-01-02 18:12:48", "2020-01-03 19:45:32", "2020-01-08 23:16:43"]
df2 = pl.DataFrame({"dt": dates, "a": [3, 7, 5, 9, 2, 1]}).with_column(pl.col("dt").str.strptime(pl.Datetime))
df2.groupby_rolling(index_column="dt", period="2d").agg([pl.sum("a").alias("sum_a")])

# create pipeline to simplify the data creation
def cast_str_to_int(data:pl.DataFrame, c:str): # c is column name
    return data.with_column(pl.col(c).cast(pl.Float64))
df.pipe(cast_str_to_int, c="B")

# join two dataframes (gdp and pop) by date where each pop date is merged with nearest gdp date (searching backward)
gdp = pl.DataFrame({"date": [dt.datetime(2016, 1, 1), dt.datetime(2017, 1, 1), dt.datetime(2019, 1, 1)], "gdp": [4164, 4411, 4696]})
pop = pl.DataFrame({"date": [dt.datetime(2016, 5, 12), dt.datetime(2017, 5, 12), dt.datetime(2018, 5, 12), dt.datetime(2019, 5, 12)],
        "population": [82.19, 82.66, 83.12, 83.52]})
pop.join_asof(gdp, left_on="date", right_on="date", strategy="backward")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# COLUMN MANIPULATION
df.with_column(pl.Series([4, 2, 2, 5, 7]).alias("newcol"))  # assign the new column newcol the list of values, same as df["newcol"]=[4,2,2,5,7] in pandas dataframe
df.with_columns([pl.when(pl.col("cars").is_in(["beetle"])).then(pl.col("B")).otherwise(999)])  # assgn column B with value 999 if column cars is not "beetle"
df.with_column(pl.arange(0, df.shape[0]).alias("index")).select([pl.all(), pl.when(pl.col("index").is_in([1, 2])).then(100).otherwise(pl.col("B")).alias("new_col")])
#           add column called index, and create new column "new_col" where it's 100 if index value is in 1,2 othereise, assign by column B, pl.all()
#           is to just add all exisiting columns at beginning of all columns
df.with_columns([pl.col("fruits").alias("eatfruits"),  # add new column called 'eatfruits' by assigning fruits to it
                 # A_Sqr is column A square if fruits=banana, otherwise, assign column A sqaure root
                 pl.when((pl.col("fruits") == "banana")).then(pl.col("A") ** 2).otherwise(pl.col("A")**0.5).alias("A_Sqr"),
                 (pl.col("C").is_not()).alias("NotC")])  # add two new columns, "fruits" as "eatfruits" and "B" as "newcol"
df.rename(mapping={"B": "new_B"})  # rename the column B to new_B
df.with_columns([pl.Series(["2020-12-01"]*5).alias("timestamp").str.strptime(pl.Datetime, fmt="%F"), ]).drop(["A"])  # convert the string date to datetime, also drop column A
df.filter(pl.col("A").sum().over("fruits") < 8)  # get the rows with fruits whose total sum of column A < 8, in this case rows for apple are chosen
df.sort(["fruits", "A"], reverse=[True, True])  # sort data by columns fruits, A but both in descending order
print("The polars sort speed gets very slow when there are too many columns in the data")
df.with_columns([pl.arange(0,len(df)).alias("__zemtaq")]).select([pl.all(), pl.col("__zemtaq").min().over("fruits").alias("fruits_keyid")]).drop(["__zemtaq"])
                 # This is to assign an integer ID to each unqiue column "fruits" value, may use it for numba njit operation
df.lazy().groupby(["fruits", "cars"]).agg([pl.count(), pl.col("B").list(), pl.first("C"), pl.col("A").sum()]).sort(["count"], reverse=[True]).limit(5).collect()
#           group by columns fruits, cars, and do counts, list of B values, take first C value, add up column A values, and sort by count in descending order, take first 5 rows
df.lazy().groupby(["fruits"]).agg([(pl.col("cars") == "beetle").sum().alias("beetle_count")]).collect() # group by columns fruits, and count the num of column cars values being "beetle"
# group by columns fruits, and get average birthday for apple
def avg_birthday(fruit: str) -> pl.Expr:  # get the average birthday for given fruit
    return (dt.date(2021, 1, 1).year - pl.col("birthday").dt.year()).filter(pl.col("fruits") == fruit).mean().alias(f"avg {fruit} birthday")
df.with_columns([pl.col("birthday").str.strptime(pl.Datetime, fmt="%F"), ]).lazy().groupby(["fruits"]).agg([avg_birthday("apple"), ]).collect()

df.groupby(["fruits"]).agg([pl.col("cars").unique().len()])  # count unique num of cars group by fruits
df.select([pl.all(), pl.col("cars").unique().len().over("fruits").alias("unique_cars_count")])  # count unique num of cars group by fruits, and merge back to dataframe by column fruits

# add new mapped column, say, fruits_new by value mapping
value_mapping={"banana":111, "apple":222}
df.join(pl.DataFrame([(k, value_mapping[k]) for k in value_mapping],columns=["fruits","fruits_newvalue"], orient="row"), on=["fruits"], how="left")

# sort by birthday and group by fruits to concatenate columns A and B (by casting int to str)
def AandB() -> pl.Expr:
    return pl.col("A").cast(pl.Utf8) + pl.lit(" and ") + pl.col("B").cast(pl.Utf8)
df.sort(["birthday"], reverse=[True]).groupby(["fruits"]).agg([AandB().alias("AjoinB")])

# use regex to find the string values based on string pattern
df1 = pl.DataFrame({"words":["ret_gross_12q2","ret_net_12q2", "ret_apple"]})
df1.filter(pl.col("words").str.contains(r"ret_\w+[0-9]+q[0-9]+")) # find the ret*<num>q<num>

# Under each condition, apply multiple changes to the data. For exmaple, the following is
#    1) add 5 to current column A value, and add 2 to column A value to assign column B value when cars=='audi'
#    2) X 10 to current column A value for column C, and square column A value to assign column D value when cars=='toyota'
#    since the two pl.when statements are both in one with_columns statement, the column A value in calculation still uses old A value
#    even one of expressions changes A value during the same with_columns statement
df2 = pl.DataFrame({"cars": ["beetle", "audi", "toyota"], "A": [1, 2, 3], "B": [5, 9, 3]})
df2.with_columns([pl.Series([None]).alias("C"), pl.Series([None]).alias("D")]).with_columns([
        pl.when(pl.col("cars")=="audi").then(
            pl.struct([(pl.col("A")+5.).alias("A"),  # add 5 to column A
                       (pl.col("A")+2.).alias("B")]) # add 2 to column A as column B value
            ).otherwise(pl.struct(["A","B"])).alias("_newconstruct1"),
        pl.when(pl.col("cars") == "toyota").then(
            pl.struct([(pl.col("A")*10.).alias("C"),
                       (pl.col("A")**2.).alias("D")])
            ).otherwise(pl.struct(["C","D"])).alias("_newconstruct2"),
    ]).drop(["A","B","C","D"]).unnest(["_newconstruct1","_newconstruct2"])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATAFRAME JOINS/MERGES
df_trades = pl.DataFrame({"stock": ["A", "B", "B", "C"], "trade": [101, 299, 301, 500], })
df_q = pl.DataFrame({"stock": ["A", "B", "D"], "quote": [100, 300, 501], })
df_trades = df_trades.join(df_q, on=["stock"], how="left")  # join df_trades with df_q on column stock, use how="inner" for inner join, how="anti" for anti-join

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# WEIGHTED AVERAGE
# weighted average of trade by weight column quote group by stocks
df_trades.groupby(["stock"]).agg([((pl.col("trade")*pl.col("quote")).sum()/pl.col("quote").sum()).alias("avg_trade_weighted_by_quote")])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# SOME CUSTOMIZED FUNCITONS
#..............................................................

def pl_weighted_avg(df:pl.DataFrame, num_cols:list, weight_col:str, groupby_cols:list, add_effective_wgts:bool=True):
    """ Get weighted average of polars dataframe for numerical columns (num_cols) group by groupby_cols

    Parameters
    ----------
    df : pl.DataFrame
        Source dataframes.
    num_cols : list
        The numerical columns to aggregate data on.
    weight_col : str
        Weight column.
    groupby_cols : list
        Group By columns.
    add_effective_wgts : bool, optional
        Since it could be missing in either numerical field or weight column, enabling this option is to add the effective
        weight that are used in calculating weighted average by ignoring null values. The default is True.

    Returns
    -------
    pl.DataFrame
        Resulting DataFrame

    Examples
    -------
        >>> df = pl.DataFrame({"fruits": ["banana", "banana", "apple", "apple", "banana", "apple"],
                   "cost": [1, 2, 3, None, 5, None],
                   "wgt": [5, 4, 3, 2, None, None]})
        >>> pl_weighted_avg(df, num_cols=["cost"], weight_col="wgt", groupby_cols=["fruits"], add_effective_wgts=True)
    """
    if isinstance(num_cols, str):
        num_cols = [num_cols]
    if isinstance(groupby_cols, str):
        groupby_cols = [groupby_cols]
    allcols = groupby_cols+num_cols+[weight_col]
    if add_effective_wgts:
        return df.lazy().select(allcols).groupby(groupby_cols).agg([((pl.col(c)*pl.col(weight_col)).sum()/(~pl.col(c).is_null() * pl.col(weight_col)).sum()).alias(f"{c}_avg") for c in num_cols] + \
            [pl.col(weight_col).sum()] + [(~pl.col(c).is_null() * pl.col(weight_col)).sum().alias(f"eff_wgt_by_{c}") for c in num_cols]).collect()
    else:
        return df.lazy().select(allcols).groupby(groupby_cols).agg([((pl.col(c)*pl.col(weight_col)).sum()/(~pl.col(c).is_null() * pl.col(weight_col)).sum()).alias(f"{c}_avg") for c in num_cols] + \
            [pl.col(weight_col).sum()]).collect()


def force_vstack(df1:pl.DataFrame, df2:pl.DataFrame):
    """ This is upgraded verion for df1.vstack(df2), since this vstack is very stric on matching all
        column types and list of columns including order of columns, this function is to arrange data
        in df1, df2 in order to force the vstack

    Parameters
    ----------
    df1 : pl.DataFrame
        First dataframe to vstack (row combine) on
    df2 : pl.DataFrame
        Second dataframe to vstack (row combine) on

    Returns
    -------
    pl.DataFrame
        Resulting stacked dataframes

    Examples
    -------
        >>> df1 = pl.DataFrame({"a": ["foo", "bar", "ham"], "b": [1, 2, 3]})
        >>> df2 = pl.DataFrame({"a": ["foo", "spam", "eggs"], "c": [3, 2, 2]})
        >>> force_vstack(df1, df2)
    """
    newcols1 = set(df2.columns) - set(df1.columns)
    newcols2 = set(df1.columns) - set(df2.columns)
    df1_withcols_exp = []
    df2_withcols_exp = []
    if newcols1 != set():
        for c in newcols1:
            t = df2[c].dtype
            if t in [pl.Int64, pl.Int32, pl.Int16, pl.Int8]:
                df1_withcols_exp.append(pl.Series([None]).cast(pl.Float64).alias(c))
                df2_withcols_exp.append(pl.col(c).cast(pl.Float64))
            else:
                df1_withcols_exp.append(pl.Series([None]).cast(t).alias(c))
    if newcols2 != set():
        for c in newcols2:
            t = df1[c].dtype
            if t in [pl.Int64, pl.Int32, pl.Int16, pl.Int8]:
                df2_withcols_exp.append(pl.Series([None]).cast(pl.Float64).alias(c))
                df1_withcols_exp.append(pl.col(c).cast(pl.Float64))
            else:
                df2_withcols_exp.append(pl.Series([None]).cast(t).alias(c))
    df1 = df1.with_columns(df1_withcols_exp)
    df2 = df2.with_columns(df2_withcols_exp)
    return df1.vstack(df2.select(df1.columns))


def fast_query(df:pl.DataFrame, column:str, column_val, check_if_data_sorted:bool=True):
    """ When dealing with very large dataframe, we use this method for quick search to get the subset
        of dataframe where column value is specified

        Since polars sorting data is very slow, first need to sort data in order to do many quick searches

        This is same as df.loc[df[column]==column_val, :] in pandas, but this method is slow when dealing
        with lots of large searches

    Parameters
    ----------
    df : pl.DataFrame
        The source dataframe
    column : str
        The column to search value for
    column_val : str, float, int
        The value to search for
    check_if_data_sorted: bool, opitonal
        Perform a quick check on whether data is already sorted by column

    Returns
    -------
    pl.DataFrame
        Subset of the data where column values = column_val

    Examples
    -------
        >>> df = pl.DataFrame({"fruits": ["banana", "banana", "apple", "apple", "banana"], "A": [1, 2, 3, 4, 5]})
        >>> fast_query(df, column="fruits", column_val="banana") # get subset of data where column fruits == banana
    """
    if check_if_data_sorted:
        if (df[column] != df[column].sort()).sum() > 0:
            raise ValueError(f"The dataframe is not sorted by column {column}")
    vs = df[column].to_numpy()
    s, e = np.searchsorted(vs, column_val, side="left"), np.searchsorted(vs, column_val, side="right")
    if s >= e:
        return df.cleared()
    else:
        return df[s:e,:]


def upload_data_to_database(df:pl.DataFrame, conn, DB_tablename:str):
    """ Upload Polars dataframe data to the postgresql database

    Parameters
    ----------
    df : pl.DataFrame
        Data to upload
    conn :
        The connection to the DB
    DB_tablename:
        The table name on the DB for uploading data to

    Returns
    -------
    None.

    """
    from psycopg2 import sql
    import psycopg2.extras
    # first me convert polars date representation to python datetime objects
    #for col in df:
        # only for date
    #    if col.dtype == pl.Date:
    #        df = df.with_column(col.dt.to_python_datetime())
    # create sql identifiers for the column names
    # we do this to safely insert this into a sql query
    columns = sql.SQL(",").join(sql.Identifier(name) for name in df.columns)
    # create placeholders for the values. These will be filled later
    values = sql.SQL(",").join([sql.Placeholder() for _ in df.columns])
    table_id = DB_tablename
    # prepare the insert query
    insert_stmt = sql.SQL("INSERT INTO {} ({}) VALUES({});").format(
        sql.Identifier(table_id), columns, values)
    # make a connection
    #conn = psycopg2.connect(url)
    cur = conn.cursor()
    # do the insert
    psycopg2.extras.execute_batch(cur, insert_stmt, df.rows())
    conn.commit()


def cleanup_null_vals(df:pl.DataFrame, string_null_vals:list=["Source Undefined","N/A","None"]):
    """ This is to clean up all the Null/Nan values in the string and float columns, if it's float, then
        change all null values to "", blank string, otherwise, change all nan float values to
        Null (None) values for better numerical calculations

    Parameters
    ----------
    df : pl.DataFrame
        Source dataframe
    string_null_vals : list, optional
        List of string values as invalid values, hence treat as null values. The default is ["Source Undefined","N/A","None"].

    Returns
    -------
    pl.DataFrame
        Resulting DataFrame

    Examples
    -------
        >>> df = pl.DataFrame({"fruits": ["banana", "Source Undefined", "apple", None, "banana"],"A": [1, 2, 3, np.nan, 5],"D":[np.nan]*5})
        >>> cleanup_null_vals(df, string_null_vals=["Source Undefined","N/A","None"])
    """
    df2 = df.lazy()
    types = df.dtypes
    withcols = []
    string_null_vals_lower = [x.lower() for x in string_null_vals]
    for i, c in enumerate(df.columns):
        t = types[i]
        if t == pl.Utf8:
            withcols.append(pl.when(pl.col(c).str.to_lowercase().is_in(string_null_vals_lower)).then("").otherwise(pl.col(c).fill_null("")).alias(c))
        elif t in [pl.Float32, pl.Float64]:
            withcols.append(pl.col(c).fill_nan(None))
        else:
            pass
    return df2.with_columns(withcols).collect()


def remove_allempty_cols(df:pl.DataFrame):
    """ This is to remove all columns that have either only blank string ('') or only Null/Nan values, i.e. empty columns are to be removed

    Parameters
    ----------
    df : pl.DataFrame
        Source dataframe

    Returns
    -------
    pl.DataFrame
        Resulting dataframe

    Examples
    -------
        >>> df = pl.DataFrame({"fruits": ["banana", "Source Undefined", "apple", None, "banana"],"A": [1, 2, 3, np.nan, 5],"D":[np.nan]*5})
        >>> remove_allempty_cols(df)
    """
    df2 = df.lazy()
    types = df.dtypes
    selctcols = []
    for i, c in enumerate(df.columns):
        t = types[i]
        if t == pl.Utf8:
            selctcols.append((pl.col(c).is_not_null() & (pl.col(c) != "")).sum().alias(c))
        elif t in [pl.Float32, pl.Float64]:
            selctcols.append((pl.col(c).is_not_null() & pl.col(c).is_not_nan()).sum().alias(c))
        else:
            selctcols.append(pl.Series([1]).alias(c))
    d = df2.select(selctcols).collect()
    idx = np.where(np.array(d.rows()[0]) == 0)[0]
    if len(idx) == 0:
        return df
    else:
        cols2drop = np.array(df.columns)[idx].tolist()
        return df2.drop(cols2drop).collect()
