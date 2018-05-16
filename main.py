from doubanscrap import Douban_Spider
from time import sleep
import random
import pymysql

conn=pymysql.connect("localhost","root","123p123p","douban",charset='utf8')
cur=conn.cursor()

def read_mids(filename):
    with open(filename) as fr:
        mids = fr.readlines()
        mids = [each[:-1] for each in mids]
    return mids

def write_mids(filename,mids):
    with open(filename,'w') as fw:
        fw.seek(0)
        fw.truncate()
        for each in mids:
            fw.write(each+'\n')

def write_continue(filename,mids):
    with open(filename,'a') as fw:
        for each in mids:
            fw.write(each+'\n')

def store(info):
    try:
        cur.execute("INSERT INTO m_info (m_id,m_cn_name,m_real_name,m_release_time,m_score,m_pic_url,m_sheet_length,m_another_name,m_brief) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(info[0],info[1],info[2],info[3],info[4],info[5],info[9],info[12],info[13]))
        cur.connection.commit()
        for director in info[6]:
            cur.execute("INSERT INTO m_directors (m_id,m_director) VALUES(%s,%s)",(info[0],director))
        cur.connection.commit()
        for actor in info[8]:
            cur.execute("INSERT INTO m_actors (m_id,m_actor) VALUES(%s,%s)",(info[0],actor))
        cur.connection.commit()
        for mtype in info[7]:
            cur.execute("INSERT INTO m_types (m_id,m_type) VALUES(%s,%s)",(info[0],mtype))
        cur.connection.commit()
        nations=info[10].split('/')
        for nation in nations:
            cur.execute("INSERT INTO m_nations (m_id,m_nation) VALUES(%s,%s)",(info[0],nation))
        cur.connection.commit()
        languages=info[11].split('/')
        for language in languages:
            cur.execute("INSERT INTO m_language (m_id,m_language) VALUES(%s,%s)",(info[0],language))
        cur.connection.commit()
    except Exception:
        print("输入异常\n")

def download():
    mids=read_mids('mids.txt')
    finshed_mids=read_mids('finshmids.txt')
    n=input("输入要爬取多少条数据:")
    index=0
    spider = Douban_Spider()
    for index in range(int(n)):
        info=spider.begin(mids[index],mids,finshed_mids)
        if info is ():
            break
        elif info==1:
            continue
        print("已爬取第",index+1,"个电影\n" )
        store(info)
        sleep(2+random.randint(1,3))

    finshed_mids.extend(mids[:index+1])
    mids=mids[index+1:]
    write_mids('finshmids.txt',finshed_mids)
    write_mids('mids.txt',mids)

download()