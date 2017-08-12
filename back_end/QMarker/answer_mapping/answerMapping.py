from nltk.corpus import wordnet
import json


class answerMapping:

	# this
    def __init__(self):
        print("answer mapping created 2")

    # this method is used for check whether two words are synonyms or not
    # take two words as parameters and return boolean value
    def isTwoWordsAreSynonyms(self,word1, word2):
        isSynonym = False
        for synset in wordnet.synsets(word1):
            for lemma in synset.lemma_names():
                if lemma == word2 and lemma != word1:
                    isSynonym=True
        return isSynonym


    # this method is used for check whether two words are antonyms or not
    # take two words as parameters and return boolean value
    def isTwoWordsAreAntonyms(self,word1, word2):

        isAntonym = False
        antonyms = []
        for synset in wordnet.synsets(word1):
            for lemma in synset.lemmas():
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name())

        for word in antonyms:
            if(word==word2):
                isAntonym=True

        return isAntonym

    # this method is used to get semantic similarity of given two words
    # take two words and pos of the words as parameters and return double value
    # pos means whether they are nouns,verbs,adjectives etc.
    # used wu and palmer algorithm to calculate semantic similarity between two words
    def getSymanticSimilarityValue(self,word1, word2,pos):
        max = 0

        synsets1 = wordnet.synsets(word1, pos=pos)
        synsets2 = wordnet.synsets(word2, pos=pos)

        for s1 in synsets1:
            for s2 in synsets2:
                wup_val = s1.wup_similarity(s2)
                if (max < wup_val):
                    max = wup_val

        return max

    # this method is use to select best matching sentences between student answer and model answer
    # takes two parameters
    # first parameter is an array which contains all compared student answer and model answer sentences ids and
    #  value for their semantic similarity
    # the algorithm compares those values and sentences and selects the best matching pairs
    def selectBestMatchingSentencePares(self, marksArray, finalMarksArr):

        selected_model_answer = 0
        selected_std_answer = -1
        highest_mark = 0
        finalMarkObjTxt = ""

        for y, mas in enumerate(marksArray):

            # print(mas)
            if selected_model_answer != mas[0]:

                # finalMarksArr[selected_model_answer][0]=selected_model_answer
                # finalMarksArr[selected_model_answer][1]=selected_std_answer
                # finalMarksArr[selected_model_answer][2]=highest_mark
                finalMarkObjTxt += '{"ModeAanswer" : "%s", "StudentAnswer" : "%s", "mark" : "%s"},' % (selected_model_answer, selected_std_answer, highest_mark)

                # for finalMr in finalMarksArr:
                #     if(mas[1]==finalMr[1] and mas[2]>finalMr[2]):
                #         print(mas + finalMr)
                #         # current_hs_mark=finalMr[2]
                #         next_hs_mark = 0
                #         next_hs_mark_std_ans = -1
                #         for marks in marksArray:
                #             if(marks[0]==finalMr[0] and marks[1]!=finalMr[1]):
                #                 if(next_hs_mark<marks[2]):
                #                     next_hs_mark=marks[2]
                #                     next_hs_mark_std_ans=marks[1]
                #
                #         finalMr[1] = next_hs_mark_std_ans
                #         finalMr[2] = next_hs_mark

                selected_model_answer = mas[0]
                selected_std_answer = -1
                highest_mark = 0

            if mas[2] > highest_mark:
                selected_std_answer = mas[1]
                highest_mark = mas[2]

            if y == (len(marksArray)-1):
                # finalMarksArr[selected_model_answer][0] = selected_model_answer
                # finalMarksArr[selected_model_answer][1] = selected_std_answer
                # finalMarksArr[selected_model_answer][2] = highest_mark
                finalMarkObjTxt += '{"ModeAanswer" : "%s", "StudentAnswer" : "%s", "mark" : "%s"}' % (selected_model_answer, selected_std_answer, highest_mark)

        finalMarkObj = '{"markedSentences": [%s]}' % (finalMarkObjTxt)
        print('This object contains matching sentence pairs and relevent semantic score')
        print(finalMarkObj)
        return json.loads(finalMarkObj)
    #
    #
    #
    #
    # js1 is model answer and js2 is student answer
    def compareAnswersAndReturnMatchingPairs(self,js1, js2):


        print(js1['triplets'])
        print(js2['triplets'])

        # create 2d array to save marks which has given to each compared sentences
        countModelAnswerSentences=len(js1['triplets'])
        countStudentAnswerSentences=len(js2['triplets'])
        marksArray = [[-1 for x in range(3)] for y in range(countModelAnswerSentences*countStudentAnswerSentences)]
        indexFor2DArray = 0

        for modelAnswer_sentence_id, modelAnswerSentence in enumerate(js1['triplets']):

            Selected_sentence_modelAnswer_subject = modelAnswerSentence['sentence'][0]['Subject']
            Selected_sentence_modelAnswer_predicate = modelAnswerSentence['sentence'][0]['Predicate']
            Selected_sentence_modelAnswer_object = modelAnswerSentence['sentence'][0]['Object']

            model_answer_sentense_negation = modelAnswerSentence['negation']

            model_answer_sentense_ner_subject = modelAnswerSentence['ner'][0]['Subject']
            model_answer_sentense_ner_object = modelAnswerSentence['ner'][0]['Object']


            for studentAnswer_sentence_id, studentAnswerSentence in enumerate(js2['triplets']):

                mark = 0

                Selected_sentence_studentAnswer_subject = studentAnswerSentence['sentence'][0]['Subject']
                Selected_sentence_studentAnswer_predicate = studentAnswerSentence['sentence'][0]['Predicate']
                Selected_sentence_studentAnswer_object = studentAnswerSentence['sentence'][0]['Object']

                student_answer_sentense_negation = studentAnswerSentence['negation']

                student_answer_sentense_ner_subject = studentAnswerSentence['ner'][0]['Subject']
                student_answer_sentense_ner_object = studentAnswerSentence['ner'][0]['Object']

                # check ner of the subject
                if(model_answer_sentense_ner_subject != "-2" and model_answer_sentense_ner_subject == student_answer_sentense_ner_subject):
                    # consider subject
                    if(Selected_sentence_modelAnswer_subject.lower() == Selected_sentence_studentAnswer_subject.lower()):
                         mark = mark+(1)*3

                    elif(self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_subject.lower(),Selected_sentence_studentAnswer_subject.lower())):
                         mark = mark+(self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_subject.lower(),Selected_sentence_studentAnswer_subject.lower(),"n"))*2.5

                    else:
                         mark = mark+self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_subject.lower(),Selected_sentence_studentAnswer_subject.lower(),"n")





                # consider predicate
                # predicate might be or might not be a negation
                #in here checking whether sentences are negations or not
                if(model_answer_sentense_negation=="1" and student_answer_sentense_negation=="1"):

                    # consider predicate
                    if (Selected_sentence_modelAnswer_predicate.lower() == Selected_sentence_studentAnswer_predicate.lower()):
                        mark = mark + (1)*3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower(),"v"))*2.5

                    else:
                        mark=mark+self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower(),"v")


                elif(model_answer_sentense_negation=="1" and student_answer_sentense_negation=="0"):

                    if(self.isTwoWordsAreAntonyms(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (1)*3

                elif(model_answer_sentense_negation == "0" and student_answer_sentense_negation == "1"):

                    if (self. ntonyms(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (1)*3


                elif(model_answer_sentense_negation == "0" and student_answer_sentense_negation == "0"):

                    # consider predicate
                    if (Selected_sentence_modelAnswer_predicate.lower() == Selected_sentence_studentAnswer_predicate.lower()):
                        mark = mark + (1)*3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower(),"v"))*2.5

                    else:
                        mark=mark+self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_predicate.lower(),Selected_sentence_studentAnswer_predicate.lower(),"v")


                # check ner of the object
                if (model_answer_sentense_ner_object != "-2" and model_answer_sentense_ner_object == student_answer_sentense_ner_object):
                    # consider object
                    if (Selected_sentence_modelAnswer_object.lower() == Selected_sentence_studentAnswer_object.lower()):
                         mark = mark + (1)*3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_object.lower(), Selected_sentence_studentAnswer_object.lower())):
                         mark = mark + (self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_object.lower(), Selected_sentence_studentAnswer_object.lower(),"n"))*2.5

                    else:
                         mark=mark+self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_object.lower(),Selected_sentence_studentAnswer_object.lower(),"n")



                # marksObj["marks"].append({"ModelAnswerSentense": modelAnswer_sentence_id, "StudentAnswerSentense": studentAnswer_sentence_id,"Mark": (mark/9)*100})

                # add marks to the marksArray
                marksArray[indexFor2DArray][0] = modelAnswer_sentence_id
                marksArray[indexFor2DArray][1] = studentAnswer_sentence_id
                marksArray[indexFor2DArray][2] = (mark/9)*100
                indexFor2DArray = indexFor2DArray + 1



        finalMarksArr = [[-1 for x in range(3)] for y in range(countModelAnswerSentences)]

        finalMarksArr = self.selectBestMatchingSentencePares(marksArray, finalMarksArr)
        return finalMarksArr



    # obj1 = '{"full_sentence": "Kazun is a lazy turtle",' \
    #         \
    #       '"grammar": [{"student":"Noun"}, {"likes":"anee manda"}],' \
    #         \
    #       '"triplets": ['\
    #        '{"sentence": [{"Subject" : "John","Predicate" : "play","Object" : "basketball"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1","Object" : "thing"}],' \
    #        '"negation" : "0"},' \
    #        '{"sentence": [{"Subject" : "David","Predicate" : "play", "Object" : "cricket"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1", "Object" : "thing"}],' \
    #        '"negation" : "0"},' \
    #        '{"sentence": [{"Subject" : "King","Predicate" : "live", "Object" : "america"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1", "Object" : "country"}],' \
    #        '"negation" : "0"} ' \
    #       ']}'
    #
    #
    # obj2 = '{"full_sentence": "Kazun is a lazy turtle",' \
    #         \
    #       '"grammar": [{"John":"Noun"}, {"likes":"anee manda"}],' \
    #         \
    #       '"triplets": [' \
    #        '{"sentence": [{"Subject" : "John", "Predicate" : "enjoy ","Object" : "basketball"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1","Object" : "thing"}],' \
    #        '"negation" : "0"},' \
    #        '{"sentence": [{"Subject" : "David","Predicate" : "play", "Object" : "netball"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1","Object" : "thing"}],' \
    #        '"negation" : "1"},' \
    #        '{"sentence": [{"Subject" : "monarch","Predicate" : "rule", "Object" : "england"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1","Object" : "thing"}],' \
    #        '"negation" : "0"} ' \
    #       ']}'
    #
    #


    # obj1 = '{"full_sentence": "Kazun is a lazy turtle",' \
    #         \
    #       '"grammar": [{"John":"Noun"}, {"likes":"anee manda"}],' \
    #         \
    #       '"triplets": ['\
    #        '{"sentence": [{"Subject" : "I","Predicate" : "eat","Object" : "restaurant"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1","Object" : "thing"}],' \
    #        '"negation" : "0"}' \
    #       ']}'
    # #
    # #
    # obj2 = '{"full_sentence": "Kazun is a lazy turtle",' \
    #         \
    #       '"grammar": [{"John":"Noun"}, {"likes":"anee manda"}],' \
    #         \
    #       '"triplets": [' \
    #        '{"sentence": [{"Subject" : "I", "Predicate" : "feed","Object" : "hotel"}],' \
    #        '"ner": [{"Subject" : "person","Predicate" : "-1","Object" : "thing"}],' \
    #        '"negation" : "0"}' \
    #       ']}'


    # js1 = json.loads(obj1)
    # js2 = json.loads(obj2)
    # jsl1 = json.dumps(obj1)
    # jsl2 = json.dumps(obj2)
    #
    # print(compareAnswersAndReturnMatchingPairs(js1,js2))
    #
    # print(js1)
    # print(jsl1)

    # this is for prototype!!!!!!!!!!!!!!!!!
    # remove this
    # remove this
    # remove this
    # remove this
    # remove this
    # remove this
    # remove this
    # remove this
    # remove this
    # remove this
    def compareAnswersAndReturnMatchingPairsPrototype(self, js1, js2):

        print(js1['triplets'])
        print(js2['triplets'])

        # create 2d array to save marks which has given to each compared sentences
        countModelAnswerSentences = len(js1['triplets'])
        countStudentAnswerSentences = len(js2['triplets'])
        marksArray = [[-1 for x in range(3)] for y in
                      range(countModelAnswerSentences * countStudentAnswerSentences)]
        indexFor2DArray = 0

        for modelAnswer_sentence_id, modelAnswerSentence in enumerate(js1['triplets']):

            Selected_sentence_modelAnswer_subject = modelAnswerSentence['sentence'][0]['Subject']
            Selected_sentence_modelAnswer_predicate = modelAnswerSentence['sentence'][0]['Predicate']
            Selected_sentence_modelAnswer_object = modelAnswerSentence['sentence'][0]['Object']

            model_answer_sentense_negation = modelAnswerSentence['negation']

            model_answer_sentense_ner_subject = modelAnswerSentence['ner'][0]['Subject']
            model_answer_sentense_ner_object = modelAnswerSentence['ner'][0]['Object']

            for studentAnswer_sentence_id, studentAnswerSentence in enumerate(js2['triplets']):

                mark = 0

                Selected_sentence_studentAnswer_subject = studentAnswerSentence['sentence'][0]['Subject']
                Selected_sentence_studentAnswer_predicate = studentAnswerSentence['sentence'][0]['Predicate']
                Selected_sentence_studentAnswer_object = studentAnswerSentence['sentence'][0]['Object']

                student_answer_sentense_negation = studentAnswerSentence['negation']

                student_answer_sentense_ner_subject = studentAnswerSentence['ner'][0]['Subject']
                student_answer_sentense_ner_object = studentAnswerSentence['ner'][0]['Object']

                # check ner of the subject
                if (
                        model_answer_sentense_ner_subject != "-2" and model_answer_sentense_ner_subject == student_answer_sentense_ner_subject):
                    # consider subject
                    if (
                        Selected_sentence_modelAnswer_subject.lower() == Selected_sentence_studentAnswer_subject.lower()):
                        mark = mark + (1) * 3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_subject.lower(),
                                                     Selected_sentence_studentAnswer_subject.lower())):
                        mark = mark + (
                                      self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_subject.lower(),
                                                                      Selected_sentence_studentAnswer_subject.lower(),
                                                                      "n")) * 2.5

                    else:
                        mark = mark + self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_subject.lower(),
                                                                      Selected_sentence_studentAnswer_subject.lower(),
                                                                      "n")

                # consider predicate
                # predicate might be or might not be a negation
                # in here checking whether sentences are negations or not
                if (model_answer_sentense_negation == "1" and student_answer_sentense_negation == "1"):

                    # consider predicate
                    if (
                        Selected_sentence_modelAnswer_predicate.lower() == Selected_sentence_studentAnswer_predicate.lower()):
                        mark = mark + (1) * 3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_predicate.lower(),
                                                     Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (self.getSymanticSimilarityValue(
                            Selected_sentence_modelAnswer_predicate.lower(),
                            Selected_sentence_studentAnswer_predicate.lower(), "v")) * 2.5

                    else:
                        mark = mark + self.getSymanticSimilarityValue(
                            Selected_sentence_modelAnswer_predicate.lower(),
                            Selected_sentence_studentAnswer_predicate.lower(), "v")


                elif (model_answer_sentense_negation == "1" and student_answer_sentense_negation == "0"):

                    if (self.isTwoWordsAreAntonyms(Selected_sentence_modelAnswer_predicate.lower(),
                                                   Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (1) * 3

                elif (model_answer_sentense_negation == "0" and student_answer_sentense_negation == "1"):

                    if (self.ntonyms(Selected_sentence_modelAnswer_predicate.lower(),
                                     Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (1) * 3


                elif (model_answer_sentense_negation == "0" and student_answer_sentense_negation == "0"):

                    # consider predicate
                    if (
                        Selected_sentence_modelAnswer_predicate.lower() == Selected_sentence_studentAnswer_predicate.lower()):
                        mark = mark + (1) * 3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_predicate.lower(),
                                                     Selected_sentence_studentAnswer_predicate.lower())):
                        mark = mark + (self.getSymanticSimilarityValue(
                            Selected_sentence_modelAnswer_predicate.lower(),
                            Selected_sentence_studentAnswer_predicate.lower(), "v")) * 2.5

                    else:
                        mark = mark + self.getSymanticSimilarityValue(
                            Selected_sentence_modelAnswer_predicate.lower(),
                            Selected_sentence_studentAnswer_predicate.lower(), "v")

                # check ner of the object
                if (
                        model_answer_sentense_ner_object != "-2" and model_answer_sentense_ner_object == student_answer_sentense_ner_object):
                    # consider object
                    if (
                        Selected_sentence_modelAnswer_object.lower() == Selected_sentence_studentAnswer_object.lower()):
                        mark = mark + (1) * 3

                    elif (self.isTwoWordsAreSynonyms(Selected_sentence_modelAnswer_object.lower(),
                                                     Selected_sentence_studentAnswer_object.lower())):
                        mark = mark + (self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_object.lower(),Selected_sentence_studentAnswer_object.lower(),"n")) * 2.5

                    else:
                        mark = mark + self.getSymanticSimilarityValue(Selected_sentence_modelAnswer_object.lower(),Selected_sentence_studentAnswer_object.lower(),"n")

                # marksObj["marks"].append({"ModelAnswerSentense": modelAnswer_sentence_id, "StudentAnswerSentense": studentAnswer_sentence_id,"Mark": (mark/9)*100})

                # add marks to the marksArray
                marksArray[indexFor2DArray][0] = modelAnswerSentence['sentence'][0]
                marksArray[indexFor2DArray][1] = studentAnswerSentence['sentence'][0]
                marksArray[indexFor2DArray][2] = (mark / 9) * 100
                indexFor2DArray = indexFor2DArray + 1


        return marksArray



