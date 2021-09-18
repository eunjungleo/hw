import os
import sys
import urllib.request
import json
import pandas as pd
from openpyxl import Workbook
from pandas import json_normalize


# 인증
client_id = "p8SenRAS7NLnzhjRTEdT"
client_secret = "UkbBYoc3RH"


# 키워드: nct127
encText = urllib.parse.quote("nct127")

#서비스, 출력 개수를 변수로 받는 함수
def get_result(service, number):
    
    # 서비스, 출력 개수를 변수로 받아서 url 생성
    url = "https://openapi.naver.com/v1/search/" + service + "?query=" + encText + "&display=" + str(number) # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    
    if(rescode==200):
        response_body = response.read()

        result = response_body.decode('utf-8')
        # str -> json -> df
        result = json.loads(result)
        df = pd.DataFrame(result)
        
        # 중첩된 dict에서 items만 추출
        items = df['items']
        df = json_normalize(result['items'])
        
        # 엑셀 파일로 저장
        sheet = service + ".xlsx"
        df.to_excel(sheet, sheet_name=service)

    else:
        print("Error Code:" + rescode)
        
        
# 결과값 출력
result1 = get_result("news", 20) #뉴스, 20개
result2 = get_result("blog", 10) #블로그, 10개
result3 = get_result("kin", 10) #지식in, 10개