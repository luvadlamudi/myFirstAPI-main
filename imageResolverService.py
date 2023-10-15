from flask import Flask, request
from flask_cors import CORS
import mysql.connector
import sys
import boto3
import os


app = Flask(__name__)


ENDPOINT="shopify.c1eabem1vluk.us-east-1.rds.amazonaws.com"
PORT="3306"
USR="admin"
DBNAME="shopify"



CORS(app)
 

def insertIntoDB(imageName, imageURL):
    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd="password123!", port=PORT, database=DBNAME, use_pure=True)
        cur = conn.cursor()
        cur.execute("""
        Insert into Images(url, name) values ('{0}', '{1}')
        """.format(imageName, imageURL))
        conn.commit()
        query_results = cur.fetchall()
        print(query_results, "results")
    except Exception as e:
        print("Database connection failed due to {}".format(e))      


@app.route('/getAllImages')
def getAllImages():
    returnElement = "<div style='display: flex; flex-direction: column'>"
    query_results = getAllImagesFromDB()
    for image in query_results:
            returnElement += createNewImgTag(image[0])
    returnElement += "</div>"
    return returnElement  
    

def getAllImagesFromDB():
    print('called')
    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd="password123!", port=PORT, database=DBNAME, use_pure=True)
        cur = conn.cursor()
        cur.execute("""
        select * from Images
        """)
        results= cur.fetchall()
        conn.close()
        print(results)
        return results
    except Exception as e:
        print("Database connection failed due to {}".format(e)) 


def createNewImgTag(url):
    return "<img src=" + url + ">"

@app.route('/getImage')
def getSpecificImage():
    name = request.args.get('name')

    for image in listOfImages:
        if(name == image['name']):
            return createNewImgTag(image['url'])
    
    return "nothing found"

@app.route('/queryFromUser')
def getFromQuery():
    tagName = request.args.get('tag')
    responseObj = '<div>'

    for image in listOfImages:
        for tag in image['tags']:
            if(tagName in tag):
                responseObj += createNewImgTag(image['url'])
                break


    responseObj += '</div>'
    return responseObj


if __name__ == '__main__':
    app.run()