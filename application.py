"""python sertifikat-massal.py"""
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, send_file, request, Response
import os
import pymysql
pymysql.install_as_MySQLdb()
from werkzeug.utils import import_string, redirect
import PyCertGen
import common_utils
from flask.helpers import flash
from flask_mysqldb import MySQL, MySQLdb
import xlrd
import mysql.connector
import tambahan
import mimetypes
import subprocess
import shutil

# file-file html berada di folder templates
TEMPLATES = "templates"

app = Flask(__name__, static_folder="assets", template_folder=TEMPLATES)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Standard File Size
ROOT_DIR = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))


app = Flask(__name__)
app = Flask(__name__, static_folder="assets")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)


# Reloading
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/unggah-desain')
def base():
    return render_template('unggah-desain.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/uploaddocxsukses', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        #kosongkan file didalam folder penyimpanan sementara
        lokasifoldernya = "../sertifmassal/PenyimpananSementara"
        files_in_directory = os.listdir(lokasifoldernya)
        filtered_files = [file for file in files_in_directory if file.endswith(".docx")]
        for file in filtered_files:
            path_to_file = os.path.join(lokasifoldernya, file)
            os.remove(path_to_file)

        lokasifoldernya = "../sertifmassal/PenyimpananSementara"
        files_in_directory = os.listdir(lokasifoldernya)
        filtered_files = [file for file in files_in_directory if file.endswith(".xlsx")]
        for file in filtered_files:
            path_to_file = os.path.join(lokasifoldernya, file)
            os.remove(path_to_file)

        lokasifoldernya = "../sertifmassal/PenyimpananSementara/TempFiles"
        files_in_directory = os.listdir(lokasifoldernya)
        filtered_files = [file for file in files_in_directory if file.endswith(".docx")]
        for file in filtered_files:
            path_to_file = os.path.join(lokasifoldernya, file)
            os.remove(path_to_file)
        #batas
        
        f = request.files['file']
        #hanya dile docx yang boleh diupload
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in set(['docx'])
        if f.filename != '' and allowed_file(f.filename):

            DocxFileSavePath = os.path.join(
                ROOT_DIR, "PenyimpananSementara", "Generated.docx")
            f.save(DocxFileSavePath)
            # return str(f.filename) + 'file berhasil diunggah!'
            document = PyCertGen.DocxLoader(DocxFileSavePath)
            ParsedResults = PyCertGen.parser(document, v=0)
            CleanParsed = PyCertGen.cleanParsed(ParsedResults)
        else: 
            return render_template('unggah-desain.html')
    return render_template('ubah-variabel.html', UploadFileMessage=str(f.filename) + ' file Berhasil Diunggah', data=CleanParsed)

@app.route('/unggah-data-excel')
def upload_excel_file():
    return render_template('unggah-data.html')


@app.route('/uploadexcelsuccess', methods=['GET', 'POST'])
def uploadexcelsuccess():
    if request.method == 'POST':
        f = request.files['ExcelFile']
        #hanya file xlsx yang boleh diupload
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in set(['xlsx'])
        if f.filename != '' and allowed_file(f.filename):
            ExcelFileSavePath = os.path.join(ROOT_DIR, "PenyimpananSementara", "Data.xlsx")
            f.save(ExcelFileSavePath)
            DocxFileSavePath = os.path.join(
                ROOT_DIR, "PenyimpananSementara", "Generated.docx")
            # return str(f.filename) + 'file berhasil diunggah!'
            SaveFolder = os.path.join(ROOT_DIR, "PenyimpananSementara", "TempFiles")
            # Clean First
            common_utils.DeleteFolderContents(SaveFolder)

            #error jika bukan string
            try:
                PyCertGen.CertGenEngine(
                DocxFileSavePath, ExcelFileSavePath, SaveFolder)
            except:
                return redirect(url_for('foo'))

            SaveFolderPath = os.path.join("PenyimpananSementara", "TempFiles")
            #convert to 
            
            shutil.copy('TEST.ps1', SaveFolderPath)
            
            # SaveZipFilePath = os.path.join(ROOT_DIR, "PenyimpananSementara", "SertifikatMassal.zip")
            SaveZipFilePath = os.path.join("TempZipSaved", "SertifikatMassal.zip")
            common_utils.zipper(SaveFolderPath, SaveZipFilePath)
            # Processing
        else: 
            return render_template('unggah-data.html')
    return render_template('unduh-file-zip.html', value="SertifikatMassal.zip")

@app.route('/foo')
def foo():
    flash = "Semua Data harus bernilai String! Lihat Tutorial!"
    return render_template('unggah-data.html', flash=flash)

@app.route('/download/<filename>')
def return_files_tut(filename):
    if filename == "SertifikatMassal.zip":
        ZipFilePath = os.path.join("TempZipSaved", filename)
        return send_file(ZipFilePath, as_attachment=True, mimetype='application/zip',
                         attachment_filename='HasilSertifikatMassal.zip')
    else:
        return render_template("tutorial.html", flash=flash)


@app.route('/validasi')
def Home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM daftar_sertifikat")
    fetchdata = cur.fetchall()
    cur.close()

    return render_template('apakah-valid.html', data = fetchdata)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search = request.form['search']
        cur = mysql.connection.cursor()
        #cur.execute("select * from daftar_sertifikat where id = %s", [search])
        # hasil = cur.fetchall()
        cur.execute('''SELECT id, nama, lembaga, bukti FROM daftar_sertifikat where id = %s''', [search])
        rv = cur.fetchall()

        if rv == () :
            flash="Sertifikat Tidak Sah / Tidak Ada"
        else:
            flash= "Sertifikat Asli"
        
        return render_template('apakah-valid.html', flash=flash, value=rv)
    
    else:
        return render_template('apakah-valid.html')

@app.route('/lihatdata', methods=['GET', 'POST'])
def lihatdata():
    if request.method == "POST" or "GET":
        cur = mysql.connection.cursor()
        #cur.execute("select * from daftar_sertifikat where id = %s", [search])
        # hasil = cur.fetchall()
        cur.execute('''SELECT no, id, nama, lembaga, bukti, keterangan FROM daftar_sertifikat''')
        rvv = cur.fetchall()

        cur.execute('SELECT COUNT(no) FROM daftar_sertifikat')
        jumlah = cur.fetchone()
        flash= jumlah

        return render_template('lihatdata.html', flash=flash, value=rvv)
    
    else:
        return render_template('lihatdata.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/bisaga', methods=['GET', 'POST'])
def bisaga():
    if request.method == "POST":
        login = request.form['login']

        if login == "admindiah" :
            flash="Berhasil"
            return redirect(url_for('unggahdataexcelvalidasi'))
        else:
            flash= "Tidak Berhasil"
        
        return render_template('login.html', flash=flash)
    
    else:
        return render_template('login.html')


@app.route('/unggahdataexcelvalidasi')
def unggahdataexcelvalidasi():
    return render_template('unggah-data-valid.html')


@app.route('/suksesvalid', methods=['GET', 'POST'])
def uploadefileexcelvalidasi():
    if request.method == 'POST':
        f = request.files['ExcelFile']
        #hanya file xls yang boleh diupload
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in set(['xls'])
        if f.filename != '' and allowed_file(f.filename):
            ExcelFileSavePath = os.path.join(ROOT_DIR, "savezone", "Data.xls")
            f.save(ExcelFileSavePath)
            loc = (ExcelFileSavePath)

            conn = mysql.connection
            cur = conn.cursor()

            l=list()
            a=xlrd.open_workbook(loc)
            sheet=a.sheet_by_index(0)
            sheet.cell_value(0,0)

            if sheet.ncols!=5:
                flash="DATA SALAH !!!"
            else:
                for i in range(1,sheet.nrows):
                    l.append(tuple(sheet.row_values(i)))

                q="insert ignore into daftar_sertifikat(id,nama,lembaga,bukti,keterangan)values(%s,%s,%s,%s,%s)"
                cur.executemany(q,l)
                conn.commit()

                flash="FILE BERHASIL DIUPDATE!"

            return render_template('unggah-data-valid.html', flash=flash)
        else: 
            return render_template('unggah-data-valid.html')

    return render_template('unggah-data-valid.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
