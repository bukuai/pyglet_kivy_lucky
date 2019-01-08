# -*- coding: utf-8 -*-
import pickle

def ready(file, list):
    dbfile = open(file, 'wb')
    pickle.dump(list, dbfile)
    dbfile.close()

    s= pickle.load(open(file, 'rb'))
    print('ready', file, s)

#total
total = list(range(1, 23))
ready('total',total)

#prize1
ready('prize1', [])
#prize2
ready('prize2', [])
#prize3
ready('prize3', [])
#prize5
ready('prize5', [])
#prize100
ready('prize100', [])
