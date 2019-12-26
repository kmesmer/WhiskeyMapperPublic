There are five directories in this project:

1) tfidf_whiskey: this directory extracts reviews using Reddit's API. Next, the reviews are cut and cleaned. Finally, we run a Term Frequency-Inverse Document Frequency analysis as a first step in building a recommendation engine. This was not a novel approach and u/shasty does an excellent job of explaining the code in his post at https://www.reddit.com/r/Scotch/comments/amrq5z/whisky_recommender_based_on_reddit_whisky_review/. Ultimately, the tf-idf analysis will be discarded because we can create a more accurate engine by selecting our own set of features (see below). In each of the directories, python files are alphabetized for easy execution and there is typically a .csv file output after each step so progress is obvious.

2) flavor_whiskey: In this directory, we create a custom dictionary of 323 descriptive words and count the frequency at which each word is used across reviews for each whiskey. These counts are averaged and these 323 features are used to calculate cosine similarity between whiskeys. We also pull the top 20 most frequenty used descriptive words for each whiskey, which will later be shown on the website. Next, we map each of the 323 words to one of 13 high-level flavor categories based on the work of David Wishart. I altered his categories a bit to make the system more appropriate for bourbon and rye in addition to scotch. These 13 feature profiles will also be displayed on the website, and we will use them to calculate cosine similarity across whiskeys again as the second model in our recommendation engine.

3) cf_whiskey: Here, we utilize user ratings (not reviews) to calculate cosine similarity between whiskeys in a process called item-based collaborative filtering. This is the third model used in our recommendation engine.

4) pca_whiskey: Here, we run a principal component analysis on our 323 descriptive terms to reduce the dimensionality to only 3 components. This allows us to graph each whiskey on a 3D scatter chart on the website.

5) stats_whiskey: Finally, we pull the basic stats for each whiskey. We do some cleaning and mapping since the original spreadsheet can be inconsistent and doesn't include some of the information we want to show.

Note: All data is ultimately written to whiskey.db using SQLite3 commands. This database is hosted on the website server.