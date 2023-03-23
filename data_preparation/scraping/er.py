#!/usr/bin/env python
# coding: utf-8

# In[68]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# similarity_join.py
import re
import numpy as np
import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains,concat_ws, split, explode, lower, array_remove, to_json, array, array_intersect, array_union, size, expr, array_distinct
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

class SimilarityJoin:
    def __init__(self, data_file1, data_file2):
        spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
        self.df1 = spark.read.option("header",True).csv(data_file1)
        self.df2 = spark.read.option("header",True).csv(data_file2)

    def preprocess_df(self, new_df, cols): 
        """ 
            Input: $df represents a DataFrame
                   $cols represents the list of columns (in $df) that will be concatenated and be tokenized

            Output: Return a new DataFrame that adds the "joinKey" column to the input $df

            Comments: The "joinKey" column is a list of tokens, which is generated as follows:
                     (1) concatenate the $cols in $df; 
                     (2) apply the tokenizer to the concatenated string
            Here is how the tokenizer should work:
                     (1) Use "re.split(r'\W+', string)" to split a string into a set of tokens
                     (2) Convert each token to its lower-case
        """
        
        # new_df = df.select("*")
        # replace NaN with empty string for columns
        new_df.na.fill("",[cols[0]])
        # join values, apply regex, filter empty strings, and convert to lower
        # new_df['joinKey'] = new_df[cols].apply(lambda row: ' '.join(row.values.astype(str)).strip(), axis=1)
        # new_df['joinKey'] = new_df['joinKey'].apply(lambda row: re.split(r'\W+', row))
        # new_df['joinKey'] = new_df['joinKey'].apply(lambda row: list(filter(None, row)))
        # new_df['joinKey'] = new_df['joinKey'].apply(lambda row: list(map(str.lower, row)))
        new_df = new_df.withColumn("OG-Company", new_df[cols[0]])
        new_df = new_df.withColumn('joinKey', concat_ws(' ', *cols))
        new_df = new_df.withColumn('joinKey', split('joinKey', '\W+')) \
               .withColumn('joinKey', array_remove(col('joinKey'), '')) \
               .withColumn('joinKey', expr("transform(joinKey, x -> lower(x))"))
        
        return new_df
        

    def filtering(self, df1, df2):
        """ 
            Input: $df1 and $df2 are two input DataFrames, where each of them 
                   has a 'joinKey' column added by the preprocess_df function

            Output: Return a new DataFrame $cand_df with four columns: 'id1', 'joinKey1', 'id2', 'joinKey2',
                    where 'id1' and 'joinKey1' are from $df1, and 'id2' and 'joinKey2'are from $df2.
                    Intuitively, $cand_df is the joined result between $df1 and $df2 on the condition that 
                    their joinKeys share at least one token. 

            Comments: Since the goal of the "filtering" function is to avoid n^2 pair comparisons, 
                      you are NOT allowed to compute a cartesian join between $df1 and $df2 in the function. 
                      Please come up with a more efficient algorithm (see hints in Lecture 2). 
        """
        # df1["joinKey1"] = df1["joinKey"]
        # df2["joinKey2"] = df2["joinKey"]
        # new_df1 = df1.explode('joinKey')
        # new_df2 = df2.explode('joinKey')
        # cand_df = pd.merge(new_df1[['id', 'joinKey1', 'joinKey']], new_df2[['id', 'joinKey2', 'joinKey']], on=['joinKey'], suffixes=('1', '2'))
        # # drop duplicates, and drop exploded merge column
        # cand_df = cand_df.drop_duplicates(subset=['id1', 'id2'], ignore_index= True)
        # cand_df.drop('joinKey', axis=1, inplace=True)
        # return cand_df
        
       # explode for both keys
        df1 = df1.withColumn("joinKey1", df1["joinKey"])
        df2 = df2.withColumn("joinKey2", df2["joinKey"])
        new_df1 = df1.select('id', 'joinKey1', explode('joinKey').alias('joinKey'), 'OG-Company')
        new_df2 = df2.select('id', 'joinKey2', explode('joinKey').alias('joinKey'), 'OG-Company')

        # merge on joinKey column
        new_df1 = new_df1.withColumnRenamed("id","id1")
        new_df2 = new_df2.withColumnRenamed("id","id2")
        new_df1 = new_df1.withColumnRenamed("OG-Company","OG-Company-Warn")
        new_df2 = new_df2.withColumnRenamed("OG-Company","OG-Company-Nasdaq")
        cand_df = (new_df1.select('id1', 'joinKey1', 'joinKey','OG-Company-Warn')
           .join(new_df2.select('id2', 'joinKey2', 'joinKey', 'OG-Company-Nasdaq'), on='joinKey')
           .select('id1', 'id2', 'joinKey1', 'joinKey2','OG-Company-Warn','OG-Company-Nasdaq'))
        
        # drop duplicates and joinKey column
        cand_df = cand_df.dropDuplicates(['id1', 'id2']) \
                         .drop('joinKey')

        return cand_df

        

    def verification(self, cand_df, threshold):
        """ 
            Input: $cand_df is the output DataFrame from the 'filtering' function. 
                   $threshold is a float value between (0, 1] 

            Output: Return a new DataFrame $result_df that represents the ER result. 
                    It has five columns: id1, joinKey1, id2, joinKey2, jaccard 

            Comments: There are two differences between $cand_df and $result_df
                      (1) $result_df adds a new column, called jaccard, which stores the jaccard similarity 
                          between $joinKey1 and $joinKey2
                      (2) $result_df removes the rows whose jaccard similarity is smaller than $threshold 
        """
        # # create a columns for converting the joinKey lists to sets
        # # create columns applying intersection and union on the sets
        # cand_df["intersection"] = cand_df.apply(lambda row: len(list(row["joinKey1_set"].intersection(row["joinKey2_set"]))), axis =1)
        # cand_df["union"] = cand_df.apply(lambda row: len(list(row["joinKey1_set"].union(row["joinKey2_set"]))), axis =1)
        # # ceate column to compute jaccard apply threshold and reset index
        # cand_df["jaccard"] = cand_df.apply(lambda row: row["intersection"]/row["union"], axis=1)
        # cand_df = cand_df[cand_df['jaccard'] >= threshold]
        # cand_df.reset_index(drop=True, inplace=True)
        # # drop intermediate columns
        # result_df = cand_df.copy()
        # result_df.drop(columns=["joinKey1_set", "joinKey2_set", "intersection", "union"], inplace=True)       
        # return result_df     
        
        # convert joinKey1 and joinKey2 arrays to sets
        cand_df = cand_df.withColumn('joinKey1_set', array_distinct(col('joinKey1')))
        cand_df = cand_df.withColumn('joinKey2_set', array_distinct(col('joinKey2')))

        # compute intersection and union of sets
        joinKey1_set = cand_df.select('joinKey1_set')
        cand_df = cand_df.withColumn('intersection', size(array_intersect(col('joinKey1_set'), col('joinKey2_set'))))
        cand_df = cand_df.withColumn('union', size(array_union(col('joinKey1_set'), col('joinKey2_set'))))

        # compute jaccard similarity and filter by threshold
        cand_df = cand_df.withColumn('jaccard', col('intersection')/col('union'))
        cand_df = cand_df.filter(col('jaccard') > threshold)

        # drop intermediate columns and reset index
        result_df = cand_df.drop('joinKey1_set', 'joinKey2_set', 'intersection', 'union').dropna()
