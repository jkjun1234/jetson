import gspeech
import naverTTS

import os
import sys
import urllib.request
import json

client_id = "D60dTOJXcQ1gwlwN8cku"      ## papago api id, secret
client_secret = "GzYg8Nb5YA"

tts = naverTTS.NaverTTS()
gsp = gspeech.Gspeech()

cmdLists = [
        #명령어               대답                     종료 리턴값
        [u'끝내자',     '그럼 이만 물러가겠습니다.',            0],
        [u'안녕',       '안녕하십니까?',                      1],
        [u'앞에 뭐가 있는지 알려 줘',     '잠시만 기다려주십시오',   1],
        [u'전방 탐색', '잠시만 기다려주십시오', 1]
        ]

def CommandProc(stt):
    cmd = stt.strip()

    print('나: ' + str(stt))
    print(type(cmd))

    for cmdList in cmdLists:
        print("\n cmd: " + cmd + "\n cmdList: " + cmdList[0])
        if cmd == cmdList[0]:
            
            if cmdList[0] == "앞에 뭐가 있는지 알려 줘" or cmdList[0] == "전방 탐색":
                tts.play(cmdList[1])    # 명령에 응답 라벨 찾기 시작
                os.system("fswebcam ./front.jpg")
                os.system("./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights front.jpg")

                f = open("getLabels.txt", "r", encoding = 'utf8')     ##open Labels file
                srcText = f.read()
                f.close()
                
                if(srcText != '0'):
                    encText = urllib.parse.quote(srcText)   # label 번역
                    data = "source=en&target=ko&text=" + encText
                    url = "https://openapi.naver.com/v1/papago/n2mt"
                    request = urllib.request.Request(url)
                    request.add_header("X-Naver-Client-Id",client_id)
                    request.add_header("X-Naver-Client-Secret",client_secret)
                    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                    rescode = response.getcode()
                    if(rescode==200):
                        res_body = response.read()
                        #print(res_body, decode('utf-8'))

                        #json
                        res = json.loads(res_body.decode('utf-8'))
                        from pprint import pprint
                        pprint(res)

                        #file edit
                        f2 = open('translate.txt', 'w', encoding='utf8')
                        f2.write(res['message']['result']['translatedText'])
                        f2.close()

                    else :
                        print('Error Code:' + rescode)

                    getlabels = open('translate.txt', 'r', encoding='utf8')
                    result = getlabels.read()
                    tts.play(result + '가 있습니다.')    # 찾은 객체 응답
                    print(result)
                    
                else: 
                    tts.play("아무것도 찾지 못했습니다.")

                # if data == '0':      기존코드 수정
                    
                # else:               
                    
            else :
                tts.play(cmdList[1])

            print('구글 스피치: ' + cmdList[1])
            
            return cmdList[2]       # 0 종료, 1 계속
        
    print("죄송합니다. 알아듣지 못했습니다.")
    tts.play("죄송합니다. 알아듣지 못했습니다.")
    return 1

def main():
    tts.play("안녕하십니까? 명령을 내려주세요")
    
    while True:
        print("loop stt")
        stt = gsp.getText()
        if CommandProc(stt) == 0:
            break

        if stt is None:
            print("stt END")
            break

if __name__ == '__main__':
    main()
    