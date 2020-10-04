#db.py
import os
import pymysql
from flask import jsonify
from collections import defaultdict

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn

def classify(object):
    conn = open_connection()
    with conn.cursor() as cursor:
        return object
        for item in object:
            product_id = cursor.execute('SELECT product_id FROM products;')
            #if not product_id:
                #rec_id = cursor.execute('SELECT rec_id FROM plastic_rec_mapping where type = %s;',(item));
                #if not rec_id:
                    #cursor.execute('INSERT INTO classification (recyclable, unclassified, isActive,points) VALUES(%s, %s, %s, %s)', ('', item, 1,0));
            '''    else:
                    points = cursor.execute('SELECT points FROM plastic_type_rec_mapping where rec_id = %s', rec_id);
                    cursor.execute('INSERT INTO classification (recyclable, unclassified, isActive,points) VALUES(%s, %s, %s)',
                                   (item,'', 1,points));
            else:
                mapping_id = cursor.execute('SELECT mapping_id FROM product_rec_mapping where product_id = %s', product_id);
                rec_id =  cursor.execute('SELECT rec_id FROM plastic_rec_mapping where mapping_id = %s', mapping_id);
                points = cursor.execute('SELECT points FROM plastic_type_rec_mapping where rec_id = %s', rec_id);
                cursor.execute(
                    'INSERT INTO classification (recyclable, unclassified, isActive,points) VALUES(%s, %s, %s)',
                    (item, '', 1, points));
            '''
    return item
    conn.commit()
    conn.close()

def details():
    conn = open_connection()
    with conn.cursor() as cursor:
        # return 'SELECT sum(points) FROM classification where isActive = 1;'
        result = cursor.execute("SELECT recyclable,NULL unclassified, CAST(SUM(points) AS CHAR(4)) as points FROM classification where isActive = 1 and recyclable <> '' group by recyclable  UNION SELECT NULL recyclable,unclassified, CAST(SUM(points) AS CHAR(4)) as points FROM classification where isActive = 1 and unclassified <> '' group by unclassified;")
        detail = cursor.fetchall()

        #response = defaultdict(int)
        #for i, row in enumerate(detail):

        #    if i == 0:
        #        continue
        #    for a, b, c, d in row:
         #       if a != 'No entry':
         #           response[a] += d
         #       else:
         #           response[b] += d
        # if result > 0:
        #     got_detail = response
        # else:
        #     got_detail = 'No items pending for recycling'
    conn.close()
    return jsonify(detail)

def points():
    conn = open_connection()
    with conn.cursor() as cursor:
        # return 'SELECT sum(points) FROM classification where isActive = 1;'
        result = cursor.execute(
            "SELECT CAST(SUM(points) AS CHAR(4)) as points FROM classification where isActive = 1 and recyclable <> '';")
        detail = cursor.fetchall()
    conn.close()
    return jsonify(detail)

def classify_prod(obj):
    conn = open_connection()
    points = ""
    with conn.cursor() as cursor:
        for item,value in obj.items():
            product_id = None
            rec_id = None
            result = cursor.execute('SELECT product_id FROM products where product_name = %s;',(item))
            product_id = cursor.fetchall()
            if not product_id:
                result = cursor.execute('SELECT recid FROM plastic_rec_mapping where type = %s;',(item))
                rec_id = cursor.fetchall()
                if not rec_id:
                    cursor.execute('INSERT INTO classification(recyclable, unclassified, isActive,points) VALUES(%s, %s, %s, %s)', ('', item,int("1"),int("0")));
                    conn.commit()
                else:

                    result = cursor.execute('SELECT points FROM plastic_type_rec_mapping where rec_id = %s',(rec_id[0]['recid']));
                    points = cursor.fetchall()
                    cursor.execute('INSERT INTO classification (recyclable, unclassified, isActive,points) VALUES(%s, %s, %s, %s)',
                                   (item,'',int("1"),int(points[0]['points'])));
                    conn.commit()
            else:
                result = cursor.execute('SELECT mapping_id FROM product_rec_mapping where product_id = %s',(product_id[0]['product_id']));
                mapping_id = cursor.fetchall();
                result = cursor.execute('SELECT recid FROM plastic_rec_mapping where mapping_id = %s', (mapping_id[0]['mapping_id']));
                rec_id = cursor.fetchall();
                results = cursor.execute('SELECT points FROM plastic_type_rec_mapping where rec_id = %s',(rec_id[0]['recid']))
                points = cursor.fetchall()
                cursor.execute(
                    'INSERT INTO classification (recyclable, unclassified, isActive,points) VALUES(%s, %s, %s ,%s)',
                    (item, '', int("1"), int(points[0]['points'])))
                conn.commit()
        
#if result > 0:
#    got_detail = jsonify(detail)
#else:
#    got_detail = 'No items pending for recycling'
    conn.close()
    return jsonify(points)