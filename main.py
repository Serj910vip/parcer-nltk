#pip install wordcloud
#pip install pymorphy2
import pymorphy2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud
from matplotlib import pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')


text ='''
      У лукоморья дуб зелёный;
      Златая цепь на дубе том.
      И днём и ночью кот учёный
      Всё ходит по цепи кругом.
      Идёт направо — песнь заводит,
      Налево — сказку говорит.
      Там чудеса: там леший бродит,
      Русалка на ветвях сидит.
      Там на неведомых дорожках
      Следы невиданных зверей.
      Избушка там на курьих ножках
      Стоит без окон, без дверей.
      Там лес и дол видений полны.
      Там о заре прихлынут волны
      На брег песчаный и пустой,
      И тридцать витязей прекрасных
      Чредой из вод выходят ясных,
      И с ними дядька их морской.
      Там королевич мимоходом
      Пленяет грозного царя.
      Там в облаках перед народом
      Через леса, через моря
      Колдун несёт богатыря.
      В темнице там царевна тужит,
      А бурый волк ей верно служит.
      Там ступа с Бабою Ягой
      Идёт, бредёт сама собой,
      Там царь Кащей над златом чахнет;
      Там русский дух… там Русью пахнет!
      И там я был, и мёд я пил;
      У моря видел дуб зелёный;
      Под ним сидел, и кот учёный
      Свои мне сказки говорил.
'''


#Разбираем тект на предложения
sentences = sent_tokenize(text, language='russian')

print(20 * "-")
print(sentences)
print(20 * "-")
print("Всего предложений: ", len(sentences))


#Удаляем стоп-слова
stop_words = set(stopwords.words('russian'))

print(10 * "-", " Стоп-слова ", 10 * "-")
print(stop_words)
print(20 * "-")

words = word_tokenize(text)

print( 20 * "-")
print(words)
print(20 * "-")
print("Всего слов в вашем тексте: ", len(words))
print(20 * "-")

wc = WordCloud().generate(' '.join([i for i in words]))
plt.imshow(wc)

words = [word.lower() for word in words if word.isalpha()]
words = [word for word in words if word not in stop_words]

print(10 * "-", " Слова в нижнем регистре без стоп-слов ", 10 * "-")
print(words)
print(20 * "-")
print("Всего слов в вашем тексте: ", len(words))
print(20 * "-")

wc = WordCloud().generate(' '.join([i for i in words]))
plt.imshow(wc)


#Лемматизация
morph = pymorphy2.MorphAnalyzer()
words = [morph.parse(word)[0].normal_form for word in words]

print(10 * "-", " Слова в начальной форме ", 10 * "-")
print(words)
print(20 * "-")
print("Всего слов в вашем тексте: ", len(words))
print(20 * "-")

wc = WordCloud().generate(' '.join([i for i in words]))
plt.imshow(wc)



#Вычисляем частотность каждого предложения

freq_dist = FreqDist(words)
sentence_scores = {}

for i, sentence in enumerate(sentences):
    sentence_words = word_tokenize(sentence.lower())
    sentence_score = sum([freq_dist[word] for word in sentence_words if word in freq_dist])

    sentence_scores[i] = sentence_score

sentence_scores



#Сортировка предложений по частотности
sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)

sorted_scores


# Формируем суммаризацию
selected_sentences = sorted_scores[:1]
selected_sentences = sorted(selected_sentences)

# Формируем суммаризацию
summary = ' '.join([sentences[i] for i, _ in selected_sentences])
print(summary)



#Оборачиваем код в функцию
def summariztion(text, sent_number=3):
  sentences = sent_tokenize(text, language='russian')
  stop_words = set(stopwords.words('russian'))
  words = word_tokenize(text)
  words = [word.lower() for word in words if word.isalpha()]
  words = [word for word in words if word not in stop_words]
  morph = pymorphy2.MorphAnalyzer()
  words = [morph.parse(word)[0].normal_form for word in words]
  freq_dist = FreqDist(words)
  sentence_scores = {}

  for i, sentence in enumerate(sentences):
      sentence_words = word_tokenize(sentence.lower())
      sentence_score = sum([freq_dist[word] for word in sentence_words if word in freq_dist])

      sentence_scores[i] = sentence_score

  sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
  selected_sentences = sorted_scores[:sent_number]
  selected_sentences = sorted(selected_sentences)
  summary = ' '.join([sentences[i] for i, _ in selected_sentences])
  return summary


#парсер 
#Суммируем полученные новости

#pip3 install bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd


df = pd.read_csv("data.csv")

links = list(df.links)

url_main = 'https://new-science.ru/'
response = requests.get(url)
bs = BeautifulSoup(response.text,"lxml")

news_text = " "
for url in links:
  response = requests.get(url_main + url)
  bs = BeautifulSoup(response.text,"lxml")
  temp = bs.find('div', 'entry-content entry clearfix').find_all('p')
  news_text += " ".join([p.text for p in temp])

  summariztion(news_text, 10)
