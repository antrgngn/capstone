#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install requests beautifulsoup4 vaderSentiment pandas


# In[1]:


pip install google-api-python-client


# In[2]:


pip install newspaper3k


# In[2]:


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


# In[6]:


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
search_term = "kim jones dior"
vogue_urls = fetch_vogue_urls(search_term)

# Optional: Filter only unique URLs
vogue_urls = list(set(vogue_urls))

# Output the URLs
print(vogue_urls)

# You can now analyze the URLs or pass them into another function for sentiment analysis


# In[11]:


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
    "https://www.vogue.com/article/vogue-club/get-to-know-kristin-vartan",
    "https://www.vogue.com/article/burberry-reopens-57th-street-new-york-flagship-daniel-lee-interview",
    "https://www.vogue.com/article/kim-jones-is-stepping-down-from-dior-men",
    "https://www.vogue.com/article/who-should-be-the-next-artistic-director-of-dior-men",
    "https://www.vogue.com/article/an-interview-with-kim-jones-ahead-of-his-french-legion-of-honour"
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
vogue_sentiment_df



# In[5]:


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


# In[12]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of creative directors and fashion houses
fashion_directors = [
    ("Maria Grazia Chiuri", "Dior"),       # 2016 - Present
    ("Kris Van Assche", "Dior"),           # 2007 - 2018 (Men’s)
    ("Kim Jones", "Dior"),
    ("Hedi Slimane", "Celine"),            # 2018 - Present
    ("Phoebe Philo", "Celine"),            # 2008 - 2018
    ("Matthieu Blazy", "Bottega Veneta"),  # 2021 - Present
    ("Daniel Lee", "Bottega Veneta"),      # 2018 - 2021
    ("Daniel Lee", "Burberry"),            # 2022 - Present
    ("Riccardo Tisci", "Burberry"),        # 2018 - 2022
    ("John Galliano", "Maison Margiela"),  # 2014 - Present
    ("Olivier Rousteing", "Balmain"),      # 2011 - Present
    ("Anthony Vaccarello", "Saint Laurent"), # 2016 - Present
    ("Hedi Slimane", "Saint Laurent"),     # 2012 - 2016
    ("Demna", "Balenciaga"),               # 2015 - Present
    ("Alessandro Michele", "Gucci"),       # 2015 - 2022
    ("Sabato De Sarno", "Gucci"),          # 2023 - Present
    ("Virginie Viard", "Chanel"),          # 2019 - 2024
    ("Karl Lagerfeld", "Chanel"),          # Until 2019
    ("Pierpaolo Piccioli", "Valentino"),   # 2016 - 2023
    ("Alessandro Sartori", "Zegna"),       # 2016 - Present
    ("Jonathan Anderson", "Loewe")         # 2013 - Present
]

# Function to fetch articles from Vogue
def fetch_vogue_urls(search_term):
    search_url = f"https://www.vogue.com/search?q={search_term.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'article' in href or 'fashion-shows' in href:
            urls.append(f"https://www.vogue.com{href}" if href.startswith("/") else href)
    return list(set(urls))

# Function to fetch blog content
def fetch_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_body = soup.find('article')
    return article_body.get_text() if article_body else ""

# Function to perform sentiment analysis
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Main function to analyze sentiment from Vogue articles
def analyze_fashion_sentiment():
    sentiment_data = []
    
    for director, brand in fashion_directors:
        search_term = f"{director} {brand}"
        urls = fetch_vogue_urls(search_term)
        
        for url in urls:
            content = fetch_blog_content(url)
            if content:
                sentiment_score = analyze_sentiment(content)
                sentiment_data.append({
                    'fashion_house': brand,
                    'creative_director': director,
                    'url': url,
                    'compound_score': sentiment_score['compound'],
                    'pos_score': sentiment_score['pos'],
                    'neu_score': sentiment_score['neu'],
                    'neg_score': sentiment_score['neg']
                })
    
    return pd.DataFrame(sentiment_data)

# Run analysis
fashion_sentiment_df = analyze_fashion_sentiment()
print(fashion_sentiment_df.head())


# In[13]:


fashion_sentiment_df


