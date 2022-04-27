from crypt import methods
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# mySQL connection
app.config['MYSQL_HOST'] = '192.168.64.2'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] ='flask'

mysql = MySQL(app)

# settings
app.secret_key= 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    #print(data)
    return render_template("index.html", contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname,phone) VALUES (%s,%s)",(fullname,phone))
        mysql.connection.commit()
        flash('Contact added')
        return redirect(url_for("index"))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id= {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed')
    return redirect(url_for("index"))

@app.route('/edit//<string:id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id= {0}'.format(id))
    data = cur.fetchall()
    #print(data[0])
    return render_template("edit_contact.html", contact = data[0])

@app.route('/update//<string:id>', methods = ['POST'])
def update_contact(id):

    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']

    cur = mysql.connection.cursor()
    cur.execute("""
    UPDATE contacts 
    SET fullname = %s,
        phone = %s
    WHERE id= %s    
    """,(fullname,phone,id))
    mysql.connection.commit()
    flash ('bbien')
    return redirect(url_for("index"))

if __name__ == '__main__':
    #app.run(host='localhost',port=3000, debug= True)#
    app.run(host="0.0.0.0" port=3000)
