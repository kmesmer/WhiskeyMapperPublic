# Term Frequency/Inverse Document Frequency Analysis

1) Save archive.csv

2) Run a1_archive_clean.py, yields archive_clean.csv

3) Run a2_extract_reviews.py, yields reviews_raw.csv

4) Run a3_cut_reviews.py, yields reviews_cut.csv

5) Run a4_clean_reviews.py, yields reviews_clean.csv

6) Run a5_tfidf.py, yields recommendations.csv and similarities.csv

7) Run a6_combine_recs_simps.py, yields TF_sims_1.csv

8) Run a7_scale_sims.py, yields TF_sims_2.csv

# Item-Based Collaborative Filtering

1) Run b1_archive_clean.py, yields archive_clean.csv (reads raw archive from tfidf directory)

2) Run b2_adj_cos_sim.py, yields CF_sims1.csv

3) Run b3_scale_sims.py, yields CF_sims2.csv

4) Run b4_combine_sims.py, yeilds combined_sims.csv

5) Run b5_clean_sims.py, yields final_recs.csv

# Creating Flavor Profiles

1) 