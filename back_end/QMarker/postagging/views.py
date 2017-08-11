import os
import json

os.environ['STANFORD_PARSER'] = 'D:\python test\stanford-parser-full-2017-06-09\stanford-parser-full-2017-06-09'
os.environ['STANFORD_MODELS'] = 'D:\python test\stanford-parser-full-2017-06-09\stanford-parser-full-2017-06-09'

from django.http import Http404
from django.shortcuts import render
from nltk.stem import PorterStemmer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from array import array
from nltk.corpus import wordnet
from nltk.chunk import *
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree, Tree
# nltk.download()

class postagger:


    def __init__(self):
        print("pos tagger created 1")


    def find_subject(self,t):
        for s in t.subtrees(lambda t: t.label() == 'NP'):
            for n in s.subtrees(lambda n: n.label().startswith('NN')):
                return (n[0])
            for n in s.subtrees(lambda n: n.label().startswith('PRP')):
                return (n[0])


    # Depth First Search the tree and take the last verb in VP subtree.


    def find_predicate(self,t):
        v = None

        for s in t.subtrees(lambda t: t.label() == 'VP'):
            for n in s.subtrees(lambda n: n.label().startswith('VB')):
                v = n
        return (v[0])

    # Breadth First Search the siblings of VP subtree
    # and take the first noun or adjective


    def find_object(self,t):
        for s in t.subtrees(lambda t: t.label() == 'VP'):
            for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
                if n.label() in ['NP', 'PP']:
                    for c in n.subtrees(lambda c: c.label().startswith('NN')):
                        return (c[0])
                else:
                    for c in n.subtrees(lambda c: c.label().startswith('JJ')):
                        return (c[0])


    def find_attrs(self,node):
        attrs = []
        p = node.parent()

        # Search siblings of adjective for adverbs
        if node.label().startswith('JJ'):
            for s in p:
                if s.label() == 'RB':
                    attrs.append(s[0])

        elif node.label().startswith('NN'):
            for s in p:
                if s.label() in ['DT', 'PRP$', 'POS', 'JJ', 'CD', 'ADJP', 'QP', 'NP']:
                    attrs.append(s[0])

        # Search siblings of verbs for adverb phrase
        elif node.label().startswith('VB'):
            for s in p:
                if s.label() == 'ADVP':
                    attrs.append(' '.join(s.flatten()))

        # Search uncles
        # if the node is noun or adjective search for prepositional phrase
        if node.label().startswith('JJ') or node.label().startswith('NN'):
            for s in p.parent():
                if s != p and s.label() == 'PP':
                    attrs.append(' '.join(s.flatten()))

        elif node.label().startswith('VB'):
            for s in p.parent():
                if s != p and s.label().startswith('VB'):
                    attrs.append(' '.join(s.flatten()))

        return attrs

    # get triplets if the sentence contains subordinte conjunction clauses


    def subordinate_conjunction(self,subtree, array_complete_sent):

        parser = StanfordParser()

        return_array = []
        return_array_1 = []
        return_array_2 = []
        array_of_words_in_sbar = []
        subject_of_prev = ""

        s1 = ""
        p1 = ""
        o1 = ""
        s2 = ""
        p2 = ""
        o2 = ""

        for el in subtree.leaves():
            array_of_words_in_sbar.append(el)
        for ssub in subtree:
            # if ssub.label() == 'IN' or ssub.label() == 'CC' or ssub.label() == 'TO':
                # print(ssub.leaves())
            if ssub.label() == 'S':

                s1 = self.find_subject(ssub)
                p1 = self.find_predicate(ssub)
                o1 = self.find_object(ssub)



        array_next = []

        isEqual = False
        actualCount = len(array_of_words_in_sbar)
        count = 0
        startIndex = -1
        endIndex = len(array_complete_sent)
        for i, s in enumerate(array_complete_sent):
            c = array_of_words_in_sbar[count]
            if (count == actualCount - 1):
                # print("found")
                count = 0
                endIndex = i
                break
            if (s == c and isEqual == False and count != actualCount):
                isEqual = True
                count = count + 1
                startIndex = i
            elif (s == c and isEqual and count != actualCount):
                count = count + 1
            elif (s != c):
                isEqual = False
                count = 0



        if startIndex>0:
            array_next = array_complete_sent[:startIndex]

        if startIndex==0:
            array_next = array_complete_sent[endIndex+1:]

        for el in array_next:
            if el == ',':
                array_next.remove(el)

        remade_sent = " ".join(array_next)
        s = list(parser.raw_parse(remade_sent))[0]
        s = ParentedTree.convert(s)

        s2 = self.find_subject(s)
        p2 = self.find_predicate(s)
        o2 = self.find_object(s)

        return_array_1.append(s1)
        return_array_1.append(p1)
        return_array_1.append(o1)

        return_array_2.append(s2)
        return_array_2.append(p2)
        return_array_2.append(o2)

        return_array.append(return_array_1)
        return_array.append(return_array_2)

        return return_array


    def get_subject_object_predicate(self,sentence, array_complete_sent):

        return_array = []

        subject = self.find_subject(sentence)
        predicate = self.find_predicate(sentence)
        object = self.find_object(sentence)

        # return_array.append('Sentence')
        return_array.append(subject)
        return_array.append(predicate)
        return_array.append(object)

        return return_array


    def extraxtedTriplets(self,sent):

        parser = StanfordParser()

        # Parse the example sentence
        sentence_array = nltk.sent_tokenize(sent)

        triplet_array = []
        array_for_json = []

        for sentence in sentence_array:
            t = list(parser.raw_parse(sentence))[0]
            t = ParentedTree.convert(t)
            t.pretty_print()

            array_complete_sent = []
            for t_el in t.leaves():
                array_complete_sent.append(t_el)

            cval = 0

            for subtree in t.subtrees():
                if subtree.label()=='SBAR':
                    cval = 1

            if cval == 1:
                for subtree in t.subtrees():
                    if subtree.label() == 'SBAR':
                        # print(self.subordinate_conjunction(subtree, array_complete_sent))
                        for el in self.subordinate_conjunction(subtree, array_complete_sent):
                            triplet_array.append(el)

            if cval == 0:
                # print(self.get_subject_object_predicate(t, array_complete_sent))
                triplet_array.append(self.get_subject_object_predicate(t, array_complete_sent))


        print(len(triplet_array))
        res = ""
        for ta_el in triplet_array:
            res += '{"sentence" : [{"Subject" : "%s", "Predicate" : "%s", "Object" : "%s"}], "negation" : "0"},' % (ta_el[0], ta_el[1], ta_el[2])


        json_object = '{"full_sentence": "%s",' \
                \
              '"grammar": [{"John":"Noun"}, {"likes":"anee manda"}],' \
                \
              '"triplets": [%s]}' % (sent, res[:-1])

        object_conversion = json.loads(json_object)
        return (object_conversion)


    def getTripletsCount(self,sent):

        parser = StanfordParser()

        # Parse the example sentence
        sentence_array = nltk.sent_tokenize(sent)

        triplet_array = []
        array_for_json = []

        for sentence in sentence_array:
            t = list(parser.raw_parse(sentence))[0]
            t = ParentedTree.convert(t)
            t.pretty_print()

            array_complete_sent = []
            for t_el in t.leaves():
                array_complete_sent.append(t_el)

            cval = 0

            for subtree in t.subtrees():
                if subtree.label()=='SBAR':
                    cval = 1

            if cval == 1:
                for subtree in t.subtrees():
                    if subtree.label() == 'SBAR':
                        # print(self.subordinate_conjunction(subtree, array_complete_sent))
                        for el in self.subordinate_conjunction(subtree, array_complete_sent):
                            triplet_array.append(el)

            if cval == 0:
                # print(self.get_subject_object_predicate(t, array_complete_sent))
                triplet_array.append(self.get_subject_object_predicate(t, array_complete_sent))


        return (len(triplet_array))



# p = postagger()
# # print(p.get_subject_object_predicate("john likes apple because he is hungry."))
#
# sent = 'Sara sings whenever she sees a flower. She loves nature.'
# print(p.extraxtedTriplets(sent))



















