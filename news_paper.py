from newspaper import Article

url = "https://imvahonshya.co.rw/israel-mbonyi-yaciye-agahigo-ko-gukurikirwa-cyane-kuri-youtube/"
article = Article(url)
print("the article authors are: {}".format(article.text))
print("the publish dates are: {}".format(article.publish_date))