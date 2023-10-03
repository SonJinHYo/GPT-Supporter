# GPT-Supporter

### 개발 기간 : 2023-08 ~ 2023-09  

(프론트엔드와 백엔드의 README는 각 폴더 내에 작성했습니다)


## Intro

ChatGPT를 보다 잘 사용하게 도와주는 웹사이트입니다.  
ChatGPT에게 질문하는 방식에만 변화를 주어도 성능 향상이 잘 이루어집니다. 여러가지 방법 중 하나로 질문하기 전 사용자의 정보를 ChatGPT에게 알려주는 방식이 있습니다.  
이런 질문 방식을 적용하여, 사용자(대학생)의 정보와 몇가지 데이터를 저장해두면 ChatGPT에게 사용자의 정보를 효율적으로 전달하는 템플릿을 제공합니다.

대학 전공 수준의 질문은 광범위하고 수준이 가파르게 변화합니다. 이에 맞춰 질문자의 전공, 참고하는 자료, 수준 등을 입력하면 OpenAI ChatGPT 가이드라인에 맞춰진 프롬프트를 제공합니다.

<br>

[웹사이트 바로가기](https://gpt-supporter.click)

<br><br>

## Architecture

![image](https://github.com/SonJinHYo/GPT-Supporter/assets/88013439/a15072cd-c194-4e20-9743-6e66e8fbcc12)


- nginx에서 정적 파일을 모두 처리하도록 react의 build 폴더를 nginx 컨테이너로 복사했습니다.
  - ALB에서 http 80포트, https 443포트를 리슨하고 nginx로 로드밸런싱 합니다.
    - http 80포트를 https 443포트로 리다이렉트합니다.
- RDS에 프라이빗하게 접근이 가능하도록 클러스터 단위에서 VPC가 공유되도록 했습니다.
- nginx, django 컨테이너를 하나의 Task로 가지고 현재 서비스에선 하나의 Task만을 사용하고 있습니다.

- 웹사이트 주소 : gpt-supporter.click


