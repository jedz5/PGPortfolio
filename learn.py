import numpy as np
def simulate():
    cs = cp = 0.0025
    def close(mon,t,new_v):
        m = mon[t]
        m[1] = m[0]
        m[1,1] = new_v
        omega(m)
        if(t < len(mon) - 1):
            mon[t+1][0] = m[1]
    def omega(m,y = True):
        if y:
            m[1,3] = m[1,1] / (m[0,1]+1.0e-10) #y
            tmp = (m[0,2] * m[1,3])
            m[1,2] = tmp / (sum(tmp)+1.0e-10)
        else:
            tmp = m[0,0] * m[0,1]
            m[0, 2] = tmp / (sum(tmp) + 1.0e-10)
    def sell(mon,howmany,which):
        if howmany == 0:
            return
        m = mon[0]
        sold = m[0,which] * howmany  #份数
        m[0, which] -= sold
        m[0,0] += sold * m[1,which] * (1 - cs)
        omega(mon, False)
    def buy(mon,howmany,which):
        if howmany == 0:
            return
        m = mon[0]
        bought = m[0,0] * howmany #现金
        m[0,0] -= bought
        m[0,which] += bought * (1-cp) / m[1,which]
        omega(mon,False)
    Day = 3
    money = np.zeros((Day,2,4,5)) #样本,开盘/收盘,份/元/omega/比,现金/资产1/资产2/资产3/资产4
    money[0,0,0] = [0,1000,1000,1000,1000] #份
    money[0,0,1] = [1,1,1,1,1] #元
    money[0,0,2] = [0,0.25,0.25,0.25,0.25] #omega
    money[0,0,3] = [1,1,1,1,1] #比

    value = [[1,2,0.5,1,1],[1, 1, 1, 2, 1],[1,1,3,1,1]]
    to_sell = [(0,0),(0.3,2), (1.0,1)]
    to_buy = [(0,0),(1.0,3), (0.5,3)]
    np.set_printoptions(precision=4)
    np.set_printoptions(suppress=True)
    pp = 1
    for x in range(Day):
        print('day {} open:'.format(x))
        print(money[x,0])
        if x > 0:
            print('---------after sell {}'.format(to_sell[x]))
            sell(money[x], to_sell[x][0], to_sell[x][1])
            if x == 1:
                sell(money[x], 0.4, 4)
            print(money[x, 0])
            print('----after buy {}'.format(to_buy[x]))
            buy(money[x], to_buy[x][0], to_buy[x][1])
            print(money[x, 0])
            v0 = sum(money[x, 0, 0] * money[x, 0, 1])
            v1 = sum(money[x - 1, 0, 0] * money[x - 1, 0, 1])
            # pt = sum(money[x - 1, 0, 2] * money[x, 0, 3])
            pt = v0 / v1
            print('Pt: %2f = %2f / %2f' % (pt, v0, v1))
            miu = pt/pp
            print('μ:{} = {} / {}'.format(miu,pt,pp))
            sold = np.maximum(money[x - 1,1,2,1:] - miu*money[x,0,2,1:],0)
            print('sold ω= {}'.format(sold))
        print('day {} close:'.format(x))
        close(money,x,value[x])
        print(money[x, 1])
        v0 = sum(money[x,1,0]*money[x,1,1])
        v1 = sum(money[x,0,0]*money[x,0,1])
        pp = sum(money[x,0,2] * money[x,1,3])
        print('P\': %2f = %2f / %2f'%(pp,v0,v1))
if __name__ == '__main__':
    simulate()