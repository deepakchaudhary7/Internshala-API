import requests
from bs4 import BeautifulSoup
from lxml import etree
import urllib2
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if(request.method == 'GET'):
        Request_URL = 'https://internshala.com/internships'
        response = urllib2.urlopen(Request_URL)

        #################################################################################################
        #setting up the BeautifulSoup
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')

        # setting up the etree (lxml.html)
        response = urllib2.urlopen(Request_URL)

        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        ##################################################################################################


        internship_type = []
        internship_company = []
        internship_URL = []
        stipend = []
        location = []
        duration = []

        base_URL = "https://internshala.com/"

        divTag = soup.find_all("div", {"class": "individual_internship_header"})

        for element in divTag:
            z = element.find_all('h4')
            cnt = 1

            for txt in z:
                if(cnt):
                    internship_type.append(txt.text.encode('utf-8').rstrip().lstrip())
                    link = txt.find('a')['href']
                    internship_URL.append(base_URL + str(link))
                else:
                    internship_company.append(txt.text.encode('utf-8').rstrip().lstrip())
                cnt = 0


        divTag = soup.find_all("div", {"class": "individual_internship_details"})

        for element in divTag:
            z = element.find_all('a')
            location.append(z[0].text.encode('utf-8'))

            z = element.find_all('tbody')

            for row in z:
                tds = row.find_all('td')
                duration.append(tds[1].text.encode('utf-8').rstrip().lstrip())
                stipend.append(tds[2].text.encode('utf-8').rstrip().lstrip())


        length_of_data = len(internship_URL)

        data = {}

        for i in range(0,length_of_data):
            inner_dic = {}
            inner_dic['internship_type'] = internship_type[i]
            inner_dic['internship_company'] = internship_company[i]
            inner_dic['stipend'] = stipend[i]
            inner_dic['location'] = location[i]
            inner_dic['duration'] = duration[i]

            data[internship_URL[i]] = inner_dic


        ## now creating the json dump to return the data
        final_data = json.dumps(data)

        json_response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

        return json_response



if __name__ == "__main__":
    app.run()
