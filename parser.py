import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

def get_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select('span.titleline > a')  # новая структура сайта
    print(f"Найдено заголовков: {len(titles)}")
    return [title.get_text() for title in titles]

def clean_and_count_words(titles):
    all_words = []
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend(words)
    counter = Counter(all_words)
    df = pd.DataFrame(counter.items(), columns=['word', 'count'])
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)
    return df[df['word'].str.len() > 3]

def plot_top_words(df, top_n=10):
    top_words = df.head(top_n)
    plt.figure(figsize=(10, 6))
    plt.bar(top_words['word'], top_words['count'])
    plt.title(f'Top {top_n} most frequent words in titles')
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = 'https://news.ycombinator.com'
    titles = get_titles(url)
    word_stats = clean_and_count_words(titles)
    print(word_stats.head(10))
    plot_top_words(word_stats)
