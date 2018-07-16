import psycopg2
import csv
from datetime import timedelta


hostname = 'ec2-174-129-206-173.compute-1.amazonaws.com'
username = 'dwurdtkxyqwlnn'
password = 'b98d3fc241b9feadac180e17989fec12920f8daf94ca8d1d2ae31025d136e939'
database = 'dfdtpbeic1csbo'


def doQuery( conn ) :
    cantidad_trabajadores = 31
    hours = 0
    minute = 0
    sec = 0
    time = 0
    vector_tiempo = [0] * cantidad_trabajadores
    vector_cantidad = [0] * cantidad_trabajadores
    vector_nombres = [0] * cantidad_trabajadores
    start_date="2018-06-01"
    end_date="2018-06-30"

    cur = conn.cursor()
    cur.execute("select auth_user.id,auth_user.username,records_attendance.start_date,records_attendance.end_date,(records_attendance.end_date-records_attendance.start_date ) as dif  from auth_user left join records_attendance on auth_user.id=records_attendance.user_id  where records_attendance.start_date >= '"+start_date+"' AND records_attendance.start_date < '"+end_date+"' order by records_attendance.user_id")


    with open('asistencia.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["id_usuario", "Nombre", "Checkins", "Tiempo"])
        for id,username,start,end,dif in cur.fetchall():
            aux=str(dif)
            array=aux.split(":")
            try:
                hours=array[0]
                minute=array[1]
                sec=(array[2].split("."))[0]
                time=int(hours)*60+int(minute)
            except:
                hours=8
                minute=0
                sec=0
                time = 8*60

            vector_tiempo[int(id)]=vector_tiempo[int(id)]+time
            vector_cantidad[int(id)]=vector_cantidad[int(id)]+1
            vector_nombres[int(id)]=username

        for i in range(len(vector_tiempo)):
            if vector_nombres[i]!=0:
                print(i, vector_nombres[i], vector_cantidad[i], vector_tiempo[i])
                spamwriter.writerow([i, vector_nombres[i], vector_cantidad[i], vector_tiempo[i]/60])



myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
doQuery(myConnection)
myConnection.close()