# In[15]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of creative directors and fashion houses
fashion_directors = [
    ("Maria Grazia Chiuri", "Dior", 2016, 2024),
    ("Kris Van Assche", "Dior", 2007, 2018),
    ("Kim Jones", "Dior", 2018, 2024),
    ("Hedi Slimane", "Celine", 2018, 2024),
    ("Phoebe Philo", "Celine", 2008, 2018),
    ("Matthieu Blazy", "Bottega Veneta", 2021, 2024),
    ("Daniel Lee", "Bottega Veneta", 2018, 2021),
    ("Daniel Lee", "Burberry", 2022, 2024),
    ("Riccardo Tisci", "Burberry", 2018, 2022),
    ("John Galliano", "Maison Margiela", 2014, 2024),
    ("Olivier Rousteing", "Balmain", 2011, 2024),
    ("Anthony Vaccarello", "Saint Laurent", 2016, 2024),
    ("Hedi Slimane", "Saint Laurent", 2012, 2016),
    ("Demna", "Balenciaga", 2015, 2024),
    ("Alessandro Michele", "Gucci", 2015, 2022),
    ("Sabato De Sarno", "Gucci", 2023, 2024),
    ("Virginie Viard", "Chanel", 2019, 2024),
    ("Karl Lagerfeld", "Chanel", 1983, 2019),
    ("Pierpaolo Piccioli", "Valentino", 2016, 2023),
    ("Alessandro Sartori", "Zegna", 2016, 2024),
    ("Jonathan Anderson", "Loewe", 2013, 2024)
]

# Function to determine the fashion season based on year
def get_fashion_season(year):
    return [f"{year} FW", f"{year} SS"]

# Function to fetch articles from Vogue
def fetch_vogue_urls(search_term):
    search_url = f"https://www.vogue.com/search?q={search_term.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'article' in href or 'fashion-shows' in href:
            urls.append(f"https://www.vogue.com{href}" if href.startswith("/") else href)
    return list(set(urls))

# Function to fetch blog content
def fetch_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_body = soup.find('article')
    return article_body.get_text() if article_body else ""

# Function to perform sentiment analysis
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Main function to analyze sentiment from Vogue articles
def analyze_fashion_sentiment():
    sentiment_data = []
    
    for director, brand, start_year, end_year in fashion_directors:
        for year in range(start_year, end_year + 1):
            for season in get_fashion_season(year):
                search_term = f"{director} {brand} {season}"
                urls = fetch_vogue_urls(search_term)

                season_scores = []

                for url in urls:
                    content = fetch_blog_content(url)
                    if content:
                        sentiment_score = analyze_sentiment(content)
                        sentiment_data.append({
                            'fashion_house': brand,
                            'creative_director': director,
                            'season': season,
                            'url': url,
                            'compound_score': sentiment_score['compound'],
                            'pos_score': sentiment_score['pos'],
                            'neu_score': sentiment_score['neu'],
                            'neg_score': sentiment_score['neg']
                        })
                        season_scores.append(sentiment_score['compound'])

                # Compute average sentiment for the season
                if season_scores:
                    avg_sentiment = sum(season_scores) / len(season_scores)
                    sentiment_data.append({
                        'fashion_house': brand,
                        'creative_director': director,
                        'season': season,
                        'avg_compound_score': avg_sentiment
                    })

    return pd.DataFrame(sentiment_data)

# Run analysis
fashion_sentiment_df = analyze_fashion_sentiment()
print(fashion_sentiment_df.head())


# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import random
from datetime import datetime

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of fashion houses from your dataframe
fashion_houses = [
    "Burberry", "Dior", "Loewe", "Prada", "Miu Miu", "Louis Vuitton", 
    "Saint Laurent", "Gucci", "Bottega Veneta", "Valentino", 
    "Hermes", "Celine", "Maison Margiela", "Versace"
]

# Define seasons with approximate months and runway show keywords
seasons = {
    "ss": ["Spring", "Summer", "Resort", "Pre-Spring"],  # Spring/Summer keywords
    "fw": ["Fall", "Winter", "Autumn", "Pre-Fall"]  # Fall/Winter keywords
}

