library(data.table)
library(fst)
library(feather)

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


##  TEST CASE  ##
df = data.table(a=c(1,2,3),b=c(4,5,6))
# add data dictionary for columns
df = add_data_dictionary(df, column="a", description="description for a")
df = add_data_dictionary(df, column="b", description="description for b")
# extract data dictoionary
generate_data_dictionary(df)
# extract data dictoionary and store it
write_fst(generate_data_dictionary(df), "test_data_dictionary.fst", compress=100)
# write to fst file
write_fst(df, "test.fst", compress=100)
# read fst file, it loses data dicitonary
df2 = read_fst("test.fst", as.data.table = T)

# wrtie to feather file that is compatible with Python Pandas data frame
write_feather(df, "test.feather")
# read feather file
df3 = read_feather("test.feather")
