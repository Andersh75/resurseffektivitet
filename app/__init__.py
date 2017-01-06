from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from flask import jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from xml.etree import ElementTree as ET
from socket import *
from functools import wraps
from decimal import Decimal
from bs4 import BeautifulSoup
import gc
import urllib
import urllib2
from urllib2 import urlopen
import xmltodict
import json
from flask import json
from myfunctions import jsonifycoursesfromdepartment, fetchinglistofcodesfordepartmentcourses, staffperdepartment, courseinfoperyearandround, new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/f1'
db = SQLAlchemy(app)





@app.route('/')
def hello_world2():
    '''
    tempdict = {}
    tempdict2 = {}
    tempdict3 = {}

    templist = []
    templist2 = []

    departments = ["AIB", "AIC", "AID", "AIE"]

    for item in departments:
        tempdict = fetchinglistofcodesfordepartmentcourses(item)
        templist.append(jsonifycoursesfromdepartment(tempdict))

        tempdict2 = staffperdepartment(item)
        templist2.append(tempdict2)

    tempdict3 = courseinfoperyearandround(2016, 1)


    testv = jsonify(tempdict3)
    '''
    data = [ {
    "department": "ABE/Bygg- och fastighetsekonomi",
    "courses": [
            {
            "code": "AI2140",
            "title": "Advanced Issues in Real Estate and Financial Services",
            "href": "http://www.kth.se/student/kurser/kurs/AI2140",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2125",
            "title": "Advanced Issues in Real Estate Economics",
            "href": "http://www.kth.se/student/kurser/kurs/AI2125",
            "info": "<p>Hedonic prices; Real estate price indices; Efficient market theory; Vacancies; Urban growth; Market Segmentation; Real Estate Performance; Valuation of Lease contracts; Real estate security market; Mortgage markets.<\/p>",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI225U",
            "title": "Analys av fastighetsportfÃ¶ljer /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI225U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI239U",
            "title": "Analys och vÃ¤rdering av fastighetsbestÃ¥nd /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI239U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2154",
            "title": "Avancerad fastighetsvÃ¤rdering och analys",
            "href": "http://www.kth.se/student/kurser/kurs/AI2154",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1135",
            "title": "BeskattningsrÃ¤tt",
            "href": "http://www.kth.se/student/kurser/kurs/AI1135",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI143V",
            "title": "BeskattningsrÃ¤tt",
            "href": "http://www.kth.se/student/kurser/kurs/AI143V",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI3004",
            "title": "Bli publicerad i fÃ¶retagsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI3004",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI3001",
            "title": "Bostadsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI3001",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI202V",
            "title": "Business Cycles in Construction and Real Estate Market",
            "href": "http://www.kth.se/student/kurser/kurs/AI202V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI236U",
            "title": "Byggnads- och installationsteknik /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI236U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI109V",
            "title": "Bygg- och fastighetsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI109V",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2116",
            "title": "Contract Theory",
            "href": "http://www.kth.se/student/kurser/kurs/AI2116",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1N5309",
            "title": "Det finansiella systemet i teori och praktik",
            "href": "http://www.kth.se/student/kurser/kurs/1N5309",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI2112",
            "title": "Economics",
            "href": "http://www.kth.se/student/kurser/kurs/AI2112",
            "info": "",
            "credits": "4,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2131",
            "title": "Economics and Quantitative Methods",
            "href": "http://www.kth.se/student/kurser/kurs/AI2131",
            "info": "",
            "credits": "5,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI104V",
            "title": "Ekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI104V",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1103",
            "title": "Ekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI1103",
            "info": "<p>En grundl&#228;ggande kurs i nationalekonomi, investeringsanalys och aff&#228;rsredovisning.<\/p>",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI3007",
            "title": "Ekonomiska cykler pÃ¥ fastighets- och finansmarknader",
            "href": "http://www.kth.se/student/kurser/kurs/AI3007",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI1131",
            "title": "Ekonomisk analys",
            "href": "http://www.kth.se/student/kurser/kurs/AI1131",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1145",
            "title": "Ekonomisk fastighetsfÃ¶rvaltning",
            "href": "http://www.kth.se/student/kurser/kurs/AI1145",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI221V",
            "title": "EntreprenÃ¶rskap och management",
            "href": "http://www.kth.se/student/kurser/kurs/AI221V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI214V",
            "title": "EntreprenÃ¶rsskap",
            "href": "http://www.kth.se/student/kurser/kurs/AI214V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI201X",
            "title": "Examensarbete inom bygg- och fastighetsekonomi, avancerad nivÃ¥",
            "href": "http://www.kth.se/student/kurser/kurs/AI201X",
            "info": "",
            "credits": "30,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI206X",
            "title": "Examensarbete inom Bygg- och Fastighetsekonomi, avancerad nivÃ¥",
            "href": "http://www.kth.se/student/kurser/kurs/AI206X",
            "info": "<p>Examensarbetet ska utg&#246;ra en f&#246;rdjupning inom &#160;huvudomr&#229;det p&#229; avancerad niv&#229;. Kursen utformas som ett begr&#228;nsat&#160;forskningsprojekt inom omr&#229;det bygg- och fastighetsekonomi.<\/p><p>Kursstrukturen innefattar bl.a. f&#246;ljande moment: Litteraturstudier, problemformulering, insamling och sammanst&#228;llning av data, analys, rapportskrivning samt muntlig presentation och opposition.<\/p>",
            "credits": "30,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI277U",
            "title": "Examensarbete inom fastigheter/uppragsutibldnig/",
            "href": "http://www.kth.se/student/kurser/kurs/AI277U",
            "info": "",
            "credits": "15,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI102X",
            "title": "Examensarbete inom fastighetsekonomi, grundnivÃ¥",
            "href": "http://www.kth.se/student/kurser/kurs/AI102X",
            "info": "",
            "credits": "15,0",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI107X",
            "title": "Examensarbete inom fastighetsekonomi, grundnivÃ¥",
            "href": "http://www.kth.se/student/kurser/kurs/AI107X",
            "info": "",
            "credits": "15,0",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI204X",
            "title": "Examensarbete inom fastighetsfÃ¶retagande, avancerad nivÃ¥",
            "href": "http://www.kth.se/student/kurser/kurs/AI204X",
            "info": "",
            "credits": "30,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI276U",
            "title": "Examensarbete inom fastighetsfÃ¶retagande/uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI276U",
            "info": "",
            "credits": "15,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI101X",
            "title": "Examensarbete inom samhÃ¤llsbyggnad, grundnivÃ¥",
            "href": "http://www.kth.se/student/kurser/kurs/AI101X",
            "info": "",
            "credits": "15,0",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2117",
            "title": "Facility Management",
            "href": "http://www.kth.se/student/kurser/kurs/AI2117",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI233U",
            "title": "Facility Management /Commissioned Course/",
            "href": "http://www.kth.se/student/kurser/kurs/AI233U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI3006",
            "title": "Fastigheter och byggande",
            "href": "http://www.kth.se/student/kurser/kurs/AI3006",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI1132",
            "title": "Fastighetsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI1132",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI270U",
            "title": "Fastighetsekonomins grunder /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI270U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI251U",
            "title": "Fastighetsekonomi /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI251U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1144",
            "title": "Fastighetsfinansiering och investering",
            "href": "http://www.kth.se/student/kurser/kurs/AI1144",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI274U",
            "title": "Fastighetsfinansiering och investering",
            "href": "http://www.kth.se/student/kurser/kurs/AI274U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI228U",
            "title": "FastighetsfÃ¶retagande i offentlig sektor /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI228U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI118U",
            "title": "FastighetsfÃ¶retagande i privat sektor",
            "href": "http://www.kth.se/student/kurser/kurs/AI118U",
            "info": "<p>Syftet med kursen &#228;r att deltagarna ska f&#229; b&#228;ttre kunskap att kunna fatta b&#229;de l&#229;ngsiktiga och kortsiktiga beslut kring underh&#229;ll, investering och f&#246;rvaltning.<\/p><p>S&#228;rskilt fokus ligger p&#229; fastighetsekonomiska bed&#246;mningar som investeringsbed&#246;mningar, nyckeltalsber&#228;kningar, marknadsanalyser och det juridiska regelverket.<\/p>",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI119U",
            "title": "FastighetsfÃ¶retagande i privat sektor, steg 2",
            "href": "http://www.kth.se/student/kurser/kurs/AI119U",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI120U",
            "title": "FastighetsfÃ¶retagets ekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI120U",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI230U",
            "title": "FastighetsfÃ¶retagets ekonomi: BostÃ¤der och kommersiella lokaler /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI230U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI227U",
            "title": "FastighetsfÃ¶retagets ekonomi /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI227U",
            "info": "",
            "credits": "15,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI222U",
            "title": "FastighetsfÃ¶retagets kontrakt /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI222U",
            "info": "",
            "credits": "4,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI240U",
            "title": "FastighetsfÃ¶retagets kontrakt /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI240U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1N5304",
            "title": "FastighetsfÃ¶rmedling",
            "href": "http://www.kth.se/student/kurser/kurs/1N5304",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI219V",
            "title": "FastighetsfÃ¶rmedling",
            "href": "http://www.kth.se/student/kurser/kurs/AI219V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI220V",
            "title": "FastighetsfÃ¶rmedling II",
            "href": "http://www.kth.se/student/kurser/kurs/AI220V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI237U",
            "title": "FastighetsfÃ¶rmedling II /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI237U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI226U",
            "title": "FastighetsfÃ¶rmedling /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI226U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1146",
            "title": "FastighetsfÃ¶rvaltning",
            "href": "http://www.kth.se/student/kurser/kurs/AI1146",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI206V",
            "title": "FastighetsfÃ¶rvaltning",
            "href": "http://www.kth.se/student/kurser/kurs/AI206V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1143",
            "title": "FastighetsfÃ¶rvaltning I",
            "href": "http://www.kth.se/student/kurser/kurs/AI1143",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI258U",
            "title": "Fastighetsinvesteringar",
            "href": "http://www.kth.se/student/kurser/kurs/AI258U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI224U",
            "title": "Fastighetsstrategier i offentlig sektor-forts /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI224U",
            "info": "",
            "credits": "4,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI223U",
            "title": "Fastighetsstrategier i offentlig sektor /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI223U",
            "info": "",
            "credits": "3,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1F5308",
            "title": "FastighetsvÃ¤rdering",
            "href": "http://www.kth.se/student/kurser/kurs/1F5308",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI105V",
            "title": "FastighetsvÃ¤rdering",
            "href": "http://www.kth.se/student/kurser/kurs/AI105V",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1147",
            "title": "FastighetsvÃ¤rdering",
            "href": "http://www.kth.se/student/kurser/kurs/AI1147",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2104",
            "title": "FastighetsvÃ¤rdering",
            "href": "http://www.kth.se/student/kurser/kurs/AI2104",
            "info": "<p>En till&#228;mpad kurs i v&#228;rdering av fr&#228;mst avkastningsfastigheter s&#229;som flerbostads- och kommersiella hyresfastigheter samt fastigheter i f&#246;retag.<\/p>",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1148",
            "title": "FastighetsvÃ¤rdering fÃ¶r samhÃ¤llsbyggnad",
            "href": "http://www.kth.se/student/kurser/kurs/AI1148",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI231U",
            "title": "FastighetsvÃ¤rdering fÃ¶r stadshypotek /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI231U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI273U",
            "title": "FastighetsvÃ¤rdering och analys",
            "href": "http://www.kth.se/student/kurser/kurs/AI273U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI234U",
            "title": "FastighetsvÃ¤rdering och analys /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI234U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI229U",
            "title": "Fastigh.fÃ¶retagets ekonomi o fastigh.vÃ¤rdering /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI229U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI215V",
            "title": "Financial Economics",
            "href": "http://www.kth.se/student/kurser/kurs/AI215V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1133",
            "title": "Finansiella system och riskkapital",
            "href": "http://www.kth.se/student/kurser/kurs/AI1133",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2135",
            "title": "Finansiell Ekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI2135",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2153",
            "title": "Finansiell ekonomi med fastighetstillÃ¤mpningar",
            "href": "http://www.kth.se/student/kurser/kurs/AI2153",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1142",
            "title": "Finansiell rapportering och analys",
            "href": "http://www.kth.se/student/kurser/kurs/AI1142",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2144",
            "title": "FÃ¶retagsfinansiering",
            "href": "http://www.kth.se/student/kurser/kurs/AI2144",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI203V",
            "title": "Industriell utveckling med entreprenÃ¶rskap",
            "href": "http://www.kth.se/student/kurser/kurs/AI203V",
            "info": "",
            "credits": "15,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI246U",
            "title": "Introductory Course - Real Estate Principles /Commissioned Course/",
            "href": "http://www.kth.se/student/kurser/kurs/AI246U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1120",
            "title": "Introductory Economics and Quantitative Methods",
            "href": "http://www.kth.se/student/kurser/kurs/AI1120",
            "info": "<ol><li>Financial Mathematics<\/li><\/ol><ul><li>Exponents, exponential functions, and logarithms<\/li><li>Linear and quadratic equations<\/li><li>Arithmetic and geometric progressions<\/li><\/ul><p>&#160;&#160;&#160;&#160;&#160;&#160; B. Introduction to Excel&#160;&#160;&#160;&#160;&#160;&#160; C. Statistics <\/p><ul><li>Descriptive statistics &#8211; frequency distribution, measures of central tendency and dispersion<\/li><li>Probability concepts <ul><li>Probability distributions, expected value, variance, and covariance<\/li><li>The normal distribution<\/li><li>Confidence intervals and hypothesis testing<\/li><\/ul><\/li><li>Regression analysis <ul><li>Statistical inference using regression analysis<\/li><li>Forecasting<\/li><\/ul><\/li><\/ul><p>&#160;&#160;&#160;&#160;&#160;&#160;&#160; D. Economics <\/p><ul><li>Demand, Supply, Equilibrium prices and Elasticity<\/li><li>Short-run and long run production theory<\/li><li>Short and long-run costs<\/li><\/ul><p>Perfect Competition &amp; Monopoly<\/p>",
            "credits": "1,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI245U",
            "title": "Introductory Economics and Quantitative Methods /Commissioned Course/",
            "href": "http://www.kth.se/student/kurser/kurs/AI245U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1108",
            "title": "Investeringsanalys",
            "href": "http://www.kth.se/student/kurser/kurs/AI1108",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI272U",
            "title": "Investeringsanalys fÃ¶r fastighetstillÃ¤mpningar",
            "href": "http://www.kth.se/student/kurser/kurs/AI272U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI103V",
            "title": "Investment Analysis",
            "href": "http://www.kth.se/student/kurser/kurs/AI103V",
            "info": "<p>Recruitment text: To provide students with basic theoretical and practical knowledge of investment decision making, and to prepare students for further studies in real estate finance and economics.<\/p>",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1134",
            "title": "Kapitalmarknader och finansiella instrument",
            "href": "http://www.kth.se/student/kurser/kurs/AI1134",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2106",
            "title": "Konjunkturcykler pÃ¥ bygg- och fastighetsmarknaden",
            "href": "http://www.kth.se/student/kurser/kurs/AI2106",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2156",
            "title": "Kontraktsteori med tillÃ¤mpningar pÃ¥ fastighetsfÃ¶rvaltning",
            "href": "http://www.kth.se/student/kurser/kurs/AI2156",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI235U",
            "title": "Kontraktsutformning och ersÃ¤ttningssystem /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI235U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI280U",
            "title": "Kvalificerad centrumledning",
            "href": "http://www.kth.se/student/kurser/kurs/AI280U",
            "info": "",
            "credits": "15,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1N5310",
            "title": "Kvantitativa metoder, strukturekvationsmodellering LISREL",
            "href": "http://www.kth.se/student/kurser/kurs/1N5310",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI2152",
            "title": "Kvantitativa metoder tillÃ¤mpade pÃ¥ fastigheter och byggnader",
            "href": "http://www.kth.se/student/kurser/kurs/AI2152",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI207V",
            "title": "Management",
            "href": "http://www.kth.se/student/kurser/kurs/AI207V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2102",
            "title": "Marknadsanalys och fastighetsutveckling",
            "href": "http://www.kth.se/student/kurser/kurs/AI2102",
            "info": "<p>Marknadsanalys och fastighetsutveckling &#228;r en till&#228;mpad kurs i marknadsanalys med s&#228;rskild vikt p&#229; bostadsfastigheter. Metodik f&#246;r marknadsanalyser av handelsfastigheter behandlas i mindre omfattning. Speciell tonvikt l&#228;ggs p&#229; f&#246;rh&#229;llanden i USA och Sverige. M&#229;ls&#228;ttningen med kursen &#228;r att ge kunskaper om teori f&#246;r marknadsanalys samt f&#228;rdigheter i att till&#228;mpa teori f&#246;r analyser av marknadsf&#246;rh&#229;llanden som p&#229;verkar utfallet av st&#246;rre fastighets-utvecklingsprojekt. kursen f&#246;rbereder f&#246;r arbete inom byggf&#246;retag, kommuner, konsultf&#246;retag och institutionella investerare.<\/p>",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI271U",
            "title": "Marknadsanalys och fastighetsutveckling",
            "href": "http://www.kth.se/student/kurser/kurs/AI271U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI253U",
            "title": "Marknadsanalys och fastighetsutveckling /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI253U",
            "info": "",
            "credits": "6,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI281U",
            "title": "Marknadsanalys och utveckling av handelsfastigheter",
            "href": "http://www.kth.se/student/kurser/kurs/AI281U",
            "info": "",
            "credits": "5,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI286U",
            "title": "Marknadsanalys och utveckling av handelsfastigheter",
            "href": "http://www.kth.se/student/kurser/kurs/AI286U",
            "info": "",
            "credits": "3,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI241U",
            "title": "MarknadsfÃ¶ring av finansiella tjÃ¤nster/Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI241U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1129",
            "title": "MarknadsfÃ¶ring i fastighet och finans",
            "href": "http://www.kth.se/student/kurser/kurs/AI1129",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI2146",
            "title": "MarknadsfÃ¶ring i tidig fas med riskfinansiering",
            "href": "http://www.kth.se/student/kurser/kurs/AI2146",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1F5314",
            "title": "Mikroekonomisk teori",
            "href": "http://www.kth.se/student/kurser/kurs/1F5314",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI216V",
            "title": "Portfolio Management and Real Estate Finance",
            "href": "http://www.kth.se/student/kurser/kurs/AI216V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2133",
            "title": "Preparatory Course in Nordic Real Estate Market Research",
            "href": "http://www.kth.se/student/kurser/kurs/AI2133",
            "info": "",
            "credits": "4,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI250U",
            "title": "Projekt management /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI250U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI3002",
            "title": "Quantitative Methods with Real Estate Applications",
            "href": "http://www.kth.se/student/kurser/kurs/AI3002",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI2113",
            "title": "Real Estate Investment Analysis",
            "href": "http://www.kth.se/student/kurser/kurs/AI2113",
            "info": "<p>A basic course in investment analysis.<\/p>",
            "credits": "4,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2132",
            "title": "Real Estate Investment Analysis",
            "href": "http://www.kth.se/student/kurser/kurs/AI2132",
            "info": "",
            "credits": "5,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI247U",
            "title": "Real Estate Investment Analysis /Commissioned Course/",
            "href": "http://www.kth.se/student/kurser/kurs/AI247U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI248U",
            "title": "Real Estate Management /Commissioned Course/",
            "href": "http://www.kth.se/student/kurser/kurs/AI248U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI208V",
            "title": "Real Estate Market Analysis and Development",
            "href": "http://www.kth.se/student/kurser/kurs/AI208V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI217V",
            "title": "Real Estate Valuation",
            "href": "http://www.kth.se/student/kurser/kurs/AI217V",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI249U",
            "title": "Real Estate Valuation /Commissioned Course/",
            "href": "http://www.kth.se/student/kurser/kurs/AI249U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2142",
            "title": "Real Estate Valuation in an International Context",
            "href": "http://www.kth.se/student/kurser/kurs/AI2142",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI110V",
            "title": "Redovisning fÃ¶r fastighetsfÃ¶retag",
            "href": "http://www.kth.se/student/kurser/kurs/AI110V",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI221U",
            "title": "Risk och portfÃ¶ljananlyser fÃ¶r fastigheter/Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI221U",
            "info": "",
            "credits": "4,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI1128",
            "title": "SamhÃ¤llsbyggnadsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI1128",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1136",
            "title": "SamhÃ¤llsbyggnadsprocessen",
            "href": "http://www.kth.se/student/kurser/kurs/AI1136",
            "info": "",
            "credits": "12,0",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1137",
            "title": "SamhÃ¤llsbyggnadsprocessen",
            "href": "http://www.kth.se/student/kurser/kurs/AI1137",
            "info": "",
            "credits": "15,0",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI1119",
            "title": "SamhÃ¤llsbyggnadsprocessen fÃ¶r Ã¶ppen ingÃ¥ng",
            "href": "http://www.kth.se/student/kurser/kurs/AI1119",
            "info": "",
            "credits": "7,0",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI101V",
            "title": "SamhÃ¤llsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI101V",
            "info": "",
            "credits": "7,5",
            "level": "GrundnivÃ¥"
        },
            {
            "code": "AI238U",
            "title": "SkatterÃ¤tt /Uppdragsutbildning/",
            "href": "http://www.kth.se/student/kurser/kurs/AI238U",
            "info": "",
            "credits": "15,0",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1N5307",
            "title": "Spelteori tillÃ¤mpad inom fastighetsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/1N5307",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI2128",
            "title": "Stadsbyggnadsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI2128",
            "info": "<p>En forts&#228;ttningskurs i stadsbyggnadsekonomi med till&#228;mpningar p&#229; markanv&#228;ndningsproblem etc.<\/p>",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI2155",
            "title": "Stadsbyggnadsekonomi",
            "href": "http://www.kth.se/student/kurser/kurs/AI2155",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "1F5320",
            "title": "Topics in Housing and Real Estate Economics",
            "href": "http://www.kth.se/student/kurser/kurs/1F5320",
            "info": "",
            "credits": "7,5",
            "level": "ForskarnivÃ¥"
        },
            {
            "code": "AI2750",
            "title": "Vetenskapsteori och forskningsmetodik",
            "href": "http://www.kth.se/student/kurser/kurs/AI2750",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        },
            {
            "code": "AI275U",
            "title": "Vetenskapsteori och forskningsmetodik",
            "href": "http://www.kth.se/student/kurser/kurs/AI275U",
            "info": "",
            "credits": "7,5",
            "level": "Avancerad nivÃ¥"
        }
    ]
} ]
    print 'DATA:', repr(data)

    data_string = json.dumps(data)
    print 'JSON:', data_string

    return "HEJ"


@app.route('/2')
def hello_world():

    return "HEJ"







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
