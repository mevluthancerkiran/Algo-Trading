import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime
from poloniex import Poloniex
polo = Poloniex()


def t_trade():

    cur_btc = 10
    cur_usdt = 10000

    print(
        "\n" + "\n" + "    ********************************************- ALGORITHMIC TRADING -********************************************" + "\n" + "\n"
        + "                                                                                      by MEVLÜT HANÇERKIRAN" + "\n" + "\n" + "\n")
    print(
        "\n" + "                                        INITIAL BTC: 10" + "          INITIAL USDT: 10000" + "\n" + "\n" + "  -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-" + "\n")
    final_df = pd.DataFrame(
        data={"Date": [0 for rrr in range(719) ],
              "Current Value": [0 for rrr in range(719) ],
              "Up": [0 for rrr in range(719) ],
              "Mean": [0 for rrr in range(719) ],
              "Low": [0 for rrr in range(719) ],
              "   Decision": [0 for rrr in range(719) ],
              "Current BTC": [0 for rrr in range(719) ],
              "Current USDT": [0 for rrr in range(719) ]})
    for xyz in range(719):

        base = "https://api.btcturk.com"
        method = "/api/v2/ticker?pairSymbol=BTC_TRY"
        uri = base + method
        result = requests.get(url=uri)
        result = result.json()



        unix_time = result["data"][0]["timestamp"] / 1000
        real_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


        tim_dif = 1601520208 - 1599696000

        return_price = polo.returnChartData("USDT_BTC", period=300, start=int((unix_time - tim_dif)), end=int(unix_time))
        cur_value = polo.returnTicker()['USDT_BTC']["last"]


        close_values = [(return_price[rrr]["weightedAverage"]) for rrr in range(5751)]


        close_values = np.array(close_values)

        boll_mean = close_values.mean()
        boll_std = close_values.std()
        boll_up = boll_mean + (boll_std * 2)
        boll_low = boll_mean - (boll_std * 2)


        if (final_df.iloc[max(xyz-1,0),1]>final_df.iloc[max(xyz-1,0),2]) and (cur_value<boll_up):
            fin_dec = "SELL"
            if cur_btc != 0:
                cur_usdt = cur_btc * cur_value
                cur_btc = 0


        elif (final_df.iloc[max(xyz-1,0),1]<final_df.iloc[max(xyz-1,0),4]) and (cur_value>boll_low):
            fin_dec = "BUY"
            if cur_usdt != 0:
                cur_btc = cur_usdt / cur_value
                cur_usdt = 0
        else:
            fin_dec = "NONE"

        final_df.iloc[xyz] = [real_date, cur_value, boll_up, boll_mean, boll_low, fin_dec, cur_btc, cur_usdt]
        print(final_df.loc[[xyz]])
        print(
            "\n" + "  -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
        time.sleep(15.1)

    print("\n" + "                                                         ...FINISH..." +
          "\n" +
          "                                             FINAL BTC: " + str(cur_btc) + "          FINAL USDT: " + str(cur_usdt))
    time.sleep(60)


t_trade()
