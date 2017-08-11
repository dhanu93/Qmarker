import pymysql

class DBConnector:


    def create_DB_Connection(self):
        conn = pymysql.connect(host='localhost', user='root', password='', db='preview_two')
        return conn

    def new_question(self,id_new, mark_given, point_given):
        conn = self.create_DB_Connection()

        mark_new = float(mark_given)
        point_new = int(point_given)
      #  ids = idd
        system = 100
        avg_mark = mark_new/point_new*system/100
        weight1 = 1
        insert1 = conn.cursor()
        #insert1.execute("INSERT INTO `testing`(name) VALUES('%s');"% ('kaz'))
        insert1.execute("INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (id_new, mark_new, point_new, system, avg_mark,weight1))
        conn.commit()
     #   ids = ids + 1
        #################################################
        system = 75
        avg_mark = mark_new / point_new * system / 100
        weight1 = 1
        insert2 = conn.cursor()
        insert2.execute("INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (id_new, mark_new, point_new, system, avg_mark, weight1))
        conn.commit()
     #   ids = ids + 1
        #######################################################
        system = 50
        avg_mark = mark_new / point_new * system / 100
        weight1 = 1
        insert3 = conn.cursor()
        insert3.execute("INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (id_new, mark_new, point_new, system, avg_mark, weight1))
        conn.commit()
     #   ids = ids + 1
        #####################################################
        system = 30
        avg_mark = mark_new / point_new * system / 100
        weight1 = 1
        insert4 = conn.cursor()
        insert4.execute("INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (id_new, mark_new, point_new, system, avg_mark, weight1))
        conn.commit()

    def checkk(self,qqq_id, mark, point):
        conn = self.create_DB_Connection()
        check = conn.cursor()
        new_mark_for_check = mark
        new_point_for_check = point

        sql_check = 'SELECT `Q_id` FROM `marking_algo` WHERE `mark` = %s and `point` = %s;' % (new_mark_for_check, new_point_for_check)
        pointz = check.execute(sql_check)
        print("number of rows :", pointz)
       # check.execute(sql_check)
        #data = check.fetchone()
      #  for d in range(0, point):
         #   selected_q_numbers = (data[d])


       # print(selected_q_numbers)




        a =91
        qqqqqq = 126
        if(a> 90):

            get = conn.cursor()
            sql_get1 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qqqqqq, 100)
            pointz = get.execute(sql_get1)
            print("number of rows :", pointz)
            get.execute(sql_get1)
            data = get.fetchone()
            avgg1 = data[5]
            wei1 = data[6]
            #######################################################
            sql_get2 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qqqqqq, 75)
            pointz = get.execute(sql_get2)
            print("number of rows :", pointz)
            get.execute(sql_get2)
            data = get.fetchone()
            avgg2 = data[5]
            wei2 = data[6]
            #############################################################
            sql_get3 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qqqqqq, 50)
            pointz = get.execute(sql_get3)
            print("number of rows :", pointz)
            get.execute(sql_get3)
            data = get.fetchone()
            avgg3 = data[5]
            wei3 = data[6]
            #################################################################
            sql_get4 = 'SELECT * FROM `marking_algo` WHERE `q_id` = %s and `system` = %s;' % (qqqqqq, 30)
            pointz = get.execute(sql_get4)
            print("number of rows :", pointz)
            get.execute(sql_get4)
            data = get.fetchone()
            avgg4 = data[5]
            wei4 = data[6]
            ######################################################################################################################
            setinsert1 = conn.cursor()
            setinsert1.execute(
                "INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (
                qqq_id, mark, point, 100, avgg1, wei1))
            conn.commit()
            ###################################################
            setinsert2 = conn.cursor()
            setinsert2.execute(
                "INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (
                qqq_id, mark, point, 75, avgg2, wei2))
            conn.commit()
            #############################################
            setinsert3 = conn.cursor()
            setinsert3.execute(
                "INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (
                qqq_id, mark, point, 50, avgg3, wei3))
            conn.commit()
            ##############################################
            setinsert4 = conn.cursor()
            setinsert4.execute(
                "INSERT INTO `marking_algo`(q_id, mark, point, system, teacher_avg, weight) VALUES('%s','%s','%s','%s','%s','%s');" % (
                qqq_id, mark, point, 30, avgg4, wei4))
            conn.commit()





    # checkk(131,6,3)


    # new_question(130, 10, 4)
    # print("heeeee")