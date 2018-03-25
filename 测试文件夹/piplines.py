#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

'''把数据存储到MYSQL'''

from datetime import datetime
# 1. Mysql_db
# 2. pymsql # python  sql语句
# 3. ORM  sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# 模型类
class News(Base):

    __tablename__ = 'news'

    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表引擎
        "mysql_charset": "utf8"  # 表的编码格式
    }

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String(50), nullable=False)  # null
    article_link = Column(Text, nullable=False)  # Null
    author = Column(String(50), nullable=False)  # Null
    author_link = Column(Text, nullable=False)  # Null
    pub_date = Column(DateTime, nullable=False)  # Null
    keyword = Column(String(50), nullable=False)  # Null


class Pipeline(object):

    def __init__(self):
        # 1. 获取一个Mysql的连接对象
        # 数据库+数据库驱动模块
        url = 'mysql+mysqlconnector://root:mysql@127.0.0.1:3306/spider?charset=utf8'
        self.conn = create_engine(url)
        Base.metadata.create_all(bind=self.conn)  # 创建数据库,如果有就忽略

    def process_item(self, item):
        Session = sessionmaker(bind=self.conn)
        session = Session()
        news = News(
                title='title',
                article_link='article_link',
                author='author',
                author_link='author_link',
                pub_date=datetime.now(),
                keyword='keyword'
             )
        session.add(news)
        session.commit()
        session.close()

Pipeline().process_item(1)