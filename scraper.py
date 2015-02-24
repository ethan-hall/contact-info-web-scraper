import cookielib
import mechanize
import csv

__author__ = 'Ethan Hall'

username = []  # will store usernames for unique urls
searchStr = 'href="/users/'  # keyword to find usernames
numPages = 8  # number of username pages

# log in and browser setup
cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)  # no robot here
br.set_cookiejar(cj)  # stores cookies for mechanize21
br.open('http://montana.thelaunchpad.org/user/login')
br.select_form(nr=0)  # select login form
br.form['name'] = 'username'  # username for login
br.form['pass'] = 'password'  # super secret password
br.submit()  # Now logged in! (no error checking)

for i in range(0, numPages):
    url = 'http://montana.thelaunchpad.org/admin/people'  # url for username pages
    if i == 0:
        br.open(url)
    else:
        br.open(url+'?page='+str(i))
    page = str(br.response().read())

    x = 0
    userStart = []  # index of usernames
    while page.find(searchStr, x) != -1:    # find usernames on page
        index = page.find(searchStr, x)
        userStart.append(index)
        x = index + 24  # +24 to skip over current username

    for i in range(0, len(userStart)):
        userTemp = ""  # used to store partial username before storing in username list
        j = userStart[i] + 13   # +13 to skip to start of username
        while page[j] != '"':   # grab username
            userTemp += page[j]
            j += 1
        username.append(userTemp)   # store username in list

print username  # for debug

# 2d list for username,full name,email,phone,ventures
contactList = [[0 for i in range(5)] for j in range(len(username))]

for i in range(0, len(username)):   # grab contact info from every username
    print i  # status print

    contactList[i][0] = username[i]  # append usernames

    url2 = 'http://montana.thelaunchpad.org/users/'  # open unique username URL
    br.open(url2+username[i])
    page = str(br.response().read())

    # find and store full name
    nameTemp = ''
    nameSearchStr = 'class="profile_meta">'
    nameIndex = page.find(nameSearchStr) + 30
    if nameIndex != (-1+24):  # error checking
        while page[nameIndex] != '<':
            nameTemp += page[nameIndex]
            nameIndex += 1
        contactList[i][1] = nameTemp
    else:
        print "No name found for user " + username[i] + "."

    # find and store email
    emailTemp = ''
    emailSearchStr = '<a href="mailto:'
    emailIndex = page.find(emailSearchStr) + 16
    if emailIndex != (-1+16):  # error checking
        while page[emailIndex] != '"':
            emailTemp += page[emailIndex]
            emailIndex += 1
        contactList[i][2] = emailTemp
    else:
        print "No email found for user " + username[i] + "."

    # find and store phone
    phoneTemp = ''
    phoneSearchStr = '<h2>Phone Number</h2><p>'
    phoneIndex = page.find(phoneSearchStr) + 24
    if phoneIndex != (-1+24):  # error checking
        while page[phoneIndex] != '<':
            phoneTemp += page[phoneIndex]
            phoneIndex += 1
        contactList[i][3] = phoneTemp
    else:
        print "No phone found for user " + username[i] + "."

    # find and store venture
    ventureTemp = ''
    ventureSearchStr = '/venture/'
    if page.find(ventureSearchStr) != -1:  # in case user has no venture
        ventureIndex = ventureIndex1 = page.find(ventureSearchStr) + 9
        while page[ventureIndex] != '>':
            ventureIndex += 1
        ventureIndex += 1
        while page[ventureIndex] != '<':
            ventureTemp += page[ventureIndex]
            ventureIndex += 1
    contactList[i][4] = ventureTemp

#  save as CSV
fl = open('ContactList.csv', 'w')
wr = csv.writer(fl)
wr.writerows(contactList)
print "ContactList.csv saved."