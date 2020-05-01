from flask import Flask, render_template, request, redirect
import pandas as pd


app = Flask(__name__)


# Global variables
uusn = ''
ll = []


@app.route('/login', methods=['GET','POST'])
def homepage_form():
    if request.method == 'POST' :
        user = request.form['username']
        pwd = request.form['password']

        x1 = user + pwd
        y1 = hash_fn(x1) # Converts username and password into a hash number

        file = open('hash_register.txt','r')
        for line in file:       # To check if  the user has registered and then only login in
            word = line.split('|')
            if y1 == word[0]:      # Check if the hash value is same as that of stored hash value
                return redirect('/homepage')

    return render_template("login.html")      # This is to load login page


@app.route('/register', methods=['GET','POST'])
def register_form():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        if password == password1 :      # To check if the password and confirm password is same
            file = open('hash_register.txt','a')        # To create hash file
            x = username + password
            y = hash_fn(x)      # To convert the username and password into hash value
            file.write(y+"|"+username+"|"+password+"\n")
            file.close()
            return redirect('/login')       # To go to login page
        return '<h2><center> Wrong confirmation password <br> Please go back and enter the correct password </center></h2>'

    return render_template("register.html")         # To load register page


@app.route('/detailspage', methods=['GET','POST'])
def detailspage_form():
    global uusn
    if request.method == 'POST' :
        name = request.form['name']
        fname = request.form['fname']
        usn = request.form['usn']
        no = request.form['no']
        mail = request.form['mail']
        uusn=usn
        file = open('details.txt','a')      # To store the details of the student in details file
        file.write(name+"|"+fname+"|"+usn+"|"+no+"|"+mail+"\n")
        file.close()
        return redirect('/markspage')       # To go to markspage page

    return render_template("detailspage.html")          # To go to detailspage page


@app.route('/markspage', methods=['GET','POST'])
def markspage_form():
    global uusn
    if request.method == 'POST' :
        m10 = request.form['m10']
        m12 = request.form['m12' ]
        meng = request.form['meng']
        mb = request.form['mb']
        file = open('marks.txt', 'a')       # To store marks in marks file
        file.write(uusn +"|"+ m10 + "|" + m12 + "|" + meng + "|" + mb + "\n")
        file.close()
        return redirect('/homepage')        # To go to homepage back

    return render_template("markspage.html")           # To load markspage page


@app.route('/homepage')
def homepage():
    return render_template("homepage.html")         # To load homepage page


"""@app.route('/displaypage', methods=['GET','POST'])
def displaypage():
    if request.method == 'post':
        usn = request.form['usn']
    
        file = open('details.txt','r')
        for line in file :
            word = line.split('|')
            if word[2] == usn :
                name = word[0]
                fname = word[1]
                num = word[3]
                mail = word[4]
        file.close()
        file1 = open('marks.txt','r')
        for line1 in file1 :
            word1 = line1.split('|')
            if word1[0] == usn :
                m10 = word1[1]
                m12 = word1[2]
                meng = word1[3]
                back = word1[4]
        file1.close()
        
        return render_template('disp.html') #,name=name,fname=fname,u=usn,num=num,mail=mail,m10=m10,m12=m12,meng=meng,back=back)

    return render_template("displaypage.html")"""


@app.route('/display', methods=['GET','POST'])
def display_form():
    global ll
    flag = 0
    if request.method == 'POST' :
        usn = request.form['usn']
        f1 = open('marks.txt','r')
        f3 = open('companymarks.txt','r')
        for line in f1:                 # This is to check if the given usn is there in the file
            word = line.split('|')
            if word[0] == usn :
                flag = 1;
                l = list(word)
                break

        if flag == 0:
            return '<h2> Wrong USN </h2>'
        l2 = list()
        str1 = ''

        for line in f3 :         # This is to compare the scores of the student with the comapany's requirement
            word = line.split('|')
            if l[1] >= word[2]:
                if l[2] >= word[3]:
                    if l[3] >= word[4]:
                        if l[4] <= word[5]:
                            flag = 1
                            l2.append(word[1])
                            str1 = '|'.join(l2)

        ll = l2[:]
        f1.close()
        f3.close()

#########################################################
        # This to create placement data file and index file
        f = 1
        file = open('placement.txt','r+')
        for line in file:
            word = line.split('|')
            if word[0] == usn :
                f = 0
        file.close()

        if f == 1 :
            file = open('placement.txt','a')
            start = file.tell()
            file.write(usn+'|'+str1+'\n')
            stop = file.tell()
            len = stop - start

            # To create add records in index file
            file1 = open('index.txt','a')
            start = start.__str__()
            len = len.__str__()
            sstr = start+'|'+len+'|'+usn+'\n'       # Store data in index file
            file1.write(sstr)
            file1.close()
        file.close()

#######################################################

        # To display data from index file
        ff3 = open('placement.txt','r+')
        ff2 = open('index.txt','r+')

        uu = "|"+usn
        for lines in ff2:
            if uu in lines:
                line = lines.rstrip()
                line = line.split('|')
                start = int(line[0])
                byte = int(line[1])
                ff3.seek(start)      # To take starting value from index file and check it in placement file
                details = ff3.read(byte-1)      # To read the entire record from the starting value

                detail = details.rstrip()
                detail = detail.split('|')
                name = detail[0]
                d = detail[1:]
                str = ', '.join(d)# Convert the list into string and display it


        dict = {}
        df1 = pd.DataFrame({"Company_Name":[],"Job_Profile":[],"Salary":[],"Location":[]})
        text = " "
        ff4 = open('companydetails.txt','r')
        for line in ff4:
            for i in d:
                w = line.split('|')
                if w[1] in i:
                    dict = {"Company_Name":[w[1]],"Job_Profile":[w[2]],"Salary":[w[3]],"Location":[w[4]]}
                    df2 = pd.DataFrame(dict)
                    df1 = df1.append(df2)



        ff2.close()
        ff3.close()
        if str == '':
            return '<h2> Sorry, Not eligible for any companies </h2>'
        return render_template('show.html', text1=usn, text2=df1.to_html())

    return render_template("display.html")      # To load display page


########################################################

def hash_fn(x):  #Hash function
    s=""
    for i in x:
        s = s + str(ord(i))     # To take each character and convert into its ascii value
    return s


if __name__ ==  "__main__":
    app.run(debug=True)





# Reserve functions
""" FOR SORTING FUNCTION
    f1 = open('index.txt').readlines()
    for i in sorted(f1,key=lambda i:i.split('|')[2]):
        f1.write(i)
    f1.close() """

""" TO CHECK IF REGISTER USER IS IN LOGIN PAGE
    str1 = str(user)+'|'+str(pwd)
        fhand = open('register.txt','r')
        for line in fhand :         # To check if login password is right
            if str1 in line :
                return redirect('/homepage')        # To go to homepage """

""" TO STORE LOGIN AND USERNAME IN REGSITER FILE
     file = open('register.txt','a')
            file.write(username+"|"+password+"\n")      # To store username and password in register file
            file.close() """