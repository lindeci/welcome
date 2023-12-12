import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.chunk import ne_chunk

# 1. 下载NLTK的数据和资源
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('vader_lexicon')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# 2. 分词
print("2. 分词")
text = "This is an example sentence."
tokens = word_tokenize(text)
print(tokens)

# 3. 停用词 （停用词是在文本处理中被过滤掉的常见词语，如“a”、“an”、“the”、“in”、“on”等）
print("3. 停用词")
stop_words = set(stopwords.words('english'))
# print(stop_words)
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
print(filtered_tokens)

# 4. 词干提取 (将单词转化为它们的词干或基本形式。词干提取可以通过去除单词的后缀来实现，例如将“running”和“runs”都转化为“run”，将“jumping”和“jumped”都转化为“jump”。)
print("4. 词干提取")
ps = PorterStemmer()
stemmed_words = [ps.stem(token) for token in tokens]
print(stemmed_words)

# 5. 词形还原 (将单词还原为它们的词根或基本形式。与词干提取不同，词形还原考虑了单词的上下文和语法规则，将单词还原为其在词典中的原始形式。)
print("5. 词形还原")
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(token) for token in tokens]
print(lemmatized_words)

# 6. 词性标注 (为文本中的每个单词确定其词性或语法角色。在词性标注中，每个单词被标记为特定的词性，如名词、动词、形容词、副词等。)
print("6. 词性标注")
tagged_words = pos_tag(tokens)
print(tagged_words)

# 7. 命名实体识别
print("7. 命名实体识别")
entities = ne_chunk(tagged_words)
print(entities)

# 8. 情感分析
print("8. 情感分析")
sentences = ["I love NLTK!", "NLTK is awesome!"]
sia = SentimentIntensityAnalyzer()
for sentence in sentences:
    sentiment = sia.polarity_scores(sentence)
    print(sentence, sentiment)

# 9. 词频统计
print("9. 词频统计")
from nltk import FreqDist
freq_dist = FreqDist(tokens)
print(freq_dist.most_common(5))

# 10. 文本相似度
print("10. 文本相似度")
from nltk.metrics.distance import edit_distance
distance = edit_distance("rain", "shine")
print(distance)

# 11. 词袋模型 (将文本视为一个袋子（bag），其中每个单词都是袋子中的一个项目，忽略了单词在文本中的顺序和语法结构，仅仅关注每个单词的出现频率。)
print("11. 词袋模型")
from sklearn.feature_extraction.text import CountVectorizer
corpus = ["This is the first document.", "This document is the second document."]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
print(X.toarray())

# 12. 文本分类
# print("12. 文本分类")
# from nltk.classify import NaiveBayesClassifier
# train_data = [("I love this car", "positive"), ("This view is amazing", "positive"),
#               ("I feel great", "positive"), ("I am so sad", "negative")]
# features = [(text_features, label) for (text_features, label) in train_data]
# classifier = NaiveBayesClassifier.train(features)
# print(classifier.classify("I feel sad"))

# 13. 文本语义相似度
print("13. 文本语义相似度")
from nltk.corpus import wordnet
syn1 = wordnet.synsets("hello")[0]
syn2 = wordnet.synsets("hi")[0]
similarity = syn1.path_similarity(syn2)
print(similarity)

# 14. 停用词表
print("14. 停用词表")
print(stopwords.words('english'))

# 15. 词性缩写
# print("15. 词性缩写")
# print(nltk.help.upenn_tagset())

# 16. 高级文本查找
print("16. 高级文本查找")
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize("This is an example sentence.")
print(tokens)

# 17. 文本清洗
print("17. 文本清洗")
from nltk.tokenize import sent_tokenize
sentences = sent_tokenize("This is the first sentence. This is another sentence.")
print(sentences)

# 18. 句子分割
print("18. 句子分割")
sentences = nltk.sent_tokenize("This is the first sentence. This is another sentence.")
print(sentences)

# 19. 句子情感分析
print("19. 句子情感分析")
sia = SentimentIntensityAnalyzer()
sentences = ["I love NLTK!", "NLTK is awesome!"]
for sentence in sentences:
    sentiment = sia.polarity_scores(sentence)
    print(sentence, sentiment)

# 20. 分类特征提取器
print("20. 分类特征提取器")
from nltk import pos_tag, word_tokenize
from nltk.corpus import names
def gender_features(word):
    return {'last_letter': word[-1]}
gender_features('John')


# 21. 获取词的定义
print("21. 获取词的定义")
synsets = wordnet.synsets('car')
definitions = [syn.definition() for syn in synsets]
print("Definitions of 'car':", definitions)