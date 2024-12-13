#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install requests beautifulsoup4 vaderSentiment pandas


# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch articles from a blog or magazine
def fetch_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Adjust this according to the specific HTML structure of the site
    articles = soup.find_all('article')
    return articles

# Function to perform sentiment analysis
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Function to format sentiment results into a DataFrame
def analyze_vogue_sentiment():
    vogue_url = 'https://www.vogue.com/article/daniel-lee-debut-burberry-collection'
    articles = fetch_blog_content(vogue_url)
    
    # List to store article data
    sentiment_data = []
    
    for article in articles:
        headline = article.find('h2').get_text() if article.find('h2') else 'No Headline'
        content = article.get_text()
        
        # Perform sentiment analysis
        sentiment_score = analyze_sentiment(content)
        
        # Append data as a dictionary (row of the DataFrame)
        sentiment_data.append({
            'headline': headline,
            'content': content,
            'compound_score': sentiment_score['compound'],
            'pos_score': sentiment_score['pos'],
            'neu_score': sentiment_score['neu'],
            'neg_score': sentiment_score['neg']
        })
    
    # Create a pandas DataFrame from the list of dictionaries
    sentiment_df = pd.DataFrame(sentiment_data)
    
    return sentiment_df

# Running the function and saving the results into a DataFrame
vogue_sentiment_df = analyze_vogue_sentiment()

# Print the first few rows of the DataFrame
vogue_sentiment_df.head()


# In[8]:


import requests
from bs4 import BeautifulSoup

# Function to get all relevant URLs from Vogue
def fetch_vogue_urls(search_term):
    # Vogue search URL with your query (adjust 'burberry+daniel+lee' as needed)
    search_url = f"https://www.vogue.com/search?q={search_term}"
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store URLs
    urls = []

    # Vogue often uses <a> tags with an href attribute for their articles
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Ensure URLs are articles (i.e., contain 'fashion-shows', 'article', etc.)
        if 'article' in href or 'fashion-shows' in href:
            urls.append(href)

    return urls

# Fetch URLs related to Burberry and Daniel Lee
search_term = "kriss van asche dior"
vogue_urls = fetch_vogue_urls(search_term)

# Optional: Filter only unique URLs
vogue_urls = list(set(vogue_urls))

# Output the URLs
print(vogue_urls)

# You can now analyze the URLs or pass them into another function for sentiment analysis


# In[7]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of URLs you got from the search or scraping
vogue_urls = [
    "https://www.vogue.com/article/dior-beauty-ss25",
    "https://www.vogue.com/article/lee-kiefer-paris-games-interview",
    "https://www.vogue.com/article/brigitte-macron-first-dior-show",
    "https://www.vogue.com/'/article/vogue-club/get-to-know-kristin-vartan",
    "https://www.vogue.com/article/burberry-reopens-57th-street-new-york-flagship-daniel-lee-interview"
    #"https:///article/dior-spa-eden-roc"
    
    
    # Add more URLs here...
]

#bof_urls = [
    #"https://www.businessoffashion.com/opinions/luxury/does-burberry-have-the-wrong-strategy/",
    #"https://www.businessoffashion.com/news/luxury/burberry-plunges-as-company-slashes-profit-forecast/",
    #"https://www.businessoffashion.com/articles/luxury/burberry-reveals-new-logo-first-campaign-by-daniel-lee-ahead-of-debut-show/",
    #"https://www.businessoffashion.com/opinions/luxury/burberry-desperately-needs-the-return-of-britpop/"
#]

# Function to fetch article content from a given URL
def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Adjust this based on the structure of the articles on Vogue
    # Usually, articles are within <p> tags
    paragraphs = soup.find_all('p')
    content = ' '.join([para.get_text() for para in paragraphs])
    
    return content

# Function to perform sentiment analysis on the content
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Function to analyze sentiment for each article from the URLs
def analyze_vogue_articles(urls):
    sentiment_data = []
    
    for url in urls:
        content = fetch_article_content(url)
        sentiment_score = analyze_sentiment(content)
        
        # Append the results to the sentiment_data list
        sentiment_data.append({
            'url': url,
            'content': content,
            'compound_score': sentiment_score['compound'],
            'pos_score': sentiment_score['pos'],
            'neu_score': sentiment_score['neu'],
            'neg_score': sentiment_score['neg']
        })
    
    # Create a pandas DataFrame from the sentiment data
    sentiment_df = pd.DataFrame(sentiment_data)
    
    return sentiment_df

# Run the analysis on the list of URLs
vogue_sentiment_df = analyze_vogue_articles(vogue_urls)

