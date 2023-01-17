from keybert import KeyBERT
from web_scraper_ifixit import get_the_content
import pandas as pd
import seaborn as sns
import gc

# doc = """
#          Supervised learning is the machine learning task of learning a function that
#          maps an input to an output based on example input-output pairs. It infers a
#          function from labeled training data consisting of a set of training examples.
#          In supervised learning, each example is a pair consisting of an input object
#          (typically a vector) and a desired output value (also called the supervisory signal).
#          A supervised learning algorithm analyzes the training data and produces an inferred function,
#          which can be used for mapping new examples. An optimal scenario will allow for the
#          algorithm to correctly determine the class labels for unseen instances. This requires
#          the learning algorithm to generalize from the training data to unseen situations in a
#          'reasonable' way (see inductive bias).
#       """
# kw_model = KeyBERT()
# keywords = kw_model.extract_keywords(doc)
# print(keywords)

kw_model = KeyBERT()
facts_list = []
data = get_the_content()
#print(data.head())
data["facts_doc"] = data["fact1"] + " " + data["fact1"] + " " + data["fact1"]
#print(data.head())


keywords_list = []
#print(data.head())
for index in data.index.values:
    #print(data.iloc[index]["facts_doc"])
    facts_list = data.iloc[index]["facts_doc"]
    keywords = kw_model.extract_keywords(facts_list, keyphrase_ngram_range=(1, 4), stop_words="english")
    keywords_list.append(keywords)
    # print(keywords)

data["keywords"] = keywords_list
print(data.head())

print(len(keywords_list))

kw_name_list = []
kw_relevancy_list = []
df = pd.DataFrame()

for ind in data.index:
    kw = data['keywords'][ind]
    for elem in kw:
        kw_name = elem[0]
        kw_name_list.append(kw_name)
        kw_relevancy = elem[1]
        kw_relevancy_list.append(kw_relevancy)

    df = pd.DataFrame(list(zip(kw_name_list, kw_relevancy_list)),
                      columns=["Keyword/Keyphrase", "Relevancy"]).sort_values(by="Relevancy",
                                                                              ascending=False).reset_index(
        drop=True)

    print(df)
    kw_name_list.clear()
    kw_relevancy_list.clear()


    # df = (
    #     pd.DataFrame(data["keywords"][ind], columns=["Keyword/Keyphrase", "Relevancy"])
    #     .sort_values(by="Relevancy", ascending=False)
    #     .reset_index(drop=True)
    # )

