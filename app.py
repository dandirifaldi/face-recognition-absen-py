from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify,json
import mysql.connector
import cv2
from PIL import Image
import numpy as np
import os
import time
from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.secret_key = 'why would I tell you my secret key?'
app.secret_key = 'ini secret key'
 
cnt = 0
pause_cnt = 0
justscanned = False
 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="fr_absen",
    auth_plugin='mysql_native_password'
)
mycursor = mydb.cursor(buffered=True)
 
 
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generate dataset >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def generate_dataset(nbr):
    face_classifier = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
 
    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5
 
        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face
 
    cap = cv2.VideoCapture(0)
 
    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]
 
    img_id = lastid
    max_imgid = img_id + 100
    count_img = 0
 
    while True:
        ret, img = cap.read()
        if face_cropped(img) is not None:
            count_img += 1
            img_id += 1
            face = cv2.resize(face_cropped(img), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
 
            file_name_path = "dataset/"+nbr+"."+ str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
 
            mycursor.execute("""INSERT INTO `img_dataset` (`img_id`, `img_mahasiswa`) VALUES
                                ('{}', '{}')""".format(img_id, nbr))
            mydb.commit()
 
            frame = cv2.imencode('.jpg', face)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
            if cv2.waitKey(1) == 13 or int(img_id) == int(max_imgid):
                break
                cap.release()
                cv2.destroyAllWindows()
 
 
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Train Classifier >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/train_classifier/<nbr>')
def train_classifier(nbr):
    dataset_dir = "dataset"
 
    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
    faces = []
    ids = []
 
    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])
 
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)
 
    # Train the classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
 
    return redirect('/mahasiswa')
 
 
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def face_recognition(kode_mk):  # generate frame by frame from camera
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
 
        global justscanned
        global pause_cnt
 
        pause_cnt += 1
 
        coords = []
 
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))
            print("id = {}, pred = {},confidence = {}".format(id,pred,confidence))
 
            if confidence > 76 and not justscanned:
                global cnt
                cnt += 1
 
                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w
                cv2.putText(img, str(int(n-3))+' %', (x + 20, y + h + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
 
                cv2.rectangle(img, (x, y + h + 40), (x + w, y + h + 50), color, 2)
                cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled), y + h + 50), (153, 255, 255), cv2.FILLED)
                
                mycursor.execute("select a.img_mahasiswa, b.nrp, b.nama_mhs"
                                 " from img_dataset a "
                                 " left join mahasiswa b on a.img_mahasiswa = b.nrp "
                                 " join mk_mhs c on b.nrp = c.nrp "
                                 " where img_id = " + str(id)+" and c.kode_mk = "+str(kode_mk))
                row = mycursor.fetchone()
                query_yang_dijalankan = mycursor.statement
                print("Query yang dijalankan:", query_yang_dijalankan)
                print("row = ",row)
                
                mk = kode_mk
                pnbr = row[0]
                pnrp = row[1]
                pname = row[2]
                # if int(cnt) == 30 and row is not None:
                if int(cnt) == 30 :
                    # pnbr = row[0]
                    # pnrp = row[1]
                    # pname = row[2]
                    cnt = 0
                    

                    mycursor.execute("insert into absensi (tanggal_absen,kode_mk, absen_mhs) values('"+str(date.today())+"','"+ mk +"', '" + pnbr + "')")
                    mydb.commit()
 
                    cv2.putText(img, pname + ' | ' + pnrp, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
                    time.sleep(1)
 
                    justscanned = True
                    pause_cnt = 0
 
                # elif(int(cnt)>30):
                # # else:
                #     cnt=0
                #     cv2.putText(img,' | ', (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
                #     time.sleep(1)

                #     pause_cnt = 0
                #     justscanned=True
            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,cv2.LINE_AA)
                if pause_cnt > 80:
                    justscanned = False
 
            coords = [x, y, w, h]
        return coords
 
    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img
 
    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
 
    wCam, hCam = 400, 400
 
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
 
    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)
 
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
 
        key = cv2.waitKey(1)
        if key == 27:
            break
 
 
 
@app.route('/')
def home():
    if session.get('user'):
            hari = {
                '1':"Senin",
                '2':"Selasa",
                '3':"Rabu",
                '4':"Kamis",
                '5':"Jum'at",
                '6':"Sabtu",
                '0':"Minggu",
            }
            x = datetime.now()
            x1 = x.strftime("%d %B %Y")
            y=hari[x.strftime("%w")]
            z=x.strftime("%H:%M:%S")
            mycursor.execute("""select jam_mulai from jadwal ORDER BY jam_mulai DESC LIMIT 1 """)
            # mycursor.execute("""select jam_mulai from jadwal where jadwal.hari = '{}'""".format(y))
            result = mycursor.fetchone()
            waktu_awal=result[0] if result else datetime.now()
            waktu_akhir = waktu_awal + timedelta(minutes=15)
            waktu_awal -= timedelta(minutes=10)
            print("waktu awal : ",waktu_awal)
            print("waktu akhir : ",waktu_akhir)
            # Format datetime menjadi string yang sesuai untuk query MySQL
            # format_waktu = "%H:%M:%S"
            # waktu_awal_str = waktu_awal.strftime(format_waktu)
            # waktu_akhir_str = waktu_akhir.strftime(format_waktu)
            # if z>=jam_mulai:

            # mycursor.execute("""select * from mata_kuliah join jadwal on jadwal.kode_mk = mata_kuliah.kode_mk where jadwal.hari = '{}' and jadwal.jam_mulai >=  '{}' and jadwal.jam_mulai <= '{}'""".format(y,waktu_awal,waktu_akhir))
            mycursor.execute("""select * from mata_kuliah join jadwal on jadwal.kode_mk = mata_kuliah.kode_mk where jadwal.hari = '{}' and jadwal.jam_akhir >= NOW() """.format(y,waktu_awal,waktu_akhir))
            data = mycursor.fetchall()
            # query_yang_dijalankan = mycursor.statement
            # print("Query yang dijalankan:", query_yang_dijalankan)
    
            return render_template('index.html', data=data,x=x1,y=y)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/mahasiswa')
def mahasiswa():
    mycursor.execute("select nrp, nama_mhs, jenis_kel, email, status, date_added from mahasiswa")
    data = mycursor.fetchall()
    data_count = len(data)
    return render_template('mahasiswa.html', data=data,data_count=data_count)

@app.route('/mata_kuliah')
def dataMatkul():
    i=1
    mycursor.execute("select a.kode_mk, a.nama_mk, a.semester, b.ruangan, b.hari, b.jam_mulai, a.sks, a.nama_dosen from mata_kuliah a left join jadwal b on a.kode_mk = b.kode_mk")
    data = mycursor.fetchall()
    return render_template('matkul.html', data=data,i=i)
 
@app.route('/addmhs')
def addmhs():
    mycursor.execute("select ifnull(max(nrp) + 1, 0) from mahasiswa")
    row = mycursor.fetchone()
    nbr = row[0]
    # print(int(nbr))
 
    return render_template('addmhs.html')

@app.route('/addmatkul')
def addmatkul():
    mycursor.execute("select ifnull(max(nrp) + 1, 0) from mahasiswa")
    row = mycursor.fetchone()
    nbr = row[0]
    # print(int(nbr))
 
    return render_template('addmatkul.html')
 
@app.route('/addmhs_submit', methods=['POST'])
def addmhs_submit():
    nrp = request.form.get('nrp')
    nama_mhs = request.form.get('nama_mhs')
    jk = request.form.get('jk')
    email = request.form.get('email')
    no_telp = request.form.get('no_telp')
    tmpt_lhr = request.form.get('tmpt_lahir')
    tgl_lhr = request.form.get('tgl_lahir')
    alamat = request.form.get('alamat')
    status = "1"
 
    mycursor.execute("""INSERT INTO `mahasiswa` (`nrp`, `nama_mhs`, `jenis_kel`,`email`,
      `no_telp`, `tmpt_lhr`,`tgl_lhr`,`alamat`,`status`) VALUES
                    ('{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}')""".format(nrp, nama_mhs, jk, email, no_telp, tmpt_lhr, tgl_lhr, alamat, status))
    mydb.commit()
 

    return redirect(url_for('vfdataset_page', nrp=nrp))

@app.route('/addmatkul_submit', methods=['POST'])
def addmatkul_submit():
    a = request.form.get('kode_mk')
    b = request.form.get('nama_mk')
    c = request.form.get('sem')
    d = request.form.get('ruangan')
    e = request.form.get('hari')
    f = request.form.get('jam_mulai')
    g = request.form.get('jam_akhir')
    h = request.form.get('sks')
    i = request.form.get('nama_dosen')
 
    mycursor.execute("""INSERT INTO `mata_kuliah` (`kode_mk`, `nama_mk`, `semester`,`sks`,`nama_dosen`) VALUES
                    ('{}', '{}', '{}','{}', '{}')""".format(a, b, c, h,i))
    mydb.commit()
    mycursor.execute("""INSERT INTO `jadwal` (`kode_mk`,`ruangan`,`hari`, `jam_mulai`,`jam_akhir`) VALUES
                    ('{}', '{}', '{}','{}', '{}')""".format(a, d, e, f, g))
    mydb.commit()
 
    return redirect(url_for('dataMatkul'))

@app.route('/delete_matkul/<kode_mk>', methods=['GET'])
def deletematkul_submit(kode_mk):
    mycursor.execute("""DELETE FROM `absensi` WHERE `kode_mk` = '{}';""".format(kode_mk))
    mydb.commit()
    mycursor.execute("""DELETE FROM `mk_mhs` WHERE `kode_mk` = '{}';""".format(kode_mk))
    mydb.commit()
    mycursor.execute("""DELETE FROM `jadwal` WHERE `kode_mk` = '{}';""".format(kode_mk))
    mydb.commit()
    mycursor.execute("""DELETE FROM `mata_kuliah` WHERE `kode_mk` = '{}';""".format(kode_mk))
    mydb.commit()
 
    return redirect(url_for('dataMatkul'))

@app.route('/delete_mhs/<nrp>', methods=['GET'])
def deletemhs_submit(nrp):
    mycursor.execute("""DELETE FROM `absensi` WHERE `absen_mhs` = '{}';""".format(nrp))
    mydb.commit()
    mycursor.execute("""DELETE FROM `mk_mhs` WHERE `nrp` = '{}';""".format(nrp))
    mydb.commit()
    mycursor.execute("""select img_id from img_dataset where img_mahasiswa = '{}' order by img_id limit 1""".format(nrp))
    img_awal = mycursor.fetchone()
    img_awal_a=img_awal[0]
    mycursor.execute("""select img_id from img_dataset where img_mahasiswa = '{}' order by img_id desc limit 1""".format(nrp))
    img_akhir = mycursor.fetchone()
    img_akhir_a = img_akhir[0]
    for i in range(img_awal_a,img_akhir_a+1):
        file_name_path = "dataset/"+nrp+"."+ str(i) + ".jpg"
        os.remove(file_name_path)
    mycursor.execute("""DELETE FROM `img_dataset` WHERE `img_mahasiswa` = '{}';""".format(nrp))
    mydb.commit()
    mycursor.execute("""DELETE FROM `mahasiswa` WHERE `nrp`= '{}';""".format(nrp))
    mydb.commit()
 
    return redirect(url_for('mahasiswa'))

@app.route('/delete_matkul_mhs/<kode_mk>/<nrp>', methods=['GET'])
def deletematkul_mhs_submit(kode_mk,nrp):
    mycursor.execute("""DELETE FROM `mk_mhs` WHERE `nrp` = '{}';""".format(nrp))
    mydb.commit()
    return redirect(url_for('matkul_mhs', kode_mk=kode_mk))
 
@app.route('/vfdataset_page/<nrp>')
def vfdataset_page(nrp):
    return render_template('gendataset.html', nrp=nrp)
 
@app.route('/vidfeed_dataset/<nbr>')
def vidfeed_dataset(nbr):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_dataset(nbr), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/video_feed/<kode_mk>')
def video_feed(kode_mk):
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognition(kode_mk), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/fr_page')
def fr_page():
    """Video streaming home page."""
    mycursor.execute("select a.id_absen, a.absen_mhs, b.nama_mhs, b.email, a.tanggal_absen "
                     "  from absensi a "
                     "  left join mahasiswa b on a.absen_mhs = b.nrp "
                     " where a.tanggal_absen = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()
 
    return render_template('fr_page.html', data=data)
 
 
@app.route('/absen/<id>')
def absensi_matkul(id):
    """Video streaming home page."""
    mycursor.execute("select a.id_absen, a.kode_mk, a.absen_mhs, b.nama_mhs, b.email, a.tanggal_absen "
                     "  from absensi a "
                     "  left join mahasiswa b on a.absen_mhs = b.nrp "
                     " where a.tanggal_absen = curdate() and a.kode_mk = "+ id +
                     " order by 1 desc")
    data = mycursor.fetchall()
    # print(data)
    # query_yang_dijalankan = mycursor.statement
    # print("Query yang dijalankan:", query_yang_dijalankan)
    mycursor.execute("""select nama_mk from mata_kuliah where kode_mk = '{}'""".format(id))
    nama_mk = mycursor.fetchone()
    nama_mk=nama_mk[0]
    id_mk=id
    x = datetime.now()
    x1 = x.strftime("%d %B %Y")
    hari = {
        '1':"Senin",
        '2':"Selasa",
        '3':"Rabu",
        '4':"Kamis",
        '5':"Jum'at",
        '6':"Sabtu",
        '0':"Minggu",
    }
    y=hari[x.strftime("%w")]
    return render_template('fr_page.html', data=data,id=id_mk,x=x1,y=y,nama_mk=nama_mk)
 
@app.route('/countTodayScan')
def countTodayScan():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="fr_absen",
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
 
    mycursor.execute("select count(*) "
                     "  from absensi "
                     " where tanggal_absen = curdate() ")
    row = mycursor.fetchone()
    rowcount = row[0]
 
    return jsonify({'rowcount': rowcount})
 
 
@app.route('/loadData/<id>', methods = ['GET', 'POST'])
def loadData(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="fr_absen",
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
 
    mycursor.execute("select a.id_absen, a.absen_mhs, b.nama_mhs, b.email, date_format(a.waktu_absen, '%H:%i:%s') "
                     "  from absensi a "
                     "  left join mahasiswa b on a.absen_mhs = b.nrp "
                     " where a.tanggal_absen = curdate() and a.kode_mk = "+ id +
                     " order by 1 desc")
    data = mycursor.fetchall()
 
    return jsonify(response = data)

@app.route('/matkul_mhs/<kode_mk>')
def matkul_mhs(kode_mk):
    mycursor.execute("select * from mk_mhs a "
                     "join mata_kuliah b on a.kode_mk = b.kode_mk "
                     "join jadwal c on b.kode_mk = c.kode_mk "
                     "join mahasiswa d on a.nrp = d.nrp "
                     "where a.kode_mk = "+ kode_mk)
    data_all = mycursor.fetchall()
    data_all_count=len(data_all)
    mycursor.execute("select * from mahasiswa")
    data_mhs = mycursor.fetchall()
    mycursor.execute("select * from mata_kuliah a "
                     "join jadwal b on a.kode_mk=b.kode_mk "
                     "where a.kode_mk = "+ kode_mk)
    data_matkul_jadwal = mycursor.fetchone()
 
    return render_template('matkul_mhs.html', data_matkul_jadwal=data_matkul_jadwal,data_all=data_all,data_all_count=data_all_count,data_mhs=data_mhs)

@app.route('/addmatkul_mhs_submit', methods=['POST'])
def addmatkul_mhs_submit():
    a = request.form.get('kode_mk')
    b = request.form.get('mhs')
    if b!="0":
        mycursor.execute("""INSERT INTO `mk_mhs` (`kode_mk`, `nrp`) VALUES
                    ('{}', '{}')""".format(a, b))
        mydb.commit()

    # return redirect(url_for('home'))
    return redirect(url_for('matkul_mhs',kode_mk=a))

@app.route('/detail_mk/<kode_mk>')
def detal_mk(kode_mk):
    hari = {
        '1':"Senin",
        '2':"Selasa",
        '3':"Rabu",
        '4':"Kamis",
        '5':"Jum'at",
        '6':"Sabtu",
        '0':"Minggu",
    }
    x = datetime.now()
    x1 = x.strftime("%d %B %Y")
    y=hari[x.strftime("%w")]
    z=x.strftime("%H:%M:%S")
    # mycursor.execute("select * from absensi a "
    #                  "join jadwal b on a.kode_mk=b.kode_mk "
    #                 #  "join mata_kuliah c on a.kode_mk=c.kode_mk "
    #                  "where a.kode_mk = "+ kode_mk)
    # data_all = mycursor.fetchall()
    mycursor.execute("""select * from mata_kuliah join jadwal on jadwal.kode_mk = mata_kuliah.kode_mk where mata_kuliah.kode_mk = '{}' """.format(kode_mk))
    data_matkul_jadwal = mycursor.fetchone()
    hari_absen= data_matkul_jadwal[8]
    mycursor.execute("select b.nrp, b.nama_mhs, count(a.tanggal_absen) from absensi a "
                     "join mahasiswa b on b.nrp=a.absen_mhs "
                    #  "join jadwal c on c.kode_mk=b.kode_mk "
                     "where a.kode_mk = "+ kode_mk + " group by b.nrp")
                    #  " and c.hari = "+ hari_absen)
    data_all = mycursor.fetchall()
    print(data_all)
    query_yang_dijalankan = mycursor.statement
    print("Query yang dijalankan:", query_yang_dijalankan)
    data_all_count=len(data_all)
    return render_template('detail_mk.html',data_matkul_jadwal=data_matkul_jadwal, data_all=data_all,x=x1,y=y,data_all_count=data_all_count)


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            # conn = mysql.connect()
            cursor = mydb.cursor(buffered=True)
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                mydb.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        mycursor.close()

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        hari = {
            '1':"Senin",
            '2':"Selasa",
            '3':"Rabu",
            '4':"Kamis",
            '5':"Jum'at",
            '6':"Sabtu",
            '0':"Minggu",
        }
        x = datetime.now()
        x1 = x.strftime("%d %B %Y")
        y=hari[x.strftime("%w")]
        z=x.strftime("%H:%M:%S")
        mycursor.execute("""select jam_mulai from jadwal ORDER BY jam_mulai DESC LIMIT 1 """)
        # mycursor.execute("""select jam_mulai from jadwal where jadwal.hari = '{}'""".format(y))
        result = mycursor.fetchone()
        waktu_awal=result[0] if result else datetime.now()
        waktu_akhir = waktu_awal + timedelta(minutes=15)
        waktu_awal -= timedelta(minutes=10)
        print("waktu awal : ",waktu_awal)
        print("waktu akhir : ",waktu_akhir)
        # Format datetime menjadi string yang sesuai untuk query M          ySQL
        # format_waktu = "%H:%M:%S"
        # waktu_awal_str = waktu_awal.strftime(format_waktu)
        # waktu_akhir_str = waktu_akhir.strftime(format_waktu)
        # if z>=jam_mulai:

        # mycursor.execute("""select * from mata_kuliah join jadwal on jadwal.kode_mk = mata_kuliah.kode_mk where jadwal.hari = '{}' and jadwal.jam_mulai >=  '{}' and jadwal.jam_mulai <= '{}'""".format(y,waktu_awal,waktu_akhir))
        mycursor.execute("""select * from mata_kuliah join jadwal on jadwal.kode_mk = mata_kuliah.kode_mk where jadwal.hari = '{}' and jadwal.jam_akhir >= NOW() """.format(y,waktu_awal,waktu_akhir))
        data = mycursor.fetchall()
        # query_yang_dijalankan = mycursor.statement
        # print("Query yang dijalankan:", query_yang_dijalankan)
    
        return render_template('index.html', data=data,x=x1,y=y)
    else:
        return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        print(_username)
        # connect to mysql 
        # con = mysql.connect()
        cursor = mydb.cursor(buffered=True)
        mycursor.execute("select * from tbl_user where user_username = '"+_username+"'")
                    #  " and c.hari = "+ hari_absen)
        data = mycursor.fetchall()
        # cursor.callproc('sp_validateLogin',(_username,))
        # data = cursor.fetchall()
        print(data)
        print("==========")
        print(check_password_hash(str(data[0][3]),_password))
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/showSignin')
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)