#bof_sentiment_df = analyze_vogue_articles(bof_urls)

# Print the DataFrame with sentiment scores
# vogue_sentiment_df.head()
vogue_sentiment_df.head()



# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import os
from googleapiclient.discovery import build
from newspaper import Article
import time

class BrandSentimentAnalyzer:
    def __init__(self, google_api_key, news_api_key):
        self.analyzer = SentimentIntensityAnalyzer()
        self.google_api_key = google_api_key
        self.news_api_key = news_api_key
        self.google_service = build('customsearch', 'v1', developerKey=google_api_key)

    def fetch_google_results(self, query, start_date=None, end_date=None, max_results=50):
        """
        Fetch results from Google Custom Search API
        """
        results = []
        start_index = 1

        while len(results) < max_results:
            try:
                # Build date range string if dates are provided
                date_range = ''
                if start_date and end_date:
                    date_range = f' after:{start_date} before:{end_date}'
                
                search_query = query + date_range
                
                response = self.google_service.cse().list(
                    q=search_query,
                    cx='YOUR_SEARCH_ENGINE_ID',  # You'll need to create this
                    start=start_index
                ).execute()

                if 'items' not in response:
                    break

                for item in response['items']:
                    results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'date': item.get('pagemap', {}).get('metatags', [{}])[0].get('article:published_time', '')
                    })

                if len(response['items']) < 10:  # Less than maximum results per page
                    break

                start_index += 10
                time.sleep(1)  # Respect rate limits

            except Exception as e:
                print(f"Error in Google search: {e}")
                break

        return pd.DataFrame(results)

    def fetch_news_api_results(self, query, start_date=None, end_date=None):
        """
        Fetch results from News API
        """
        url = 'https://newsapi.org/v2/everything'
        
        params = {
            'q': query,
            'apiKey': self.news_api_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 100
        }
        
        if start_date:
            params['from'] = start_date
        if end_date:
            params['to'] = end_date

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            articles = response.json()['articles']
            
            results = [{
                'title': article['title'],
                'link': article['url'],
                'snippet': article['description'],
                'date': article['publishedAt'],
                'source': article['source']['name']
            } for article in articles]
            
            return pd.DataFrame(results)

        except Exception as e:
            print(f"Error fetching news: {e}")
            return pd.DataFrame()

    def fetch_article_content(self, url):
        """
        Fetch and parse article content using newspaper3k
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            print(f"Error fetching article content from {url}: {e}")
            return ""

    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text using VADER
        """
        return self.analyzer.polarity_scores(text)

    def analyze_brand_sentiment(self, brand_name, creative_director=None, start_date=None, end_date=None):
        """
        Comprehensive brand sentiment analysis
        """
        # Construct search query
        query = f"{brand_name}"
        if creative_director:
            query += f" {creative_director}"

        # Get results from both APIs
        google_results = self.fetch_google_results(query, start_date, end_date)
        news_results = self.fetch_news_api_results(query, start_date, end_date)

        # Combine results
        all_results = pd.concat([google_results, news_results]).drop_duplicates(subset=['link'])

        # Analyze sentiment for each article
        sentiment_data = []
        for _, row in all_results.iterrows():
            content = self.fetch_article_content(row['link'])
            sentiment = self.analyze_sentiment(content)
            
            sentiment_data.append({
                'date': row['date'],
                'title': row['title'],
                'url': row['link'],
                'snippet': row['snippet'],
                'content': content,
                'compound_score': sentiment['compound'],
                'pos_score': sentiment['pos'],
                'neu_score': sentiment['neu'],
                'neg_score': sentiment['neg']
            })

        return pd.DataFrame(sentiment_data)

# Example usage
def main():
    analyzer = BrandSentimentAnalyzer(
        google_api_key='YOUR_GOOGLE_API_KEY',
        news_api_key='YOUR_NEWS_API_KEY'
    )
    
    # Analyze sentiment for Burberry under Daniel Lee
    results = analyzer.analyze_brand_sentiment(
        brand_name='Burberry',
        creative_director='Daniel Lee',
        start_date='2023-01-01',
        end_date='2024-01-01'
    )
    
    # Save results to CSV
    results.to_csv('burberry_sentiment_analysis.csv', index=False)
    
    # Basic analysis
    print("\nAverage Sentiment Scores:")
    print(f"Compound: {results['compound_score'].mean():.3f}")
    print(f"Positive: {results['pos_score'].mean():.3f}")
    print(f"Neutral: {results['neu_score'].mean():.3f}")
    print(f"Negative: {results['neg_score'].mean():.3f}")

if __name__ == "__main__":
    main()


# In[ ]:




