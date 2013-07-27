#!/usr/bin/env python
#coding=utf-8
import time
import sys
import os
import MySQLdb
import dbconn

def now() :
        #return str('2011-01-31 00:00:00')
        return str( time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ) )

def log( qps,tps , logs ) :
        f = file( logs , 'a' , 0 )
        f.write( now() + '  ' + str(qps) +'  '+ str(tps) + '\n' )
        f.close()

def main() :
    logs = "/root/yangql/mysqlqps_tps.xls"
 
    try: 
      conn = MySQLdb.connect(host=dbconn.DB_HOST,port=int(dbconn.DB_PORT),user=dbconn.DB_USER,passwd=dbconn.DB_PASS, charset='utf8')
    except  MySQLdb.ERROR,e:
      print "Error %d:%s"%(e.args[0],e.args[1])
      exit(1)

    conn.autocommit(True)
    cursor=conn.cursor()
    diff = 1
    mystat1={}
    mystat2={}
    sql = "show global status where Variable_name in ('Com_commit','Com_delete','Com_insert','Com_rollback','Com_select','Com_update','Questions');"
    while True:
       try :
          cursor.execute(sql)
          results1 = cursor.fetchall()
          mystat1=dict(results1)
  
          time.sleep(diff)
          cursor.execute(sql)
          results2 = cursor.fetchall()
          mystat2=dict(results2)

          Com_diff = (int(mystat2['Com_commit'])   - int(mystat1['Com_commit']) ) / diff 
          del_diff = (int(mystat2['Com_delete'])   - int(mystat1['Com_delete']) ) / diff
          ins_diff = (int(mystat2['Com_insert'])   - int(mystat1['Com_insert']) ) / diff
          rol_diff = (int(mystat2['Com_rollback']) - int(mystat1['Com_rollback']))/ diff
          sel_diff = (int(mystat2['Com_select'])   - int(mystat1['Com_select']) ) / diff
          upd_diff = (int(mystat2['Com_update'])   - int(mystat1['Com_update']) ) / diff
          que_diff = (int(mystat2['Questions'])    - int(mystat1['Questions']) )  / diff


          qps_s = sel_diff
          tps_iud = del_diff+ins_diff+upd_diff
          qps_ques=que_diff
          tps_Com_rol= Com_diff + rol_diff 
 
          print 'qps_s = %s , qps_ques = %s , tps_iud = %s ,tps_Com_rol = %s'  %(qps_s ,qps_ques, tps_iud,tps_Com_rol)
          #log(qps_s , tps_iud,qps_ques,tps_Com_rol,logs)
       except KeyboardInterrupt :
          print "exit .."
          sys.exit()
  
    conn.close()
if __name__ == '__main__':
   main()
