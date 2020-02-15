import environ as env
import json

if __name__ == "__main__":
    pname = "bbThrough"
    path = env.DBPATH + pname + "/"

    dict = {}
    #dict['goThrough'] = True
    dict['goUp'] = True

    i = 0

    #nearHigh # 250 1.1 0.9 조합 좋음 확인 완료
    n1 = [250]
    n2 = [1.1]
    n3 = [0.9]

    #bbwidth
    #b21 = [7, 8]
    #b22 = [0.06, 0.07, 0.08]
    b31 = [5] # 5, 0.04 좋은 확인완?????
    b32 = [0.04]

    #enoughVol  # [5,7] [0, 100, 200] 5, 200 이 5,100이나 7.200보다 좋네?
    e1 = [5]
    e2 = [200]

    #enoughTodayVol (5,4 조합이 좋음) 확인 완
    et1 = [5]
    et2 = [4]

    # noGoUpFor # 4,5,6 # 5가 베스트 확인 완
    ng = [5]

    # afterPeriod
    ap = [39]

    for nn1 in n1:
        for nn2 in n2:
            for nn3 in n3:
                dict['nearHigh'] = [[nn1,nn2,nn3]]

                #for bb21 in b21:
                    #for bb22 in b22:
                for bb31 in b31:
                    for bb32 in b32:
                        #dict['bbwidth'] = [[bb21, bb22], [bb31, bb32]]
                        dict['bbwidth'] = [[bb31, bb32]]

                        for ee1 in e1 :
                            for ee2 in e2:
                                dict['enoughVol'] = [[ee1,ee2]]

                                for ett1 in et1:
                                    for ett2 in et2:
                                        dict['enoughTodayVol'] = [[ett1, ett2]]

                                        for ng1 in ng:
                                            dict['noGoUpFor'] = ng1

                                            for ap1 in ap:
                                                dict['afterPeriod'] = ap1

                                                i = i + 1
                                                j = json.dumps(dict)
                                                f = open("{}{}.json".format(path, i), "w")
                                                f.write(j)
                                                f.close()