# Function to determine season from article text and title
def determine_season(text, title, year):
    text_lower = (text + " " + title).lower()
    
    # Look for explicit season mentions with year
    ss_pattern = any(f"{s.lower()} {year}" in text_lower for s in seasons["ss"])
    fw_pattern = any(f"{s.lower()} {year}" in text_lower for s in seasons["fw"])
    
    if ss_pattern:
        return f"{year}ss"
    elif fw_pattern:
        return f"{year}fw"
    
    # Try to determine from publication date if available
    date_match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', text_lower)
    if date_match:
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        
        if 1 <= month <= 6:
            return f"{year}ss"
        else:
            return f"{year}fw"
    
    return None

# Function to fetch articles from fashion publications
def fetch_brand_articles(brand, year, season_code):
    season_keywords = seasons[season_code]
    season_terms = " OR ".join(season_keywords)
    
    search_term = f"{brand} {season_terms} {year} collection"
    search_url = f"https://www.vogue.com/search?q={search_term.replace(' ', '+')}"
    
    try:
        print(f"Searching for: {search_term}")
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if ('article' in href or 'fashion-shows' in href) and 'vogue.com' in href:
                urls.append(href if 'http' in href else f"https://www.vogue.com{href}")
        
        # Also try some other fashion publications
        alt_urls = []
        alt_sites = [
            f"https://www.wmagazine.com/search?q={search_term.replace(' ', '+')}",
            f"https://www.harpersbazaar.com/search/?q={search_term.replace(' ', '+')}"
        ]
        
        for site in alt_sites:
            try:
                alt_response = requests.get(site)
                alt_soup = BeautifulSoup(alt_response.content, 'html.parser')
                
                for link in alt_soup.find_all('a', href=True):
                    href = link['href']
                    if brand.lower() in href.lower() and year in href:
                        if not href.startswith('http'):
                            base_url = site.split('/search')[0]
                            href = f"{base_url}{href}"
                        alt_urls.append(href)
            except Exception as e:
                print(f"Error searching alternative site: {e}")
        
        return list(set(urls + alt_urls))
    except Exception as e:
        print(f"Error fetching URLs for {search_term}: {e}")
        return []

# Function to fetch article content
def fetch_article_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try various selectors for article content
        content_selectors = [
            'article', 
            'div.article__body',
            'div.content-container',
            'div.article-content',
            'div.body-content'
        ]
        
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                return content_element.get_text(separator=' ', strip=True), soup.title.text if soup.title else ""
        
        # If specific selectors fail, try a more general approach
        paragraphs = soup.find_all('p')
        if paragraphs:
            return " ".join([p.get_text(strip=True) for p in paragraphs]), soup.title.text if soup.title else ""
        
        return "", ""
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return "", ""

# Main function to analyze sentiment by fashion house and season
def analyze_brand_season_sentiment():
    results = []
    
    # Create list of years and seasons
    years = range(2015, 2025)
    season_codes = ["ss", "fw"]
    
    for house in fashion_houses:
        for year in years:
            for season_code in season_codes:
                print(f"Processing {house} {year}{season_code}")
                
                # Fetch URLs for this brand and season
                urls = fetch_brand_articles(house, year, season_code)
                
                if not urls:
                    print(f"No articles found for {house} {year}{season_code}")
                    # Add placeholder with neutral sentiment
                    results.append({
                        'house': house,
                        'year': str(year),
                        'season': season_code,
                        'compound_score': 0,
                        'pos_score': 0,
                        'neu_score': 1,
                        'neg_score': 0,
                        'articles_analyzed': 0
                    })
                    continue
                
                # Analyze sentiment for each article
                article_sentiments = []
                analyzed_count = 0
                
                for url in urls[:5]:  # Limit to 5 articles per house/season
                    content, title = fetch_article_content(url)
                    
                    if content:
                        # Perform sentiment analysis
                        sentiment_score = analyzer.polarity_scores(content)
                        article_sentiments.append(sentiment_score)
                        analyzed_count += 1
                    
                    # Be nice to servers
                    time.sleep(random.uniform(1, 2))
                
                # Calculate average sentiment
                if article_sentiments:
                    avg_compound = sum(s['compound'] for s in article_sentiments) / len(article_sentiments)
                    avg_pos = sum(s['pos'] for s in article_sentiments) / len(article_sentiments)
                    avg_neu = sum(s['neu'] for s in article_sentiments) / len(article_sentiments)
                    avg_neg = sum(s['neg'] for s in article_sentiments) / len(article_sentiments)
                else:
                    # Default values if no articles found
                    avg_compound = 0
                    avg_pos = 0
                    avg_neu = 1
                    avg_neg = 0
                
                # Store result
                results.append({
                    'house': house,
                    'year': str(year),
                    'season': season_code,
                    'compound_score': avg_compound,
                    'pos_score': avg_pos,
                    'neu_score': avg_neu,
                    'neg_score': avg_neg,
                    'articles_analyzed': analyzed_count
                })
    
    # Convert to DataFrame
    return pd.DataFrame(results)

