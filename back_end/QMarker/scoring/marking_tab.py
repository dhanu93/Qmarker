import pymysql
import json

from scoring.db import DBConnector

ara = '{' \
        '"markedSentences": [' \
            '{"ModeAanswer" : "1","StudentAnswer" : "1","mark" : "100"},' \
            '{"ModeAanswer" : "2","StudentAnswer" : "3","mark" : "80"},' \
            '{"ModeAanswer" : "3","StudentAnswer" : "2","mark" : "2"},' \
            '{"ModeAanswer" : "4","StudentAnswer" : "-1","mark" : "-1"}' \
        ']' \
       '}'

class MarkAnswer:

    def MarkSentences(self,marks,q_id):

        dbConnector = DBConnector()
        conn = dbConnector.create_DB_Connection()


        numberofmodelans=0
        answered=0
        for studentAnswer_sentence_id, answerSentence in enumerate(marks['markedSentences']):
            numberofmodelans = numberofmodelans + 1
            # print(answerSentence['ModeAanswer'])
            if(answerSentence['StudentAnswer']!="-1" ):

                answered = answered + 1


        numberofmodelans=0
        answered=0
        mark_for_question =0

        #if(data[3] != numberofmodelans):
        #   print("Kazzo model answers gane aulak")

        for studentAnswer_sentence_id, answerSentence in enumerate(marks['markedSentences']):
            # print(answerSentence['ModeAanswer'])
            if(answerSentence['StudentAnswer']!="-1" ):
                if(int(float(answerSentence['mark'])) == 100):
                    #import pymysql

                    a = conn.cursor()
                    present = 100

                    sql10 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (q_id, present)

                    point = a.execute(sql10)
                    print("number of rows :", point)
                    a.execute(sql10)
                    data = a.fetchone()

                    if(data[3] != numberofmodelans):
                        print("Kazzo model answers gane aulak")

                    mark_for_question = mark_for_question + data[5]

                elif(int(float(answerSentence['mark'])) >= 75):

                    a = conn.cursor()
                    present = 75

                    sql11 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (q_id, present)

                    point = a.execute(sql11)
                    print("number of rows :", point)
                    a.execute(sql11)
                    data = a.fetchone()

                    if(data[3] != numberofmodelans):
                        print("Kazzo model answers gane aulak")

                    mark_for_question = mark_for_question + data[5]
                    ################################################################################
                elif (int(float(answerSentence['mark'])) >= 50):

                    a = conn.cursor()
                    present = 50

                    sql12 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (q_id, present)

                    point = a.execute(sql12)
                    print("number of rows :", point)
                    a.execute(sql12)
                    data = a.fetchone()

                    if (data[3] != numberofmodelans):
                        print("Kazzo model answers gane aulak")

                    mark_for_question = mark_for_question + data[5]

                elif (int(float(answerSentence['mark'])) >= 30):

                    a = conn.cursor()
                    present = 30

                    sql13= 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (q_id, present)

                    point = a.execute(sql13)
                    print("number of rows :", point)
                    a.execute(sql13)
                    data = a.fetchone()

                    if(data[3] != numberofmodelans):
                        print("Kazzo model answers gane aulak")

                    mark_for_question = mark_for_question + data[5]
                else:


                    mark_for_question = 0 + mark_for_question

        # print("ha haa")
        return mark_for_question
