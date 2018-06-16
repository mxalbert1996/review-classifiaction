# review-classifiaction
Emotion classification on book reviews

# Usage
Run `python TestServer.py` and a web server will be started at port 8000.

# Requirements
* [Python 3](https://www.python.org/)
* Test server needs [pattern](https://github.com/clips/pattern/tree/development) and [Keras](https://keras.io/)
* Training also needs [gensim](https://radimrehurek.com/gensim/index.html)

# Data
Amazon book review data credits to <http://jmcauley.ucsd.edu/data/amazon/>.

# Models used
[Word2vec](https://en.wikipedia.org/wiki/Word2vec) and [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory).