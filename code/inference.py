from gensim.models import FastText

periods = ["vedic", "upanisadic", "epics", "sutras"]

for period in periods:
   model = FastText.load(f"../models/legacy/v1-sandhi-6-12/{period}/fasttext_{period}.model")
   print(period)
   print(model.wv.most_similar("asura", topn=12))