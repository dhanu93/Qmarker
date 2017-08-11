import json
import pymysql
from scoring.db import DBConnector

# # methanata thamai teachergen mark karanda ona ans eka load karana thana
# ara = '{' \
#         '"markedSentences": [' \
#             '{"ModeAanswer" : "1","StudentAnswer" : "1","mark" : "100"},' \
#             '{"ModeAanswer" : "2","StudentAnswer" : "3","mark" : "80"},' \
#             '{"ModeAanswer" : "3","StudentAnswer" : "2","mark" : "2"}' \
#         ']' \
#        '}'
# marks = json.loads(ara)

class ScoreRfinement:

    # marks = json object which contains comparission data of two answers
    def RefineScore(self, marks,qq_id,teachers_marks):
        dbConnector = DBConnector()
        conn = dbConnector.create_DB_Connection()

        teachers_mark = float(teachers_marks)
        # qq_id = 126 # methanata question id eka ona

        i = 0
        arr_mark = [-1]*len(marks['markedSentences'])

        for studentAnswer_sentence_id, answerSentence in enumerate(marks['markedSentences']):
            #numberofmodelans = numberofmodelans + 1
            #print(answerSentence['ModeAanswer'])
            if(answerSentence['StudentAnswer']!="-1" ):
               # print(answerSentence['mark'])
               # answered = answered + 1
               arr_mark[i] = float (answerSentence['mark'])
               i = i + 1

        divi = 0
        compo = 0
        for j in arr_mark:
            if(j >30):
                divi = divi + j
                compo = compo + 1

        # teachers_mark = 4 # methanata thamai adala prashnayata teacher dipu lakunu gana assign karanda ona

        for z in arr_mark:
            if(z == 100):
                up1 = conn.cursor()
                present = 100
                sqlup1 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qq_id, present)
                point = up1.execute(sqlup1)
                print("number of rows :", point)
                up1.execute(sqlup1)
                data = up1.fetchone()
                avg = data[5]
                print("menna db 1a avg eka")
                print(data[5])
                wei = data[6]
                avg = ((avg*wei+(teachers_mark/divi*100))/(wei+1))
                wei = wei+1
                print(avg)
                if(data[2]/data[3] < avg):
                    avg = data[2]/data[3]
                b = conn.cursor()
                sql2 = 'UPDATE `marking_algo` SET teacher_avg'
                sql2 += '= %s, weight = %s WHERE `q_id` = %s and `system` = %s;' % (avg, wei, qq_id, present)
                b.execute(sql2)
                conn.commit()

            if(z >= 75 and z< 100):
                up2 = conn.cursor()
                present = 75
                sqlup2 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qq_id, present)
                point = up2.execute(sqlup2)
                print("number of rows :", point)
                up2.execute(sqlup2)
                data = up2.fetchone()
                avg = data[5]
                wei = data[6]
                print("menna weight 1a")
                print(data[6])
                avg = ((avg*wei+(teachers_mark / divi * z)) / (wei+1))
                wei = wei+1
                print(avg)
                if(data[2]/data[3] < avg):
                    avg = data[2]/data[3]
                c = conn.cursor()
                sql3 = 'UPDATE `marking_algo` SET teacher_avg'
                sql3 += '= %s, weight = %s WHERE `q_id` = %s and `system` = %s;' % (avg, wei, qq_id, present)
                c.execute(sql3)
                conn.commit()

            if(z >= 50 and z<75):
                up3 = conn.cursor()
                present = 50
                sqlup3 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qq_id, present)
                point = up3.execute(sqlup3)
                print("number of rows :", point)
                up3.execute(sqlup3)
                data = up3.fetchone()
                avg = data[5]
                wei = data[6]
                avg = ((avg*wei + (teachers_mark / divi * z)) / (wei+1))
                wei = wei+1
                print(avg)
                if(data[2]/data[3] < avg):
                    avg = data[2]/data[3]
                d = conn.cursor()
                sql4 = 'UPDATE `marking_algo` SET teacher_avg'
                sql4 += '= %s, weight = %s WHERE `q_id` = %s and `system` = %s;' % (avg, wei, qq_id, present)
                d.execute(sql4)
                conn.commit()

            if (z >= 30 and z< 50):
                up4 = conn.cursor()
                present = 30
                sqlup4 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qq_id, present)
                point = up4.execute(sqlup4)
                print("number of rows :", point)
                up4.execute(sqlup4)
                data = up4.fetchone()
                avg = data[5]
                wei = data[6]
                avg = ((avg * wei + (teachers_mark / divi * z)) / (wei + 1))
                wei = wei + 1
                print(avg)
                if(data[2]/data[3] < avg):
                    avg = data[2]/data[3]
                e = conn.cursor()
                sql5 = 'UPDATE `marking_algo` SET teacher_avg'
                sql5 += '= %s, weight = %s WHERE `q_id` = %s and `system` = %s;' % (avg, wei, qq_id, present)
                e.execute(sql5)
                conn.commit()


