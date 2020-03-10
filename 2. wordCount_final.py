# --------------------------------------------------------------------------------- #
# Word Count
# --------------------------------------------------------------------------------- #


# For WordCount
from konlpy.tag import Twitter
from collections import Counter
from heapq import nlargest

# For WordCloud
from PIL import Image
import random
import numpy as np
from IPython.display import set_matplotlib_formats
import matplotlib


from wordcloud import WordCloud
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords


# --------------------------------------------------------------------------------- #

# Select CSV file
fileName = input("Select File :")

# --------------------------------------------------------------------------------- #

# Read CSV file
file = open("./" + fileName + ".csv", "r", encoding='UTF8')
lists = file.readlines()
file.close()

# --------------------------------------------------------------------------------- #

# Parsing
twitter = Twitter()
morphs = []
for sentence in lists:
    morphs.append(twitter.pos(sentence))

print(morphs)

# --------------------------------------------------------------------------------- #

# 명사 추출
noun_adj_adv_list = []
for sentence in morphs:
    for word, tag in sentence:
        if tag in ['Noun'] and ("것" not in word) and ("저" not in word) and ("등" not in word) and ("전" not in word) and ("요" not in word) and ("분" not in word) and ("시" not in word) and ("카" not in word) and ("너" not in word) and ("및" not in word) and ("이" not in word) and ("거" not in word) and ("좀" not in word) and ("제" not in word) and ("후" not in word) and ("비" not in word) and ("내" not in word)and ("나" not in word)and ("수"not in word) and("게"not in word)and("말"not in word)and("개월"not in word)and("아기"not in word)and("맘"not in word)and("아가"not in word)and("질문"not in word)and("도"not in word)and("뭐"not in word):
            noun_adj_adv_list.append(word)

print(noun_adj_adv_list)

# --------------------------------------------------------------------------------- #

# 워드 카운트
count = Counter(noun_adj_adv_list)
words = dict(count.most_common())
words

# --------------------------------------------------------------------------------- #

# Top 100
N = 100
res = nlargest(N, words, key=words.get)

result_word = {}

for i in range(len(res)):
    result_word[res[i]] = words[res[i]]

print(result_word)


# --------------------------------------------------------------------------------- #
# Word Cloud
# --------------------------------------------------------------------------------- #

%matplotlib inline

matplotlib.rc('font', family='Malgun Gothic')

set_matplotlib_formats('retina')

matplotlib.rc('axes', unicode_minus=False)

# --------------------------------------------------------------------------------- #

r4_mask = np.array(Image.open("./background.jpeg"))

# --------------------------------------------------------------------------------- #

wordcloud = WordCloud(background_color="black", font_path='/Users/genius/Library/Fonts/HangeulNuriR.ttf',
                      colormap="prism", width=800, height=800, mask=r4_mask)


wordcloud = wordcloud.generate_from_frequencies(result_word)
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
