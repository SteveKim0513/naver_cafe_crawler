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
import pandas as pd


from wordcloud import WordCloud
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords


# Select CSV File
fileName = input("Select File ")

# Read CSV file
data = pd.read_csv("./" + fileName + ".csv")
data.head(10)

# 분석 대상 키워드 : 2번 결과보고 입력!
keywords = ['때', '추천', '신생아', '피부', '단계', '모유', '초기', '텀', '젖병', '방법', '낮잠', '태열', '접종', '유산균', '완', '유량']

# 각 키워드 포함 제목 담을 리스트
key_source = []

# 각 키워드가 포함된 제목 추출
for i in range(len(keywords)):
    globals()['key_words_{}'.format(i)] = []
    globals()['key_morphs_{}'.format(i)] = []

    tmp = data['title']

    key_source.append(tmp[tmp.str.contains(keywords[i])])

print(key_source)


# 키워드 파싱&형태소 분석
twitter = Twitter()
morphs = [[]]*len(keywords)
for j in range(len(keywords)):
    for sentence in key_source[j]:
        morphs[j].append(twitter.pos(sentence))

# 명사 추출
noun_list = [[]]*len(keywords)

for k in range(len(keywords)):
    for sentence in morphs[k]:
        for word, tag in sentence:
            if tag in ['Noun'] and ("것" not in word) and ("저" not in word) and ("등" not in word) and ("전" not in word) and ("요" not in word) and ("분" not in word) and ("시" not in word) and ("카" not in word) and ("너" not in word) and ("및" not in word) and ("이" not in word) and ("거" not in word) and ("좀" not in word) and ("제" not in word) and ("후" not in word) and ("비" not in word) and ("내" not in word)and ("나" not in word)and ("수"not in word) and("게"not in word)and("말"not in word)and("개월"not in word)and("아기"not in word)and("맘"not in word)and("아가"not in word)and("질문"not in word)and("도"not in word)and("뭐"not in word):
                noun_list[k].append(word)

# 워드 카운트 & 워드 클라우드
%matplotlib inline
matplotlib.rc('font', family='Malgun Gothic')
set_matplotlib_formats('retina')
matplotlib.rc('axes', unicode_minus=False)
r4_mask = np.array(Image.open("./background.jpeg"))

for l in range(len(keywords)):

    print("KEYWORDS = ", keywords[l])

    count = Counter(noun_list[l])
    words = dict(count.most_common())
    words

    # Top 100 추출
    N = 100
    res = nlargest(N, words, key=words.get)

    result_word = {}

    m = 0
    for m in range(len(res)):
        result_word[res[m]] = words[res[m]]

    wordcloud = WordCloud(background_color="black", font_path='/Users/jhouse/Library/Fonts/HangeulNuriR.ttf',
                      colormap="prism", width=800, height=800, mask=r4_mask)


    wordcloud = wordcloud.generate_from_frequencies(result_word)
    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    






