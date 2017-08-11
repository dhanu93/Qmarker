from nltk.tag import StanfordNERTagger
from nltk.corpus import wordnet
import json

class nerTagging:

    def __init__(self):
        print("ner tagger created 3")

    def getSymanticSimilarityValue(self,word1, word2):
        s= None
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
        return s


    def settingNER(self, data):

        st = StanfordNERTagger('D:/python test/first/ner/english.all.3class.distsim.crf.ser.gz','D:\python test/first/ner/stanford-ner.jar')

        ner_words = ["PERSON", "TIME", "LOCATION", "ITEM", "SPORTS", "VEGETABLE", "FRUIT", "ANIMAL"]

        ner_array = []

        for triplet in data["triplets"]:
            sent = []

            sentence = "%s %s %s" % (
                triplet["sentence"][0]["Subject"],
                triplet["sentence"][0]["Predicate"],
                triplet["sentence"][0]["Object"]
            )

            all_tags = st.tag(sentence.split())

            count = 0
            for tag in all_tags:
                count += 1

                if (tag[0] != 'None') and (tag[1] == "O"):
                    val = -1
                    the_word = ""

                    if count != 2:
                        for words in ner_words:
                            try:
                                ner_word = self.getSymanticSimilarityValue(tag[0], words)
                            except:
                                ner_word = None

                            print(ner_word)

                            if ner_word is not None:
                                if val < ner_word:
                                    val = ner_word
                                    the_word = words

                        if val != -1:
                            sent.append(tag[0])
                            sent.append(the_word)
                        else:
                            sent.append(tag[0])
                            sent.append("O")
                    else:
                        sent.append(tag[0])
                        sent.append("PREDICATE")
                else:
                    sent.append(tag[0])
                    sent.append(tag[1])
            ner_array.append(sent)

        for i, el in enumerate(ner_array):
            sub = "-2" if (el[1] is 'O') else el[1]
            pred = "-2" if (el[3] is 'O') else el[3]
            obj = "-2" if (el[5] is 'O') else el[5]

            dd = '[{"Subject" : "%s", "Predicate" : "%s", "Object" : "%s"}]' % (sub, pred, obj)
            a = json.loads(dd)
            data['triplets'][i]["ner"] = a

        return data




# Menna call karana function ekaaaaa.......
# print(settingNER(json.loads(obj)))
