import pickle
import time
while True:
    try:
        total = pickle.load(open('total','rb'))
        prize1 = pickle.load(open('prize1', 'rb'))
        prize2 = pickle.load(open('prize2', 'rb'))
        prize3 = pickle.load(open('prize3', 'rb'))
        prize5 = pickle.load(open('prize5', 'rb'))
        prize100 = pickle.load(open('prize100', 'rb'))
    except Exception:
        pass

    print('---------------------------------')
    print(time.ctime())
    print('total', len(total), total)
    print('prize1', prize1)
    print('prize2', prize2)
    print('prize3', prize3)
    print('prize5', prize5)
    print('prize100', prize100)
    print('---------------------------------')
    a = input('press to get...')
    if a == 'x':
        break