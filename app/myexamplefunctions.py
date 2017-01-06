#EXAMPLE OF XML TO JSON
'''
req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/AI1147')

xml = BeautifulSoup(req)

varcode = xml.course['code']
vartitle = xml.title.string
varmail = xml.examiner['primaryemail']

tempdict = {'code':varcode, 'title':vartitle, 'examiner':varmail}

return json.dumps(tempdict)

return jsonify(code=varcode, title=vartitle, examiner=varmail)
'''


#FETCHING LIST OF CODES FOR AIB COURSES
'''
j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/AIB.json')

j_obj = json.load(j)

templist =[]

for item in j_obj['courses']:
    #print item['code']
    templist.append(item['code'])

print templist

return json.dumps(j_obj)
'''



#JSONIFY COURSES FROM DEPARTMENT
'''
j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/AIB.json')

j_obj = json.load(j)

templist = []

for item in j_obj['courses']:
    #print item['code']
    templist.append(item['code'])

templist2 = []
tempdict = {}

for item in templist:
    req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s' % (item))

    xml = BeautifulSoup(req)


    #vartitle = xml.title.string
    try:
        varcode = xml.course['code']
        print varcode

    except Exception, e:
        varcode = "no title"
        print varcode


    try:
        varmail = xml.examiner['primaryemail']
        print varmail

    except Exception, e:
        varmail = "no mail"
        print varmail


    try:
        vartitle = xml.title.string
        #print vartitle.encode('utf-8')
        print vartitle

    except Exception, e:
        vartitle = "no title"
        print vartitle

    tempdict = {'code':varcode, 'title':vartitle, 'examiner':varmail}

    templist2.append(tempdict)

return jsonify(courses=templist2)

'''