# Run analysis
fashion_sentiment_df = analyze_brand_season_sentiment()

# Display results
print(fashion_sentiment_df.head())

# Save to CSV
fashion_sentiment_df.to_csv('fashion_brand_sentiment_by_season.csv', index=False)


# In[4]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import time

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of fashion houses
fashion_houses = [
    "Burberry", "Dior", "Loewe", "Prada", "Miu Miu", "Louis Vuitton", 
    "Saint Laurent", "Gucci", "Bottega Veneta", "Valentino", 
    "Hermes", "Celine", "Maison Margiela", "Versace"
]

# Function to fetch articles from Vogue
def fetch_vogue_urls(search_term):
    search_url = f"https://www.vogue.com/search?q={search_term.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'article' in href or 'fashion-shows' in href:
            urls.append(f"https://www.vogue.com{href}" if href.startswith("/") else href)
    return list(set(urls))

# Function to fetch blog content
def fetch_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_body = soup.find('article')
    return article_body.get_text() if article_body else ""

# Function to extract date from article
def extract_article_date(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for date in meta tags
        meta_date = soup.find('meta', property='article:published_time')
        if meta_date and meta_date.get('content'):
            date_str = meta_date['content'].split('T')[0]
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Try to find a time element
        time_elem = soup.find('time')
        if time_elem and time_elem.get('datetime'):
            date_str = time_elem['datetime'].split('T')[0]
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # If we can't find a date, return None
        return None
    except:
        return None

# Function to determine season and year from date
def get_season_year(date_obj):
    if not date_obj:
        return None, None
    
    year = date_obj.year
    month = date_obj.month
    
    # January to June = Spring/Summer
    # July to December = Fall/Winter
    if 1 <= month <= 6:
        season = "ss"
    else:
        season = "fw"
    
    return str(year), season

# Function to perform sentiment analysis
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Main function to analyze sentiment from Vogue articles
def analyze_fashion_sentiment():
    results = []
    
    for house in fashion_houses:
        print(f"Processing {house}")
        
        # Fetch articles for this house
        urls = fetch_vogue_urls(house)
        
        # Process each article
        for url in urls:
            content = fetch_blog_content(url)
            if not content:
                continue
            
            # Extract date and determine season
            article_date = extract_article_date(url)
            year, season = get_season_year(article_date)
            
            # Skip if we couldn't determine the date
            if not year or not season:
                continue
            
            # Analyze sentiment
            sentiment_score = analyze_sentiment(content)
            
            # Add to results
            results.append({
                'house': house,
                'year': year,
                'season': season,
                'url': url,
                'compound_score': sentiment_score['compound'],
                'pos_score': sentiment_score['pos'],
                'neu_score': sentiment_score['neu'],
                'neg_score': sentiment_score['neg']
            })
            
            # Be nice to the server
            time.sleep(1)
    
    # Create DataFrame from results
    df = pd.DataFrame(results)
    
    # Group and aggregate by house, year, and season
    aggregated_df = df.groupby(['house', 'year', 'season']).agg({
        'compound_score': 'mean',
        'pos_score': 'mean',
        'neu_score': 'mean',
        'neg_score': 'mean',
        'url': 'count'  # Count of articles analyzed
    }).reset_index()
    
    # Rename the count column
    aggregated_df = aggregated_df.rename(columns={'url': 'articles_analyzed'})
    
    return aggregated_df

# Run analysis
fashion_sentiment_df = analyze_fashion_sentiment()

# Display results
print(fashion_sentiment_df.head())

# Save to CSV
fashion_sentiment_df.to_csv('fashion_brand_sentiment_by_season.csv', index=False)


# In[5]:


fashion_sentiment_df_organized = fashion_sentiment_df

fashion_sentiment_df_organized


# In[6]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import time
import re

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of fashion houses
fashion_houses = [
    "Burberry", "Dior", "Loewe", "Prada", "Miu Miu", "Louis Vuitton", 
    "Saint Laurent", "Gucci", "Bottega Veneta", "Valentino", 
    "Hermes", "Celine", "Maison Margiela", "Versace"
]

# Function to fetch articles from Vogue with pagination
def fetch_vogue_urls(search_term, max_pages=3):
    all_urls = []
    
    for page in range(1, max_pages + 1):
        search_url = f"https://www.vogue.com/search?q={search_term.replace(' ', '+')}&page={page}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for links using more flexible criteria
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Check if it's an article link and contains the brand name
                if ('article' in href or 'fashion-shows' in href) and search_term.lower() in href.lower():
                    full_url = f"https://www.vogue.com{href}" if href.startswith("/") else href
                    if full_url not in all_urls and 'vogue.com' in full_url:
                        all_urls.append(full_url)
            
            # If we didn't find any new URLs on this page, break
            if len(all_urls) == 0 and page > 1:
                break
                
            time.sleep(1)  # Be nice to the server
                
        except Exception as e:
            print(f"Error fetching page {page} for {search_term}: {e}")
            break
    
    print(f"Found {len(all_urls)} URLs for {search_term}")
    return all_urls

# Function to fetch blog content - more robust
def fetch_blog_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple potential content containers
        content_selectors = [
            'article',
            'div.article__body',
            'div.content-container',
            'div.article-content',
            'section.body',
            'div.body__inner'
        ]
        
        for selector in content_selectors:
            try:
                content_element = soup.select_one(selector)
                if content_element:
                    return content_element.get_text(separator=' ', strip=True)
            except:
                continue
        
        # If specific selectors fail, try a more general approach - get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            return " ".join([p.get_text(strip=True) for p in paragraphs])
        
        return ""
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

# More robust date extraction
def extract_article_date(url, content=""):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Look for date in meta tags
        for meta in soup.find_all('meta'):
            if meta.get('property') in ['article:published_time', 'og:published_time']:
                if meta.get('content'):
                    date_str = meta['content'].split('T')[0]
                    return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Method 2: Look for time elements
        time_elem = soup.find('time')
        if time_elem and time_elem.get('datetime'):
            date_str = time_elem['datetime'].split('T')[0]
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Method 3: Look for date patterns in URL
        date_patterns = [
            r'/(\d{4})/(\d{1,2})/(\d{1,2})/',  # /2023/12/25/
            r'-(\d{4})-(\d{1,2})-(\d{1,2})',   # -2023-12-25
            r'(\d{4})(\d{2})(\d{2})'           # 20231225
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, url)
            if match:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                if 1900 < year < 2030 and 1 <= month <= 12 and 1 <= day <= 31:
                    return datetime.datetime(year, month, day)
        
        # Method 4: Try to find date patterns in the content
        if content:
            date_pattern = r'(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b)'
            match = re.search(date_pattern, content)
            if match:
                try:
                    date_str = match.group(1)
                    return datetime.datetime.strptime(date_str, "%B %d, %Y")
                except:
                    try:
                        return datetime.datetime.strptime(date_str, "%B %d %Y")
                    except:
                        pass
        
        # If we can't find a date, extract year from URL and use January 1 as a fallback
        year_match = re.search(r'/(\d{4})/', url)
        if year_match:
            year = int(year_match.group(1))
            if 2000 <= year <= 2025:
                return datetime.datetime(year, 1, 1)  # Default to January 1st
        
        return None
    except Exception as e:
        print(f"Error extracting date from {url}: {e}")
        return None

# Function to determine season and year from date
def get_season_year(date_obj):
    if not date_obj:
        return None, None
    
    year = date_obj.year
    month = date_obj.month
    
    # January to June = Spring/Summer
    # July to December = Fall/Winter
    if 1 <= month <= 6:
        season = "ss"
    else:
        season = "fw"
    
    return str(year), season

# Function to perform sentiment analysis
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Main function with improved robustness
def analyze_fashion_sentiment():
    all_results = []
    
    for house in fashion_houses:
        print(f"Processing {house}")
        
        # Fetch articles for this house
        urls = fetch_vogue_urls(house)
        
        house_results = []
        
        # Process each article
        for url in urls:
            try:
                content = fetch_blog_content(url)
                if not content or len(content) < 100:  # Skip very short content
                    continue
                
                # Extract date and determine season
                article_date = extract_article_date(url, content)
                year, season = get_season_year(article_date)
                
                # Skip if we couldn't determine the date
                if not year or not season:
                    continue
                
                # Analyze sentiment
                sentiment_score = analyze_sentiment(content)
                
                # Add to results
                house_results.append({
                    'house': house,
                    'year': year,
                    'season': season,
                    'url': url,
                    'compound_score': sentiment_score['compound'],
                    'pos_score': sentiment_score['pos'],
                    'neu_score': sentiment_score['neu'],
                    'neg_score': sentiment_score['neg']
                })
                
                print(f"Analyzed {url} - {year}{season}")
            except Exception as e:
                print(f"Error processing {url}: {e}")
            
            # Be nice to the server
            time.sleep(0.5)
        
        print(f"Processed {len(house_results)} articles for {house}")
        all_results.extend(house_results)
    
    # Create DataFrame from results
    df = pd.DataFrame(all_results)
    
    # Group and aggregate by house, year, and season
    if not df.empty:
        aggregated_df = df.groupby(['house', 'year', 'season']).agg({
            'compound_score': 'mean',
            'pos_score': 'mean',
            'neu_score': 'mean',
            'neg_score': 'mean',
            'url': 'count'  # Count of articles analyzed
        }).reset_index()
        
        # Rename the count column
        aggregated_df = aggregated_df.rename(columns={'url': 'articles_analyzed'})
    else:
        aggregated_df = pd.DataFrame(columns=['house', 'year', 'season', 'compound_score', 'pos_score', 'neu_score', 'neg_score', 'articles_analyzed'])
    
    return aggregated_df

# Run analysis
fashion_sentiment_df = analyze_fashion_sentiment()

# Display results
print(fashion_sentiment_df.head(10))

# Save to CSV
fashion_sentiment_df.to_csv('fashion_brand_sentiment_by_season.csv', index=False)


# In[7]:


fashion_sentiment_df


# In[14]:


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
    #results.to_csv('burberry_sentiment_analysis.csv', index=False)
    
    # Basic analysis
    print("\nAverage Sentiment Scores:")
    print(f"Compound: {results['compound_score'].mean():.3f}")
    print(f"Positive: {results['pos_score'].mean():.3f}")
    print(f"Neutral: {results['neu_score'].mean():.3f}")
    print(f"Negative: {results['neg_score'].mean():.3f}")

if __name__ == "__main__":
    main()


# In[ ]:


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import time
import re

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# List of fashion houses
fashion_houses = [
    "Burberry", "Dior", "Loewe", "Prada", "Miu Miu", "Louis Vuitton", 
    "Saint Laurent", "Gucci", "Bottega Veneta", "Valentino", 
    "Hermes", "Celine", "Maison Margiela", "Versace"
]

# Function to fetch articles from Vogue with pagination
def fetch_vogue_urls(search_term, max_pages=5):
    all_urls = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try regular search with pagination
    for page in range(1, max_pages + 1):
        search_url = f"https://www.vogue.com/search?q={search_term.replace(' ', '+')}&page={page}"
        
        try:
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for links using flexible criteria
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Check if it's an article link
                if ('article' in href or 'fashion-shows' in href):
                    full_url = f"https://www.vogue.com{href}" if href.startswith("/") else href
                    if full_url not in all_urls and 'vogue.com' in full_url:
                        all_urls.append(full_url)
            
            # If we didn't find any new URLs on this page, break
            if len(all_urls) == 0 and page > 1:
                break
                
            time.sleep(1)  # Be nice to the server
                
        except Exception as e:
            print(f"Error fetching page {page} for {search_term}: {e}")
            break
    
    # Explicitly target archive pages for each year
    for year in range(2018, 2025):
        # Try the main archive for that year
        archive_url = f"https://www.vogue.com/archive/{year}?q={search_term.replace(' ', '+')}"
        
        try:
            response = requests.get(archive_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                if ('article' in href or 'fashion-shows' in href):
                    full_url = f"https://www.vogue.com{href}" if href.startswith("/") else href
                    if full_url not in all_urls and 'vogue.com' in full_url:
                        all_urls.append(full_url)
            
            time.sleep(1)  # Be nice to the server
        except Exception as e:
            print(f"Error fetching archive for {year}: {e}")
        
        # Try runway specific searches for each season
        for season in ["spring", "fall"]:
            runway_url = f"https://www.vogue.com/fashion-shows/{season}-{year}-ready-to-wear/{search_term.lower().replace(' ', '-')}"
            
            try:
                response = requests.get(runway_url, headers=headers)
                if response.status_code == 200:  # Only process if page exists
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if ('fashion-shows' in href or 'article' in href):
                            full_url = f"https://www.vogue.com{href}" if href.startswith("/") else href
                            if full_url not in all_urls and 'vogue.com' in full_url:
                                all_urls.append(full_url)
                
                time.sleep(1)  # Be nice to the server
            except Exception as e:
                print(f"Error fetching runway archive for {season} {year}: {e}")
    
    # Also try to find articles from fashion week coverage
    for year in range(2018, 2025):
        for season in ["spring", "fall"]:
            for city in ["new-york", "london", "milan", "paris"]:
                fashion_week_url = f"https://www.vogue.com/fashion-shows/{city}/{season}-{year}-ready-to-wear"
                
                try:
                    response = requests.get(fashion_week_url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for the specific brand within fashion week coverage
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if search_term.lower().replace(' ', '-') in href.lower() and 'fashion-shows' in href:
                            full_url = f"https://www.vogue.com{href}" if href.startswith("/") else href
                            if full_url not in all_urls and 'vogue.com' in full_url:
                                all_urls.append(full_url)
                    
                    time.sleep(1)  # Be nice to the server
                except Exception as e:
                    print(f"Error fetching fashion week coverage for {city} {season} {year}: {e}")
    
    # Try specific collection review format
    for year in range(2018, 2025):
        for season in ["spring", "fall"]:
            collection_url = f"https://www.vogue.com/fashion-shows/review/{season}-{year}-ready-to-wear-{search_term.lower().replace(' ', '-')}"
            
            try:
                response = requests.get(collection_url, headers=headers)
                if response.status_code == 200:
                    all_urls.append(collection_url)
                time.sleep(1)
            except Exception as e:
                print(f"Error checking collection review: {e}")
    
    print(f"Found {len(all_urls)} URLs for {search_term}")
    return list(set(all_urls))  # Remove any duplicates

# Function to fetch blog content - more robust
def fetch_blog_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple potential content containers
        content_selectors = [
            'article',
            'div.article__body',
            'div.content-container',
            'div.article-content',
            'section.body',
            'div.body__inner'
        ]
        
        for selector in content_selectors:
            try:
                content_element = soup.select_one(selector)
                if content_element:
                    return content_element.get_text(separator=' ', strip=True)
            except:
                continue
        
        # If specific selectors fail, try a more general approach - get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            return " ".join([p.get_text(strip=True) for p in paragraphs])
        
        return ""
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

# More robust date extraction
def extract_article_date(url, content=""):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Look for date in meta tags
        for meta in soup.find_all('meta'):
            if meta.get('property') in ['article:published_time', 'og:published_time']:
                if meta.get('content'):
                    date_str = meta['content'].split('T')[0]
                    return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Method 2: Look for time elements
        time_elem = soup.find('time')
        if time_elem and time_elem.get('datetime'):
            date_str = time_elem['datetime'].split('T')[0]
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Method 3: Look for date patterns in URL
        date_patterns = [
            r'/(\d{4})/(\d{1,2})/(\d{1,2})/',  # /2023/12/25/
            r'-(\d{4})-(\d{1,2})-(\d{1,2})',   # -2023-12-25
            r'(\d{4})(\d{2})(\d{2})'           # 20231225
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, url)
            if match:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                if 1900 < year < 2030 and 1 <= month <= 12 and 1 <= day <= 31:
                    return datetime.datetime(year, month, day)
        
        # Method 4: Try to find date patterns in the content
        if content:
            date_pattern = r'(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b)'
            match = re.search(date_pattern, content)
            if match:
                try:
                    date_str = match.group(1)
                    return datetime.datetime.strptime(date_str, "%B %d, %Y")
                except:
                    try:
                        return datetime.datetime.strptime(date_str, "%B %d %Y")
                    except:
                        pass
        
        # If we can't find a date, extract year from URL and use January 1 as a fallback
        year_match = re.search(r'/(\d{4})/', url)
        if year_match:
            year = int(year_match.group(1))
            if 2000 <= year <= 2025:
                return datetime.datetime(year, 1, 1)  # Default to January 1st
        
        return None
    except Exception as e:
        print(f"Error extracting date from {url}: {e}")
        return None

# Function to determine season and year from date
def get_season_year(date_obj):
    if not date_obj:
        return None, None
    
    year = date_obj.year
    month = date_obj.month
    
    # January to June = Spring/Summer
    # July to December = Fall/Winter
    if 1 <= month <= 6:
        season = "ss"
    else:
        season = "fw"
    
    return str(year), season

# Function to perform sentiment analysis
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Main function with improved robustness
def analyze_fashion_sentiment():
    all_results = []
    
    for house in fashion_houses:
        print(f"Processing {house}")
        
        # Fetch articles for this house
        urls = fetch_vogue_urls(house)
        
        house_results = []
        
        # Process each article
        for url in urls:
            try:
                content = fetch_blog_content(url)
                if not content or len(content) < 100:  # Skip very short content
                    continue
                
                # Extract date and determine season
                article_date = extract_article_date(url, content)
                year, season = get_season_year(article_date)
                
                # Skip if we couldn't determine the date
                if not year or not season:
                    continue
                
                # Analyze sentiment
                sentiment_score = analyze_sentiment(content)
                
                # Add to results
                house_results.append({
                    'house': house,
                    'year': year,
                    'season': season,
                    'url': url,
                    'compound_score': sentiment_score['compound'],
                    'pos_score': sentiment_score['pos'],
                    'neu_score': sentiment_score['neu'],
                    'neg_score': sentiment_score['neg']
                })
                
                print(f"Analyzed {url} - {year}{season}")
            except Exception as e:
                print(f"Error processing {url}: {e}")
            
            # Be nice to the server
            time.sleep(0.5)
        
        print(f"Processed {len(house_results)} articles for {house}")
        all_results.extend(house_results)
    
    # Create DataFrame from results
    df = pd.DataFrame(all_results)
    
    # Group and aggregate by house, year, and season
    if not df.empty:
        aggregated_df = df.groupby(['house', 'year', 'season']).agg({
            'compound_score': 'mean',
            'pos_score': 'mean',
            'neu_score': 'mean',
            'neg_score': 'mean',
            'url': 'count'  # Count of articles analyzed
        }).reset_index()
        
        # Rename the count column
        aggregated_df = aggregated_df.rename(columns={'url': 'articles_analyzed'})
    else:
        aggregated_df = pd.DataFrame(columns=['house', 'year', 'season', 'compound_score', 'pos_score', 'neu_score', 'neg_score', 'articles_analyzed'])
    
    return aggregated_df

# Run analysis
fashion_sentiment_df = analyze_fashion_sentiment()

# Display results
print(fashion_sentiment_df.head(10))

# Save to CSV
fashion_sentiment_df.to_csv('fashion_brand_sentiment_by_season.csv', index=False)


# In[ ]:




