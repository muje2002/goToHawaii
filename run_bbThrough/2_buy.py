# 윈도우의 자동프로그램을 이용하여 이 코드가 매일 장 3시 15분에 run할 수 있도록 설정하자.
# db 폴더안에 yyyymmdd 폴더가 있으면 run
# yyyymmdd_buy_candidate.json을 read하여 최종 매수종목을 선별, yyyymmdd_buy.json 에 write한다.
#   1차매수) 3시 15분에 1호가 낮춰서 매수
#   2차매수) 매수 안된 물량이 있으면 15분 매수건 취소하고 남은 물량만큼 16분에 1호가 낮춰서 매수
#   3차매수) 매수 안된 물량이 있으면 16분 매수건 취소하고 남은 물량만큼 17분에 1호가 낮춰서 매수
#   4차매수) 매수 안된 물량이 있으면 17분 매수건 취소하고 남은 물량만큼 18분에 현재 호가로 매수
#   5차매수) 매수 안된 물량이 있으면 18분 매수건 취소하고 남은 물량만큼 19분에 현재 호가로 매수
#   6차매수) 동시호가로 매수 (5차매수건이 자동으로 넘어갈 것)
# 매수가 된 종목은 yyyymmdd_sell.json 및 yyyymmdd_bought.json 에 기록해둔다.
# 매수가 안 된 종목은 pass

# yyyymmdd_buy.json 의 양식
# yyyymmdd_bought.json 의 양식
# yyyymmdd_sell.json 의 양식

# 물량계산, 호가단위계산, 매수취소/매수, cron 스케쥴
# code, name, money2buy, price[], vol[]
"""
  goUP : 양봉인지의 유무
  nearHigh [a,b,c]] : 250일간 최고가에서 1.1 ~ 0.9 사이에 가격이 유지되고 있는가
    직전 249일간의 최고가 미리 계산
  enoughTodayVol [5,4] : 오늘의 거래량이 직전 5일간 거래량의 4배 이상인가?
    직전 5일간의 거래량 미리 계산
  totalPrice [a] : 오늘 거래대금이 1억 이상인가?
"""

def makeDecision():
    # read candidate
    # make decision
    # write buy json
    pass

def isRemain():
    return True

def buy1():
    pass

def buy2():
    if(isRemain() == False):
        return
    pass

def buy3():
    if (isRemain() == False):
        return
    pass

def buy4():
    if (isRemain() == False):
        return
    pass

def buy5():
    if (isRemain() == False):
        return
    pass

def writeBought():
    pass

def writeSell():
    pass

if __name__ == "__main__":
    makeDecision()
    buy1()
    buy2()
    buy3()
    buy4()
    buy5()
    writeBought()
    writeSell()

