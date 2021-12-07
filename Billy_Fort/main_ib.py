import time
from ib_insync import *

from config import position_update_frequency, price_update_frequency, liquidation_treshhold, white_list, \
    account_type, liquidation_treshhold_options

util.startLoop()


ib = IB()

if account_type == "testing":
    ib.connect('127.0.0.1', 7497, clientId=1)
    ib.reqMarketDataType(3)
else:
    ib.connect('127.0.0.1', 7496, clientId=1)

auxx = ib.positions()

ticks = {}
avgs = {}
pos = {}
seen = []

ticks_opt = {}
avgs_opt = {}
pos_opt = {}
seen_opt = []


def sell_option(contract, pos):
    msft_option_contract = contract
    ib.qualifyContracts(msft_option_contract)
    msft_option_order = MarketOrder('SELL', pos)
    msft_option_trade = ib.placeOrder(msft_option_contract, msft_option_order)



while True:
    for elt  in ib.positions(account='DU3424271'):
        try:
            ctr = elt.contract
            if elt.contract.secType =="STK":
                if ctr not in ticks.keys():
                    tic = ib.reqMktData(Option(ctr.symbol, ctr.lastTradeDateOrContractMonth, ctr.strike, ctr.right, 'SMART')) #
                    ticks_opt[ctr] = tic
                id = elt.contract.conId
                position = elt.position
                avg_cost = elt.avgCost
                avgs[ctr] = avg_cost
                pos[ctr] = position
                #print(id,position,avg_cost,elt)

            if elt.contract.secType =="OPT":
                if ctr not in ticks.keys():
                    tic = ib.reqMktData(Stock(ctr.symbol, 'SMART', 'USD'))
                    ticks[ctr] = tic
                id = elt.contract.conId
                position = elt.position
                avg_cost = elt.avgCost
                avgs[ctr] = avg_cost
                pos[ctr] = position
                #print(id,position,avg_cost,elt)
        except Exception as e:
            print("An error has occured: ", e)

    for i in range(int(position_update_frequency/price_update_frequency)):
        ib.sleep(price_update_frequency)
        for elt in ticks.keys():
            lst =  ticks[elt].last
            pnl = pos[elt]*(lst - avgs[elt])
            print(elt.symbol, ' Total positions: ',pos[elt]," Last price: ",ticks[elt].last," PNL: " ,pnl)

            if pnl < liquidation_treshhold and elt.symbol not in seen and elt.symbol not in white_list:
                print("      This is a loosing position , closing it now")
                contract = Stock(elt.symbol, 'SMART', 'USD')
                mktOrder = MarketOrder('SELL', pos[elt])
                limitTrade = ib.placeOrder(contract, mktOrder)
                seen.append(elt.symbol )

            elif pnl < liquidation_treshhold and elt.symbol not in seen and elt.symbol  in white_list:
                print("      This stock is white listed")

            elif pnl < liquidation_treshhold and elt.symbol in seen :
                print("      This position is already closed")

        for elt in ticks_opt.keys():
            lst =  ticks_opt[elt].last
            pnl = pos_opt[elt]*(lst - avgs[elt])
            print(elt.symbol, ' Total positions: ',pos[elt]," Last price: ",ticks_opt[elt].last," PNL: " ,pnl)

            if pnl < liquidation_treshhold_options and elt.symbol not in seen_opt and elt.symbol not in white_list:
                print("      This is a loosing position , closing it now")
                sell_option(elt,pos[elt])
                seen_opt.append(elt.symbol)

            elif pnl < liquidation_treshhold_options and elt.symbol not in seen_opt and elt.symbol  in white_list:
                print("      This stock is white listed")

            elif pnl < liquidation_treshhold_options and elt.symbol in seen_opt  :
                print("      This position is already closed")


        print("Checking again in 10 secs ")


