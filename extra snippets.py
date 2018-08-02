
@app.route("/users")
def userlist():
    userlist = User.select(User.username,User.sponsor,User.activated)
    test = User.get(User.username == 'aaron')
    #print test.username
    new_password = '24243'
    testpw = bcrypt.hashpw(new_password.encode('utf-8'),test.password.encode('utf-8'))
    if testpw == test.password:
        print "same pass"
    else:
        print "different pass"
    return render_template('default2.html',username=userlist)
    db.close()    
