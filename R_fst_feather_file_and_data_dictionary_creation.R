library(data.table)
library(fst)
library(feather)


#####################  UTILITIES  #####################
generate_data_dictionary = function(df) {
    # create data dictionry for the data.table
    data_dictionary = data.table::data.table(column=NA, description=NA)[0]
    for (col in colnames(df)) {
        col_desc_ = ifelse(is.null(attributes(df[, get(col)])[["label"]]), "",attributes(df[, get(col)])[["label"]])
        data_dictionary = rbind(data_dictionary, data.table::data.table(column=col, description=col_desc_))
    }
    return(data_dictionary)
}

add_data_dictionary = function(df, column, description){
    attr(df[[column]], 'label') <- description
    return(df)
}

load_fst_file = function(fst_df_file, fst_df_data_dictionary_file=NULL){
    df = fst::read_fst(fst_df_file, as.data.table = T)
    if (!is.null(fst_df_data_dictionary_file)) {
        df_dictionary = fst::read_fst(fst_df_data_dictionary_file, as.data.table = T)
        for (i in seq_len(nrow(df_dictionary))){
            column = df_dictionary[i, column]
            attr(df[[column]], 'label') <- df_dictionary[i, description]
        }
    }
    return(df)
}

load_feather_file = function(feather_df_file, feather_df_data_dictionary_file=NULL){
    df = data.table::as.data.table(feather::read_feather(feather_df_file))
    if (!is.null(feather_df_data_dictionary_file)) {
        df_dictionary = data.table::as.data.table(feather::read_feather(feather_df_data_dictionary_file))
        for (i in seq_len(nrow(df_dictionary))){
            column = df_dictionary[i, column]
            attr(df[[column]], 'label') <- df_dictionary[i, description]
        }
    }
    return(df)
}




#####################  TEST CASE  #####################
df = data.table(a=c(1,2,3),b=c(4,5,6))
# add data dictionary for columns
df = add_data_dictionary(df, column="a", description="description for a")
df = add_data_dictionary(df, column="b", description="description for b")
# extract data dictoionary and show it
generate_data_dictionary(df)
# extract data dictoionary and store it
write_fst(generate_data_dictionary(df), "test_data_dictionary.fst", compress=100)
write_feather(generate_data_dictionary(df), "test_data_dictionary.feather")
# write to fst file
write_fst(df, "test.fst", compress=100)
# read fst file, it loses data dicitonary
df2 = read_fst("test.fst", as.data.table = T)
# wrtie to feather file that is compatible with Python Pandas data frame
write_feather(df, "test.feather")
# read feather file, it loses data dictionary
df3 = read_feather("test.feather")
# Load in the fst/feather data.table and its fst data dictionary file
df4 = load_fst_file(fst_df_file="test.fst", fst_df_data_dictionary_file="test_data_dictionary.fst")
df5 = load_feather_file(feather_df_file="test.feather", feather_df_data_dictionary_file="test_data_dictionary.feather")
