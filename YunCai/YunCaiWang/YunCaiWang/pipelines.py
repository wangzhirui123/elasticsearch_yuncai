# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from twisted.enterprise import adbapi
from MySQLdb import cursors
from w3lib.html import remove_tags

class mysqlTwistedpipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings['HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True

         )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        print failure


    def do_insert(self,cursor,item):
        pass
        # dict_item = dict(item)
        # select_pro_id = 'select Id from province where provincename = "%s"'%dict_item['province']
        # cursor.execute(select_pro_id)
        # dict_item['province_id'] = cursors.fetchone()[0]
        # select_cid = 'select id from city where city_name = "%s"'%dict_item['city']
        # cursor.execute(select_cid)
        # dict_item['city_id'] = cursors.fetchone()[0]
        # print '1'*20,dict_item



class YuncaiwangPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('101.201.70.139','root','Myjr678!@#','ant',charset='utf8')
        self.cur = self.conn.cursor()

    def getprovince_id(self,name):
        sql = 'select Id from province where provincename like "%%%s%%"'%name
        self.cur.execute(sql)
        try:
            return self.cur.fetchone()[0]
        except:
            return 0

    def getcity_id(self,name):
        sql = 'select id from city where city_name LIKE "%%%s%%"'%name
        self.cur.execute(sql)
        # print '1',name
        # try:

        return self.cur.fetchone()[0]
        # except:
        #     return 0



    def process_item(self, item, spider):
        dict_item = dict(item)
        # print dict_item['city']
        dict_item['province_id'] = self.getprovince_id(dict_item['province'])
        dict_item['city_id'] = self.getcity_id(dict_item['city'])
        sql = 'insert into purchasing_demand(title,province_id,province_name,city_id,city_name,unit,contact,phone,publish_time,detail_html,iscatch,review_status)VALUES ("%s","%d","%s","%d","%s","%s","%s","%s","%s","%s",1,2)'%(dict_item['title'],dict_item['province_id'],dict_item['province'],dict_item['city_id'],dict_item['city'],dict_item['company_name'],dict_item['contact_nam'],dict_item['phone'],dict_item['publish_time'],dict_item['con'])
        self.cur.execute(sql)
        self.conn.commit()
        # sql = 'insert into wx_company_invite (work_province_id,work_city_id,work_years,work_name,label,work_description,invite_date,work_address,phone,work_salary,company_name,link_man) VALUES ("%d","%d",2,"%s","%s","%s","%s","%s","%s","面议","%s","%s")'%(dict_item['province_id'],dict_item['city_id'],dict_item['title'],'劳务分包',dict_item['con'],dict_item['publish_time'],dict_item['province']+dict_item['city'],dict_item['phone'],dict_item['company_name'],dict_item['contact_nam'])
        # self.cur.execute(sql)
        # self.conn.commit()
        return item

from models.es_types import YunCaiType
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
es = connections.create_connection(hosts="103.76.85.75")
def gen_suggests(index,info_tuple):
    #根据字符串生成搜索建议数组
    used_word = set()       #定义一个元祖存每次放建议词
    suggest = []            #用于存放最后返回的建议词
    for t,w in info_tuple:  #遍历传进来的元祖信息
        if t:               #如果文本不为空
            words = es.indices.analyze(index=index,analyzer="ik_max_word",params={'filter':['lowercase']},body=t)#
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r['token'])>1])
            new_words = anylyzed_words-used_word
        else:
            new_words = set()

        if new_words:
            suggest.append({'input':list(new_words),'weight':w})

        return suggest
class ElasticsearchPipline(object):


    def process_item(self, item, spider):
        #将item转化为es数据
        from models.es_types import YunCaiType
        yucai = YunCaiType()
        yucai.title = item['title']
        yucai.publish_time = item['publish_time']
        yucai.con = remove_tags(item['con'])
        yucai.province = item['province']
        # yucai.province_id = item['province_id']
        yucai.city = item['city']
        # yucai.city_id = item['city_id']
        yucai.company_name = item['company_name']
        yucai.phone = item['phone']
        yucai.contact_nam = item['contact_nam']
        yucai.suggest = gen_suggests(YunCaiType._doc_type.index,((yucai.title,10),))
        yucai.save()
        return item