#         result_df = result_df.withColumnRenamed('id1', 'id').drop('id2').dropna()
        return result_df
        

    def evaluate(self, result, ground_truth):
        """ 
            Input: $result is a list of matching pairs identified by the ER algorithm
                   $ground_truth is a list of matching pairs labeld by humans

            Output: Compute precision, recall, and fmeasure of $result based on $ground_truth, and
                    return the evaluation result as a triple: (precision, recall, fmeasure)

        """
        T = 0
        for item in ground_truth:
            if item in result:
                T += 1
                
        recall = T/len(ground_truth)
        precision = T/len(result)
        fmeasure = (2*precision*recall)/(precision + recall)
        
        return precision, recall, fmeasure
        

    def jaccard_join(self, cols1, cols2, threshold):
        new_df1 = self.preprocess_df(self.df1, cols1)
#         new_df1.toPandas().to_csv('ppreprocess1.csv', index=False)
#         df1 = pd.read_csv('preprocess1.csv')
#         df2 = pd.read_csv('ppreprocess1.csv')
#         print(df1.equals(df2))
    
        new_df2 = self.preprocess_df(self.df2, cols2)
        print("Before filtering: %d pairs in total" % (self.df1.count() * self.df2.count()))

        cand_df = self.filtering(new_df1, new_df2)
        print ("After Filtering: %d pairs left" %(cand_df.count()))

        result_df = self.verification(cand_df, threshold)
        print ("After Verification: %d similar pairs" %(result_df.count()))

        return result_df

def array_to_string(my_list):
    return '[' + ','.join([str(elem) for elem in my_list]) + ']'

if __name__ == "__main__":
    er = SimilarityJoin("warn.csv", "nasdaq.csv")
    amazon_cols = ["Company"]
    google_cols = ["Name"]
#     er = SimilarityJoin("Amazon_sample.csv", "Google_sample.csv")
#     amazon_cols = ["title", "manufacturer"]
#     google_cols = ["name", "manufacturer"]
    result_df = er.jaccard_join(amazon_cols, google_cols, 0.5)

    result = result_df.select('id1', 'id2').collect()
#     ground_truth = pd.read_csv("Amazon_Google_perfectMapping_sample.csv").values.tolist()
#     print ("(precision, recall, fmeasure) = ", er.evaluate(result, ground_truth))
    
    array_to_string_udf = udf(array_to_string, StringType())

    result_df = result_df.withColumn('joinKey1', array_to_string_udf(result_df["joinKey1"]))
    result_df = result_df.withColumn('joinKey2', array_to_string_udf(result_df["joinKey2"]))
    result_df.show()
    print("***********************************************************",(result_df.count(), len(result_df.columns)))

    result_df.write.option("header",True).csv("warn_jaccard.csv")
#     ground_truth = pd.read_csv("Amazon_Google_perfectMapping_sample.csv").values.tolist()
#     print ("(precision, recall, fmeasure) = ", er.evaluate(result, ground_truth))



# In[ ]:




