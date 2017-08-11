from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Questions, MarkingAlgo
from .serializer import QuestionsSerializer, MarkingAlgoSerializer
from answer_mapping.Main import QmarkerMain
from scoring.db import DBConnector
from  postagging.views import postagger
from scoring.teacher_marking_tab import ScoreRfinement
from ner.views import nerTagging
from answer_mapping.answerMapping import answerMapping

import json

# class McqPaperList(APIView):
#
#     def get(self, request):
#         # papers = McqPaper.objects.all()
#         # serializer = McqPaperSerializer(papers, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         return Response(request.data)

class AddQuestions(APIView):

    def post(self, request):
        query = Questions(question=request.data['question'], answer=request.data['answer'], mark=request.data['mark'])
        query.save()

        qid = query.id
        marks = request.data['mark']

        print("sss")
        # get pos count of the answer
        postaggerObj = postagger()
        posCount = postaggerObj.getTripletsCount(request.data['answer'])

        print(posCount)

        # add data to aravindas table
        DBConnector().new_question(qid, marks, posCount)
        return Response(request.data)

class GetQuestions(APIView):

    def get(self, request):
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data)

class MarkQuestions(APIView):

    def post(self, request):

        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)

        answer = ''
        q_mark = ''
        for i in serializer.data:
            if i['id'] == request.data['qid']:
                answer = i['answer']
                q_mark = i['mark']


        mark = QmarkerMain.compareTwoAnswers(self, answer, request.data['answer'], request.data['qid'])

        return Response('%s/%s' % (mark, q_mark))

class addTrainingData(APIView):

    def post(self, request):

        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)

        # teacher giver answer and question id
        teachersAnswer = request.data['answer']
        qid = request.data['qid']

        # get model answer for the question
        answer = ''
        for i in serializer.data:
            if i['id'] == qid:
                answer = i['answer']

        sentenceComparisonObj =   QmarkerMain.compareTwoAnswersAndGetSentenseComparisonData(self,answer,teachersAnswer)

        ScoreRfinement().RefineScore(sentenceComparisonObj,qid,request.data['mark'])
        return Response("done")

class tripletExtraction(APIView):

    def post(self, request):

        sen1 = request.data['sen1']
        sen2 = request.data['sen2']
        tripletObj1 = postagger().extraxtedTriplets(sen1)
        tripletObj2 = postagger().extraxtedTriplets(sen2)

        data = {}
        data['Sentence1'] = tripletObj1
        data['Sentence2'] = tripletObj2


        return Response(json.dumps(data))

class nerExtraction(APIView):

    def post(self, request):

        sen1 = request.data['sen1']
        sen2 = request.data['sen2']
        tripletObj1 = postagger().extraxtedTriplets(sen1)
        tripletObj2 = postagger().extraxtedTriplets(sen2)

        nerObject1 = nerTagging().settingNER(tripletObj1)
        nerObject2 = nerTagging().settingNER(tripletObj2)

        data = {}
        data['Sentence1'] = nerObject1
        data['Sentence2'] = nerObject2


        return Response(json.dumps(data))

class sentenceComparision(APIView):

    def post(self, request):

        sen1 = request.data['sen1']
        sen2 = request.data['sen2']
        tripletObj1 = postagger().extraxtedTriplets(sen1)
        tripletObj2 = postagger().extraxtedTriplets(sen2)

        nerObject1 = nerTagging().settingNER(tripletObj1)
        nerObject2 = nerTagging().settingNER(tripletObj2)

        marksObj = answerMapping().compareAnswersAndReturnMatchingPairsPrototype(nerObject1,nerObject2)

        data = {}
        data['Sentence1'] = nerObject1
        data['Sentence2'] = nerObject2
        data['marks'] = marksObj


        return Response(json.dumps(data))