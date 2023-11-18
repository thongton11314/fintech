from datetime import datetime, timedelta
import pandas as pd
from source.back_end.company.company_base_api import CompanyAPI

# Child class for sentiment analysis
class CompanySentiment(CompanyAPI):

    def __init__(self, symbol):
        super().__init__(symbol)
        self.news = pd.DataFrame()
        self.mean_sentiment_score = 0
        self.mean_sentiment_class = ""

    @staticmethod
    def _mean_score_helper(mean_score):
        if mean_score <= -0.35:
            return "Bearish"
        elif -0.35 < mean_score <= -0.15:
            return "Somewhat Bearish"
        elif -0.15 < mean_score < 0.15:
            return "Neutral"
        elif 0.15 <= mean_score < 0.35:
            return "Somewhat Bullish"
        elif mean_score >= 0.35:
            return "Bullish"
        else:
            return "Undefined"

    def get_sentiment(self, max_feed=10):

        data = self._fetch_sentiment_data()
        if not data:
            return

        news = []
        try:
            for i in data["feed"][:max_feed]:
                temp = {}
                temp["title"] = i["title"]
                temp["url"] = i["url"]
                temp["authors"] = i["authors"]

                topics = []
                for j in i["topics"]:
                    topics.append(j["topic"])
                temp["topics"] = topics

                sentiment_score = ""
                sentiment_label = ""
                for j in i["ticker_sentiment"]:
                    if j["ticker"] == self.symbol:
                        sentiment_score = j["ticker_sentiment_score"]
                        sentiment_label = j["ticker_sentiment_label"]
                        break
                temp["sentiment_score"] = sentiment_score
                temp["sentiment_label"] = sentiment_label

                news.append(temp)

        except Exception as e:
            print(e)
            return None

        self.news = pd.DataFrame(news)
        self.news["sentiment_score"] = pd.to_numeric(self.news["sentiment_score"])
        self.mean_sentiment_score = self.news["sentiment_score"].mean()
        self.mean_sentiment_class = self._mean_score_helper(self.mean_sentiment_score)

        return {
            "news": self.news,
            "mean_sentiment_score": self.mean_sentiment_score,
            "mean_sentiment_class": self.mean_sentiment_class
        }

    def _fetch_sentiment_data(self):
        current_datetime = datetime.now()
        one_year_ago = current_datetime - timedelta(days=365)
        formatted_time_from = one_year_ago.strftime("%Y%m%dT%H%M")
        print("time_from=", formatted_time_from)
        
        params_extra = {
            "function": "NEWS_SENTIMENT",
            "tickers": self.symbol,
            "sort": "RELEVANCE"
        }
        data = self._get_data_from_api("NEWS_SENTIMENT", params_extra)
        if not data:
            print(f"No data found for {self.symbol}")
            return None
        return data