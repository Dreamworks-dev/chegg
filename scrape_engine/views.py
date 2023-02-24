import json
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

from utils.check_link import checkLink


def main(request, **kwargs):
    is_check = True
    context = {
        'is_check': is_check
    }
    return render(request, 'scrape_engine/index.html', context)

def result(request):
    url = request.POST["scraping_url"]
    # Check Link
    is_check = checkLink(url)
    if not is_check:
        context = {
            'is_check': is_check,
            'link': url,
        }
        return render(request, 'scrape_engine/index.html', context)

    # Extract Id
    url_exclude_param = url.split('?')[0]
    index = url_exclude_param.rfind('q')
    id = int(url_exclude_param[index+1: ])


    # Requset Header
    cookie = 'V=f5561c4a790dc60f415d04b8e4720af363ee62d917ced8.48751442; _pxvid=74a6d35a-ae1c-11ed-b5d6-7a626b66556a; _gcl_au=1.1.759856729.1676567269; _scid=77eaeab3-8feb-4496-b4bc-ad2608b230ad; _sctr=1|1676563200000; _cs_c=0; C=0; O=0; U=638c23f5499d0c9bea13d4fda7f5d258; opt-user-profile=f5561c4a790dc60f415d04b8e4720af363ee62d917ced8.48751442%252C22383174742%253A22473560126%252C22027151712%253A22030841005%252C22676901331%253A22719991359%252C23015360008%253A22996000006%252C22959210118%253A22911472111%252C22627961154%253A22641081277; _iidt=pBjB1vIhIBrzguSjqQcU32n/MpQkDhT22+bT4U9CaAeO4lHbJvFm65dTSz+psT7VpFhlPxJ1YMsiOWKV84r68SjjXA==; _vid_t=7VDGqdKfWrHiDk0srwlnMq5LfkbudBSCbBET720U/dVJvKsPsWv8b5DZ8mpvr8+B+P4x8To9Cq/mllxO6vWfd9/lfA==; DFID=web|yQJlRwPzw5EIPx72XCC6; country_code=RU; CVID=5b18645a-0ad7-43e7-a95d-fdbdde25aaba; pxcts=b4a83159-aee2-11ed-bf5d-427446424272; user_geo_location=%7B%22country_iso_code%22%3A%22RU%22%2C%22country_name%22%3A%22Russia%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ru-RU%22%5D%7D%7D; _oa_sso=https%253A%252F%252Fwww.chegg.com; local_fallback_mcid=01614677278463807076017849851762347384; s_ecid=MCMID|01614677278463807076017849851762347384; IR_gbd=chegg.com; CSID=1676656895338; ftr_blst_1h=1676658919477; PHPSESSID=c9a01be27siunr69iu6ibptvr7; CSessionID=4ca9822e-f636-4de6-8325-ca845c4c44b7; forterToken=1575c6e7ef58468486d8a66164b33b84_1676659833966__UDF43-m4_13ck; refresh_token=ext.a0.t00.v1.MbA5eEiS36hMnNIK5U1zd4pa3jIPFEYqjpSDZ0TNwM5RueGHPqSNDnA0gMuynxu08LELuL1tO_fZQ6PRVOsWpMg; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ijc5Z3ZvaWNlQGdtYWlsLmNvbSIsImlzcyI6Imh1Yi5jaGVnZy5jb20iLCJzdWIiOiJlYWM2NGVlOC0zY2JhLTQzMmMtYTk3OS01OWQ4ZjMxYTY5MDgiLCJhdWQiOiJDSEdHIiwiaWF0IjoxNjc2NjU5ODU5LCJleHAiOjE2OTIyMTE4NTksInJlcGFja2VyX2lkIjoiYXB3In0.2YP1PQOiYD32JWP3wS1561wJQ3B_9aIjHhAcVXnPkKa70if_3PFpBV2gl3d2VqLtfBqGY7o_X-o3oicyr3tupdD9PVrdU0go6WLTq3nuexuvcs0H2ctebn0Cus_dRgjQDqqWJvQpdvJYF-pJymH4P7BGEVGP_8R8FIsEnB4gmib38UIYib6tC4Kc4pTHEDdO52-y6Qku-rebo9HvboAX4hJxaDgnBSNq_CSBG4mj2spP4H57Im8-AKi5uK3-8KqHgfYgSrX6smk3rGsEV0EMcb6p8OyJXGmKMeX0y0rt85JUsOTy6Zy1kNCxwldKca1AbviB9v8_kCiJ0smj0IWFGQ; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodWIuY2hlZ2cuY29tIiwic3ViIjoiZWFjNjRlZTgtM2NiYS00MzJjLWE5NzktNTlkOGYzMWE2OTA4IiwiYXVkIjpbInRlc3QtY2hlZ2ciLCJodHRwczovL2NoZWdnLXByb2QuY2hlZ2cuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3NjY1OTg1OSwiZXhwIjoxNjc2NjYxMjk5LCJhenAiOiJGaXBqM2FuRjRVejhOVVlIT2NiakxNeDZxNHpWS0VPZSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSBvZmZsaW5lX2FjY2VzcyIsImd0eSI6InBhc3N3b3JkIiwicmVwYWNrZXJfaWQiOiJhcHciLCJjaGdocmQiOnRydWV9.EnE5gHUad8ZZ14S1GUWQFWFMa-bKUxXRHRpgWvgfNtsPVt0Ohq90ybyAgNrEJliPX2abVJZFoIoRtE9OVrpU1SbdUzDxXuvqlg03FmcnHtm1GutLr94ez165e8-ZIqIYnCF2SPXDjbU3GCBolpg6By_yUYf9aoty_VqVTjGGICFrwsImoA7csku6n5nd4WacpfQxTeo15djmzLcjOk0Cv-1aVYtuiqWkT14LfE5zS5sayQJgfNNRk-BrYuFOmIFleW0I4BzYAlRXnR_dY3nm-OYYgDNZHemPRBPU0ktnGtJNqc9nESgSGvsCVIBQk2uREKSsg1nwNZ5i7yleTX-K9Q; access_token_expires_at=1678098932; exp=C026A%7CA890H; expkey=EAF1740563EFA52FB32F3FF3DB35A811; SU=K9o-atS59Z50BjLXcFBcKdoH3T4Ch3WCOAx3HHYxZdCuyQMXbu0iL77DsQgmfTyrMzcvT98kGJ3cH_iA2zI0sfCJBUgSx8ZeHU61n5W9gFWvI44cYHPnPYUO5Z0Fj6YE; _cs_cvars=%7B%221%22%3A%5B%22Page%20Name%22%2C%22federated%20search%22%5D%2C%222%22%3A%5B%22Experience%22%2C%22desktop%22%5D%2C%223%22%3A%5B%22Page%20Type%22%2C%22auth%22%5D%2C%224%22%3A%5B%22Auth%20Status%22%2C%22Logged%20Out%22%5D%7D; _cs_id=441203b2-6402-aa04-e430-1d326a21234e.1676567635.10.1676660347.1676658953.1.1710731635408; _cs_s=11.0.0.1676662147242; _awl=2.1676660510.5-faf2a33f73a966fd8e4c7b05d416719a-6763652d6575726f70652d7765737431-1; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Feb+18+2023+03%3A01%3A37+GMT%2B0800+(Singapore+Standard+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=a003b9ab-abbf-438b-9315-1a1eb5ac91f3&interactionCount=1&landingPath=NotLandingPage&groups=fnc%3A1%2Csnc%3A1%2Ctrg%3A1%2Cprf%3A1&AwaitingReconsent=false; IR_14422=1676660498053%7C0%7C1676660498053%7C%7C; _px3=88a89e4984a35156eed652108603bd12b204e3196ee9425347090cfea2c79e3e:1vabt1jq9nYlJFo/Zbt8jxdVFY69j28j52WZEduRtzA4McctAgQyjZ/pSi8FHyumFxMdkOdCvKms8Kg8hcAj/g==:1000:dDbV/Kscgkeb0gKHMVyYM/KoIXlBxO4v0dwdkUwqKLF+K3Oj9+TMA7+N5l6UhJ+5d6nk8Tx8y5/NVrnSWp2VJY0PsrC467DTAwnlE3bCP5ivzxrVL9raZYHYXYrH+Q1IdQE8oNZLYzs94IYbK1pmtb45FwdzNF2gFetOghPMMIW31M864RyATg+WJq/fLx7zHWMFRT35yjNpbtOS/6vJjQ==; _px=1vabt1jq9nYlJFo/Zbt8jxdVFY69j28j52WZEduRtzA4McctAgQyjZ/pSi8FHyumFxMdkOdCvKms8Kg8hcAj/g==:1000:qeZKQzMa22PSQApMcP3WEC0NGzr7zgd9+sCubfj86ka3U2vrymnqDP8rjsXFP86PcI9keJeMN34wLsRNucKkiOCKO9AMEPNjRS8sawzFoSS1z0mFUYI8rOs/D+afXtIqRW4kDpzcfd0vFtlWH9fAaKvpwzczccTfE6diqggYhqnNhHdGHorQCbL4uUbwzqoqtuT+YtHINlktJs8mHUQp3/5YBnUp0HmSvzLkfNtg3TZ1dhDY/aJd0Ljx/+OQ0lr51on8ofxTfP2YFyMkXE1Gkw=='
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    api_url = 'https://gateway.chegg.com/one-graph/graphql'
    header = {
        "accept": '*/*',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-US,en;q=0.9',
        "apollographql-client-name": 'chegg-web',
        "apollographql-client-version": 'main-248c20f8-3790047346',
        "authorization": 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        "content-length": '187',
        "content-type": 'application/json',
        "cookie": cookie,
        "origin": 'https://www.chegg.com',
        "referer": 'https://www.chegg.com/',
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'cors',
        "sec-fetch-site": 'same-site',
        "user-agent": user_agent,
    }

    # Payload
    payload = {
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "36b39e8909e7d00003f355ca4d38bab164fcf06a68a2fb433a3f1138ffb1e5b7",
            }
        },
        "operationName": "QnaPageAnswer",
        "variables": {"id": id}
    }

    try:
        # Getting Answer
        res = requests.post(
            url=api_url,
            json=payload, 
            headers=header
        )
        object = json.loads(res.text)

        # Dividing Answer Type
        step_answer = ''
        total_answer = '<h2>Expert Answer</h2><div><h2>General Guidance</h2><p>The answer provided below has been developed in a clear step by step manner.<p></div>'
        main_object = object["data"]["questionByLegacyId"]["displayAnswers"]

        # 1. Only Text Answer
        if main_object.get('htmlAnswers'):
            final_answer = f'<h2>Final Answer:</h2>{main_object["htmlAnswers"][0]["answerData"]["html"]}'

        # 2. Both Text(Step) Answer and Text(Final) Answer
        elif main_object.get('sqnaAnswers'):
            child_object = json.loads(main_object["sqnaAnswers"]["answerData"][0]["body"]["text"])
            # 2-1. Step Answer
            if child_object.get('stepByStep'):
                ans_len = len(child_object['stepByStep']["steps"])
                for i in range(ans_len):
                    step_answer += f'<h3>Step {i+1}:</h3>'
                    for j in range(len(child_object["stepByStep"]["steps"][i]["blocks"])):
                        if child_object["stepByStep"]["steps"][i]["blocks"][j]["block"].get('editorContentState'):
                            for k in range(len(child_object["stepByStep"]["steps"][i]["blocks"][j]["block"]["editorContentState"]["blocks"])):
                                step_answer += f'{child_object["stepByStep"]["steps"][i]["blocks"][j]["block"]["editorContentState"]["blocks"][k]["text"]}<br>'
                        elif child_object["stepByStep"]["steps"][i]["blocks"][j]["block"].get('codeData'):
                            step_answer += f'{child_object["stepByStep"]["steps"][i]["blocks"][j]["block"]["codeData"]}<br>'


                    # Explanation
                    step_answer += '<h4>Explanation:</h4>'
                    if child_object["stepByStep"]["steps"][i].get("explanation"):
                        for k in range(len(child_object["stepByStep"]["steps"][i]["explanation"]["editorContentState"]["blocks"])):
                            parsing_text = child_object["stepByStep"]["steps"][i]["explanation"]["editorContentState"]["blocks"][k]["text"].replace("\n", "<br>")
                            step_answer += f'{parsing_text}'

            # 2-2. Final Answer
            if child_object.get('finalAnswer'):
                final_answer = '<h2>Final Answer:</h2>'
                for j in range(len(child_object["finalAnswer"]["blocks"][0]["block"]["editorContentState"]["blocks"])):
                    final_answer += f'{child_object["finalAnswer"]["blocks"][0]["block"]["editorContentState"]["blocks"][j]["text"]}<br>'

        # 3. Both Text(Step) Answer and Image(Final) Answer
        elif main_object.get('ecAnswers'):
            # 3-1. Step Answer
            step_answer = f'<h3>Step Answer:</h3>{main_object["ecAnswers"][0]["answerData"]["steps"][0]["textHtml"]}'

            # Explanation
            if main_object["ecAnswers"][0]["answerData"]["steps"][0].get('explanationHtml'):
                step_answer += f'<h4>Explanation:</h4>{main_object["ecAnswers"][0]["answerData"]["steps"][0]["explanationHtml"]}'
            
            final_answer = f'<h2>Final Answer:</h2>{main_object["ecAnswers"][0]["answerData"]["finalAnswerHtml"][0]}'

        total_answer += step_answer + final_answer

        # Parsing Answer as HTML
        soup = BeautifulSoup(total_answer, "html.parser")
        
        extends = '{% extends "scrape_engine/master.html" %}'
        start_block = '{% block content %}'
        end_block = '{% endblock %}'
        html = f'{extends}{start_block}{str(soup)}{end_block}'

        text_file = open("scrape_engine/templates/scrape_engine/result.html", "w", encoding='utf-8')
        text_file.write(str(html))
        text_file.close()

        return render(request, 'scrape_engine/result.html')
    
    except Exception:
        return render(request, 'scrape_engine/report.html')
