from flask import Flask, render_template, request, redirect, flash
import random, os
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI']=os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if app.config['MONGO_URI']==None:
    file=open('mongostring.txt', 'r')
    connection_string=file.read()
    app.config['MONGO_URI']=connection_string.strip()
    file.close()
    file = open('secret_key.txt', 'r')
    secret_key = file.read()
    app.config['SECRET_KEY'] = secret_key.strip()
    file.close()




mongo=PyMongo(app)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/jumble', methods=['GET', 'POST'])
def jumble():
    if request.method == 'GET':
        return render_template('jumbled.html')
    else:
        input_for_jumbled_word1 = request.form['input_for_jumbled_word1'].strip()
        input_for_jumbled_word2 = request.form['input_for_jumbled_word2'].strip()
        input_for_jumbled_word3 = request.form['input_for_jumbled_word3'].strip()
        input_for_jumbled_word4 = request.form['input_for_jumbled_word4'].strip()
        input_for_jumbled_word5 = request.form['input_for_jumbled_word5'].strip()
        wordlist1 = list(input_for_jumbled_word1)
        wordlist2 = list(input_for_jumbled_word2)
        wordlist3 = list(input_for_jumbled_word3)
        wordlist4 = list(input_for_jumbled_word4)
        wordlist5 = list(input_for_jumbled_word5)
        random.shuffle(wordlist1)
        random.shuffle(wordlist2)
        random.shuffle(wordlist3)
        random.shuffle(wordlist4)
        random.shuffle(wordlist5)
        x = ''
        for loop in wordlist1:
            x = x + loop
        print(x)
        words1={'original_word':input_for_jumbled_word1,'jumbled word':x}
        mongo.db.jumbled_words.insert_one(words1)

        x = ''
        for loop in wordlist2:
            x = x + loop
        print(x)
        words2 = {'original_word': input_for_jumbled_word2, 'jumbled word': x}
        mongo.db.jumbled_words.insert_one(words2)

        x = ''
        for loop in wordlist3:
            x = x + loop
        print(x)
        words3 = {'original_word': input_for_jumbled_word2, 'jumbled word': x}
        mongo.db.jumbled_words.insert_one(words3)

        x = ''
        for loop in wordlist4:
            x = x + loop
        print(x)
        words4 = {'original_word': input_for_jumbled_word4, 'jumbled word': x}
        mongo.db.jumbled_words.insert_one(words4)

        x = ''
        for loop in wordlist5:
            x = x + loop
        print(x)
        words5 = {'original_word': input_for_jumbled_word5, 'jumbled word': x}
        mongo.db.jumbled_words.insert_one(words5)
        flash('Your words have been successfully added', "success")
        return redirect('/jumble')

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'GET':
        jumbledwords = mongo.db.jumbled_words.aggregate([{"$sample": {"size": 5}}])
        jumbled_words = []
        original_words = []
        for loop in jumbledwords:
            jumbled_words.append(loop['jumbled word'])
            original_words.append(loop['original_word'])
        return render_template('solve.html', jumbled_words=jumbled_words, original_words=original_words)
    else:
        userenteredwords=request.form.getlist('guess')
        original_words=request.form['original_words']
        original_words=original_words.replace('[', '')
        original_words=original_words.replace(']', '')
        original_words=original_words.replace(' ', '')
        original_words=original_words.replace("'", "")
        original_words=original_words.split(',')
        print(original_words)
        print(userenteredwords)
        correct=0
        for loop in range (0,5,1):
            x=original_words[loop]
            y=userenteredwords[loop]
            if x==y:
                correct=correct+1
        correct=str(correct)
        return('Your score was a '+correct+'/5')




if __name__ == '__main__':
    app.run()