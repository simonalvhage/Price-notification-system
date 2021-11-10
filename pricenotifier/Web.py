from flask import Flask, request, render_template
import main, inserthandler

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1



@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/delete.html')
def my_form2():
    return render_template('delete.html')

@app.route('/supported.html')
def my_form3():
    return render_template('supported.html')



@app.route('/', methods=['POST'])
def my_form_post():
    if request.form.get("submit"):
        #run multiple
        mail = request.form['mail']
        link = request.form['link']
        change = request.form['change']
        password,x = main.createpassword(mail)
        inserthandler.scheduler(mail,link,change, password)
        if x == 1:
            return render_template("index.html", user_start=password)
        else:
            return render_template("index.html", user_start="")

@app.route('/delete.html', methods=['POST'])
def my_form2_post():
    if request.form.get("submit2"):
        #run multiple
        mail = request.form['mail2']
        code = request.form['code']
        x = main.deleterecords(mail,code)
        if x > 0:
            return render_template("delete.html", user_start="OK! The watchlist is now removed")
        else:
            return render_template("delete.html", user_start="Could not remove watchlist")


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

app.run(host='192.168.1.67',port='8000', debug="true")
