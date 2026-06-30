from CSV_Handler import CSV_cleanner_and_manger, CSV_merger

if __name__ == "__main__":
    filter_df_1 = CSV_cleanner_and_manger("data/daily_sales_data_0.csv")
    filter_df_2 = CSV_cleanner_and_manger("data/daily_sales_data_1.csv")
    filter_df_3 = CSV_cleanner_and_manger("data/daily_sales_data_2.csv")

    merge_df = CSV_merger(filter_df_1, filter_df_2, filter_df_3)
    print(merge_df)
    print(merge_df.shape[0])