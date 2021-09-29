import flask
import sqlite3
from flask import request, url_for,flash,redirect
from flask.templating import render_template
from werkzeug.exceptions import abort
import conversion
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq
import selenium
import selenium.webdriver
import time

def database_connection(): #Used to open a connection to data base
    conn=sqlite3.connect('database.sqlite')
    conn.row_factory=sqlite3.Row #Helps to have name based access to columns
    return conn

def get_post(post_id):
    conn = database_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = flask.Flask(__name__)
app.config['SECRET_KEY']='1234567890'

@app.route('/')
def index():
    
    
  
    return render_template('index.html')

@app.route('/application/')
def application():

    return render_template('application.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    x=float(flask.request.form['weight'])
    y=float(flask.request.form['height'])
    z= conversion.bodymass(x,y)
    return render_template('calculate1.html',z=z,x=x,y=y)

@app.route('/calculate/2', methods=['POST'])
def calculate1():
    unit= flask.request.form['unit']
    value=float(flask.request.form['value'])
    mass=conversion.weigh(unit,value)
    return render_template('calculate2.html',mass=mass,unit=unit,value=value)

@app.route('/calculate/3', methods=['POST'])
def calculate2():
    t= flask.request.form['t']
    celisius=float(flask.request.form['celisius'])
    temp=conversion.fahrenheit(t,celisius)
    return render_template('calculate3.html',temp=temp,t=t,celisius=celisius)

@app.route('/shop/')
def shop():
    return render_template('shop.html')

@app.route('/shopping1',methods=['POST','GET'])
def shopping1():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    register = flask.request.form['registerer']
    serial = flask.request.form['itemNumber']
    stuff = flask.request.form['item']
    number = flask.request.form['quantity']
    unit = flask.request.form['punit']
    total = flask.request.form['ptotal']
    cursor.execute("INSERT INTO finance (registerer, itemNumber, item,quantity,unitPrice,totalPrice) VALUES (?, ?,?,?,?,?)",
                    [register, serial,stuff, number,unit,total])
    
   
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('shopping1.html',register=register,serial=serial,stuff=stuff,number=number,total=total)
    
@app.route('/scraping/') # Web scraping section
def scraping():
    url='https://www.imdb.com/chart/boxoffice/' #connects to the imdb server 

    driver = selenium.webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    source = driver.page_source
    soup = BeautifulSoup(source)
    subheadings = soup.find_all('h1') # h1 carries the tile of chart, like US top 10 list
    heading=[]
    time.sleep(1)
    for subhead in subheadings:
        t=str(subhead.get_text())
        heading.append(t)
    time.sleep(1)
    source = driver.page_source
    soup = BeautifulSoup(source)
    subheadings5 = soup.find_all('h4')
    time_of_play=[] # How long the movie was on
    time.sleep(1)
    for subhead5 in subheadings5:
        time_of_play=str(subhead5.get_text())
        heading.append(time_of_play)
    time.sleep(1)
    source = driver.page_source
    soup = BeautifulSoup(source)
    subheadings1 = soup.find_all('th')
    title=[] 
    time.sleep(1)
    for subhead1 in subheadings1:
        s=str(subhead1.get_text())
        title.append(s)
    source = driver.page_source
    soup = BeautifulSoup(source)
    subheadings2 = soup.find_all('td',class_='titleColumn')
    movie=[] # Name of top 10 movies
    time.sleep(1)
    for subhead2 in subheadings2:
        m=str(subhead2.get_text())
        movie.append(m)
   
    source = driver.page_source
    soup = BeautifulSoup(source)
    subheadings3 = soup.find_all('td',class_='ratingColumn')
    weekend=[] #How much the movie sold over the weekend
    time.sleep(1)
    for subhead3 in subheadings3:
        w=str(subhead3.get_text())
        weekend.append(w)
    source = driver.page_source
    soup = BeautifulSoup(source)
    subheadings4 = soup.find_all('span',class_='secondaryInfo')
    gross=[]
    time.sleep(1)
    for subhead4 in subheadings4:
        g=str(subhead4.get_text())
        gross.append(g)

    return render_template('scraping.html', title=title, movie=movie, weekend=weekend,gross=gross) 

@app.route('/blog') # Connects to the data base and pulls up all the blog content.
def blog():
    conn= database_connection()
    posts=conn.execute('SELECT*FROM posts').fetchall()
    conn.close()
    return render_template('blog.html',posts=posts)

@app.route('/<int:post_id>') # Since we might encounter several posts, hence using integer number to seperate different posts in the same route is essensial
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET','POST']) # To connect into data  base and get post title and contect from the user and creating the post
def create():
    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']
        if not title:
            flash('Title is required!')
        else:
            conn = database_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html') 

@app.route('/<int:id>/edit', methods=('GET', 'POST')) # Is used to find a post by its ID, connects to data base and if a new post is added updates post ID there
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = database_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id): # Is used to delete a post from database. Finds the post by its ID and after receiving confirmation deletes that
    post = get_post(id)
    conn = database_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.errorhandler(404) #Redirects to this page if the route can't be found
def page_not_found(e):
	return render_template("Error404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
