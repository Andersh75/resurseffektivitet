import csv
from datetime import date, datetime, timedelta

from operator import itemgetter
import string


# Remove Column from Table
def remove_col(list1, i):
    temp_list_suf = []
    temp_list_pre = []
    temp_list = []
    for n in list1:
        temp_list_suf.append(n[i+1:])
        temp_list_pre.append(n[:i])
    for index, item in enumerate(list1):
        temp_list.append(temp_list_pre[index] + temp_list_suf[index])
    return temp_list

# Reformat date
def reformat_date(list1):
    i = 0
    for p in range(0, len(list1)):
        year_var = "2016"
        if list1[p][i][2] == "/":
            day_var = list1[p][i][:2]
            #print day_var
        else:
            day_var = "0" + list1[p][i][:1]
            #print day_var
        if list1[p][i][-3] == "/":
            #print "hej"
            month_var = list1[p][i][-2:]
            #print month_var
        else:
            month_var = "0" + list1[p][i][-1:]
            #print month_var

        #print list1[p][7]
        if list1[p][7]:
            year_var = list1[p][7]

        list1[p][i] = year_var + "-" + month_var + "-" + day_var
        year_var = "2016"

        #print list1[p][7]
    return list1

# Insert Column to Table
def add_col(list1):
    for i in range(0, len(list1)):
        list1[i].append("")
    return list1


#
def extract_start_slut_tid(list1):
     i = 1
     for p in range(0, len(list1)):
        list1[p][-2] = list1[p][i][0:2]
        list1[p][-1] = list1[p][i][3:5]
        # print list1[p][i]

     return list1


# Separate teachers
def separate_teachers(list1):
    temp_list = []
    for p in range(0, len(list1)):
        words = list1[p][4].split()
        for word in words:
            #print word
            alist = []
            alist = list1[p]
            alist[4] = word

            #print alist
            temp_list.extend(alist)
            #print "hej"

    #print temp_list



    return temp_list

# Separate teachers
def separate_rooms(list1):
    temp_list = []
    for p in range(0, len(list1)):
        words = list1[p][2].split()
        for word in words:
            #print word
            alist = []
            alist = list1[p]
            alist[2] = word

            #print alist
            temp_list.extend(alist)
            #print "hej"

    return temp_list
