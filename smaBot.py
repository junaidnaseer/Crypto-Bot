from binance.client import Client
import math
import sys
import traceback

client = Client('',
                '')


def get_sma_klines(coin):
    try:
        klines15 = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "15 hours ago UTC")
        klines50 = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "50 hours ago UTC")
        klines16 = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "16 hours ago UTC")
        klines51 = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "51 hours ago UTC")

        sum_klines15 = 0
        sum_klines50 = 0
        sum_klines16 = 0
        sum_klines51 = 0

        for x in range(15):
            sum_klines15 += float(klines15[x][4])
        average15 = sum_klines15 / 15

        for x in range(50):
            sum_klines50 += float(klines50[x][4])
        average50 = sum_klines50 / 50

        for x in range(15):
            sum_klines16 += float(klines16[x][4])
        average16 = sum_klines16 / 15

        for x in range(50):
            sum_klines51 += float(klines51[x][4])
        average51 = sum_klines51 / 50

        averages = {'average15': average15, 'average50': average50, 'average16': average16, 'average51': average51}

        return averages
    except Exception as error:
        print str(error)
        tb = sys.exc_info()[-1]
        print(traceback.extract_tb(tb, limit=1)[-1][1])
        return False


def convert_coin(coin):
    usdt = client.get_asset_balance(asset='USDT')
    account25 = float(usdt['free']) * .25
    if len(coin) == 6:
        if coin[3:6] == 'BTC':
            currency_price = client.get_symbol_ticker(symbol='BTCUSDT')
            currency_amount = account25 / float(currency_price['price'])
            currency_amount = ((math.floor(currency_amount * 1000000)) / 1000000.0)
            try:
                client.create_order(
                    symbol='BTCUSDT',
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=currency_amount)
                print "bought " + str(currency_amount) + " BTC"
            except Exception as error:
                print str(error) + "(bought currency error)"
                pass
        if coin[3:6] == 'ETH':
            currency_price = client.get_symbol_ticker(symbol='ETHUSDT')
            currency_amount = account25 / float(currency_price['price'])
            currency_amount = ((math.floor(currency_amount * 100000)) / 100000.0)
            try:
                client.create_order(
                    symbol='ETHUSDT',
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=currency_amount)
                print "bought " + str(currency_amount) + " ETH"
            except Exception as error:
                print str(error) + "(bought currency error)"
                pass

        if coin[3:6] == 'BNB':
            currency_price = client.get_symbol_ticker(symbol='BNBUSDT')
            currency_amount = account25 / float(currency_price['price'])
            currency_amount = ((math.floor(currency_amount * 100)) / 100.0)
            try:
                client.create_order(
                    symbol='BNBUSDT',
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=currency_amount)
                print "bought " + str(currency_amount) + " BNB"
            except Exception as error:
                print str(error) + "(bought currency error)"
                pass


def buy_coin(coin):
    print "Attempting to buy " + coin
    usdt = None
    if type(coin) == str:
        if len(coin) == 6:
            if coin[3:6] == 'BTC':
                usdt = client.get_asset_balance(asset='BTC')
            if coin[3:6] == 'ETH':
                usdt = client.get_asset_balance(asset='ETH')
            if coin[3:6] == 'BNB':
                usdt = client.get_asset_balance(asset='BNB')
        coin_price = client.get_symbol_ticker(symbol=str(coin))
        account20 = float(usdt['free']) * .95
        coin_amount = account20/float(coin_price['price'])
        coin_min_amount = client.get_symbol_info(coin)
        if float(coin_min_amount['filters'][1]['minQty']) == 0.01000000:
            coin_amount = ((math.floor(coin_amount * 100)) / 100.0)
        elif float(coin_min_amount['filters'][1]['minQty']) == 1.00000000:
            coin_amount = math.floor(coin_amount)
        elif float(coin_min_amount['filters'][1]['minQty']) == 0.00001000:
            coin_amount = ((math.floor(coin_amount * 100000)) / 100000.0)
        elif float(coin_min_amount['filters'][1]['minQty']) == 0.00000100:
            coin_amount = ((math.floor(coin_amount * 1000000)) / 1000000.0)
        elif float(coin_min_amount['filters'][1]['minQty']) == 0.00100000:
            coin_amount = ((math.floor(coin_amount * 1000)) / 1000.0)
        convert_coin(coin)
        try:
            client.create_order(
                symbol=coin,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=coin_amount)
            print "Bought " + " " + str(coin)
        except Exception as error:
            print str(error) + "(bought error)"
            print coin_amount
            print len(coin)
            tb = sys.exc_info()[-1]
            print(traceback.extract_tb(tb, limit=1)[-1][1])
            pass


def sell_coin(coin):
    print coin
    if type(coin) == str:
        print 'attempting to sell ' + coin
        coin_info = client.get_asset_balance(asset=coin[0:3])
        if coin_info is not None:
            coin_info = client.get_asset_balance(asset=coin[0:4])
            if coin_info is not None:
                coin_info = client.get_asset_balance(asset=coin[0:5])
        amount = float(coin_info['free'])
        coin_min_amount = client.get_symbol_info(coin['symbol'])
        if float(coin_min_amount['filters'][1]['minQty']) == 0.01000000:
            amount = ((math.floor(amount * 100)) / 100.0)
        elif float(coin_min_amount['filters'][1]['minQty']) == 1.00000000:
            amount = math.floor(amount)
        elif float(coin_min_amount['filters'][1]['minQty']) == 0.00001000:
            amount = ((math.floor(amount * 100000)) / 100000.0)
        elif float(coin_min_amount['filters'][1]['minQty']) == 0.00000100:
            amount = ((math.floor(amount * 1000000)) / 1000000.0)
        elif float(coin_min_amount['filters'][1]['minQty']) == 0.00100000:
            amount = ((math.floor(amount * 1000)) / 1000.0)
        if amount > 0:
            try:
                client.create_order(
                    symbol=coin,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=amount)
                print "Sold " + " " + coin['symbol']
            except Exception as error:
                print str(error) + "(sold error)"
                pass
                return False
            else:
                print "didn't own coin"


def sma(coin):
    print 'Checking Simple Moving Averages'
    averages = get_sma_klines(coin)
    if averages is not None:
        return False
    if averages['average15'] < averages['average50'] and averages['average51'] < averages['average16']:
        return 'sell'
    if averages['average15'] > averages['average50'] and averages['average51'] > averages['average16']:
        return coin


def main():
    while True:
        print "STARTING BOT"
        prices = client.get_all_tickers()
        for price in prices:
            resultsma = sma(price['symbol'])
            if resultsma is not None:
                buy_coin(resultsma)
            if resultsma == 'sell':
                sell_coin(price['symbol'])


main()
