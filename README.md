# goToHawaii

하와이를 가고 싶습니다.

서핑하며 룰루랄라

[환경구축]
1. 개발환경 구축
	- 윈도우10 : 키움증권 api때문에 linux가 아닌 윈도우를 사용
	- pyCharm
	- Anaconda3 (python 3.7)
	- SQLite3 설치 (python 기본패키지이므로 설치 불필요)
	- DB file을 보기위해 DB browser 설치
	- 증권사 API : KOA Studio 및 키움영웅문4 설치 필요
    - git 주소 : https://github.com/muje2002/goToHawaii
    - pycharm - File - settings - project interpreter - conda environment 에서 conda의 python 3.7을 선택 
    - 실행도중 No module named 에러가 발생하면 pycharm - File - settings - project interpreter - 우측에 + 버튼을 눌러서 필요한 module을 설치하면 된다.

2. 전날 프로그램 로직 순서
    1) windows 자동프로그램을 이용하여 아래 python code가 장 마감날 4시에 자동으로 running 하도록 설정 
    2) webcrawling.py 를 실행하여 주가 data를 stock.db에 저장 <필요한 날짜만큼만 돌게 수정 필요>
    3) preprocessing.py 를 실행하여 stock.db 로부터 pre.db를 생성 (이때 pre process는 bbThrough.py안의 함수)
    4) pre.db로부터 candidate 후보를 선택하여 candidate.json으로 저장 (bbTrough.py 에 함수 만들 것)
    
3. 당일 프로그램 로직 순서    
    1) 매수 
        1) windows 자동프로그램을 이용하여 장중 3시 15분에 자동으로 running 하도록 설정
        2) candidate.json 에서 최종 매수 종목을 선정
        3) 정해진 portion 만큼 정해진 방법대로 매수
    2) 매도
        1) windows 자동프로그램을 이용하여 장중 3시 0분에 자동으로 running 하도록 설정
        2) 정해진 방법대로 매도 
            (+29일) 매수(3시 15분)가 시작되기 전에 전량 매도될 수 있도록 설정

4. python 스케쥴러 : https://lemontia.tistory.com/508

5. SWAPY 프로그램 사용설명
    https://github.com/pywinauto/SWAPY
    SWAPY를 통해 윈도우 창의 구성을 확인할 수 있다. (kiwoom login 및 버전처리를 위해 필요)
    1. anaconda 32 bit로 설정
    2. pywinauto 설치
    3. python 을 3.7.5 version으로 down 할것 (혹은 3.8.0) anaconda 32 bit으로 설정하니 자동으로 되는 듯? (3.7.4)
    4. pycharm 을 관리자 권한으로 실행해야 한다.    
    
4. [Data 관리] 주가데이터 저장 & daily update 환경 구축 (NA 제거 & Adj close 반영) 
	- KOSPI & KOSDAQ
	- 기본적 분석을 위한 back data는?
	- 미국주식, 중국주식?
	- 선물, 금, 환율, 지수?

5. [Data mining] Data Mining 환경 구축
	- db table -> df -> numpy array?
	- 패턴을 넣으면 내가 원하는 Data통계치가 나올 수 있는 환경 구축
		i. db -> numpy arrary로 변경? (data 통계를 잘 뽑을 수 있는 data type으로 변경 필요)
		ii. 모든 패턴에 동일하게 적용되는 변수들 정의
	
	- 특정패턴 발생을 기점으로 N일 후 주가등락폭 산술/기하평균, 승률, 횟수, 그 외 중요자료들

6. Data Mining 을 통한 패턴분석
	- 특정패턴의 정의 (N일의 범위)
	- 패턴별 Data 분석 (기하평균, 승률, 횟수, Corelation Attributes, Portion)

7. 알고리즘 적용한 백테스트 환경 구축 (zipline)
	- zipline 은 환경구축이 어려워서 직접 코딩으로 구현하였다.
	
8. 자동 매수/매도 프로그램 구현 (Kiwoom)
	- 매수, 매도의 최적화 가능?
	일단은 단순히 매수/매도하는 프로그램으로 시작해보자.	

