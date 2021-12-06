from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)

	def tickPrice(self, reqId, tickType, price, attrib):
		if tickType == 2 and reqId == 1:
			print('The current ask price is: ', price)

	def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
		print("TickNews. TickerId:", tickerId, "TimeStamp:", timeStamp,"ProviderCode:", providerCode, "ArticleId:", articleId,"Headline:", headline, "ExtraData:", extraData)

	def pnL(self, reqId: int, dailyPnL: float,unrealizedPnL: float, realizedPnL: float):
		super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
		print("Daily PnL. ReqId:", reqId, "DailyPnL:", dailyPnL,"UnrealizedPnL:", unrealizedPnL, "RealizedPnL:", realizedPnL)

	def position(self, account: str, contract: Contract, position: float,avgCost: float):
		super().position(account, contract, position, avgCost)

		print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
		contract.secType, "Currency:", contract.currency,"Position:", float, "Avg cost:", avgCost)

app = IBapi()
app.connect('127.0.0.1', 7496, 1)

#aux = app.reqPnL(1002, "U5423433", "")
aux= app.reqPositions()
time.sleep(2)

app.run()
#app.reqMarketDataType(4)
