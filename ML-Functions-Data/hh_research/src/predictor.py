

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords as nltk_stopwords
from scipy.sparse import hstack
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge


class Predictor:


    @staticmethod
    def text_replace(text) -> pd.Series:
       
        return text.apply(lambda x: [i.lower() for i in x]).replace("[^a-zA-Z]\bqout\b|\bamp\b", " ", regex=True)

    @staticmethod
    def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df_num = df[df["From"].notna() | df["From"].notna()]
        df_avg = df_num[["From", "To"]].mean(axis=1)
        df_num = df_num.drop(["Salary", "From", "To"], axis=1)
        df_num.insert(3, "Average", df_avg)
        return df_num

    @staticmethod
    def plot_results(df: pd.DataFrame):
        fp = plt.figure("Predicted salaries", figsize=(12, 8), dpi=80)
        fp.add_subplot(2, 2, 1)
        plt.title("Average Boxplot")
        sns.boxplot(data=df[["Average"]], width=0.4)

        fp.add_subplot(2, 2, 2)
        plt.title("Average Swarmplot")
        sns.swarmplot(data=df[["Average"]].dropna(), size=6)

        fp.add_subplot(2, 2, 3)
        plt.title("Average: Distribution ")
        sns.histplot(df[["Average"]].dropna(), bins=12, kde=True)
        plt.grid(False)
        plt.yticks([], [])
        plt.tight_layout()
        plt.show()

    def predict(self, df: pd.DataFrame, min_df_threshold: int = 5) -> pd.DataFrame:
        """Prepare data frame and save results

        Parameters
        ----------
        df: pd.DataFrame
            Dict of parsed vacancies.
        min_df_threshold: int
            Threshold for document freq.

        """

        
        stopwords_ru = set(nltk_stopwords.words("russian"))
        stopwords_en = set(nltk_stopwords.words("english"))
        stopwords = stopwords_ru | stopwords_en

        new_df = self.prepare_dataframe(df)
        tf_idf = TfidfVectorizer(min_df=min_df_threshold, stop_words=stopwords)

        # Training set
        txt = self.text_replace(new_df["Keys"])
        joined_text = []
        for i, x in enumerate(txt):
            print(f"{i :<4} {x}")
            joined_text.append(" ".join(x))
        x_train_text = tf_idf.fit_transform(joined_text)

        # Print top words used in keys
        idx = np.ravel(x_train_text.sum(axis=0).argsort(axis=1))[::-1][:7]
        top_words = np.array(tf_idf.get_feature_names())[idx].tolist()
        print("Top words used in keys: {}".format(top_words))

        # One-hot-encoding for data frame features
        dct_enc = DictVectorizer()
        x_train_cat = dct_enc.fit_transform(new_df[["Experience", "Name"]].to_dict("Records"))

        # Stack vectors
        x_train = hstack([x_train_text, x_train_cat])

        y_train = new_df["Average"]
        model = Ridge(alpha=1, random_state=255)
        model.fit(x_train, y_train)

        # Frame with NaNs
        x_test = df[df["From"].isna() & df["To"].isna()]

        # Test vectors
        print(x_test["Description"])
        x_desc = x_test["Description"].apply(str.lower)
        joined_desc = []
        for i, x in enumerate(x_desc):
            joined_text.append(" ".join(x))
        x_test_text = tf_idf.transform(joined_desc)
        x_test_cat = dct_enc.transform(x_test[["Experience", "Name"]].to_dict("Records"))
        x_test = hstack([x_test_text, x_test_cat])

        # Prediction model - result
        y_test = model.predict(x_test)
        print(
            f"[INFO]: Salary for vacancies with NaN:\n"
            f"Average is {y_test.mean(dtype=int)}"
            f"Maximum is {y_test.max(dtype=int)}"
            f"Maximum is {y_test.min(dtype=int)}"
        )

        df_tst = x_test.drop(["Salary", "From", "To"], axis=1)
        df_tst.insert(3, "Average", y_test.astype(int))
        return df_tst
