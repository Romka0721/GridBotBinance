import asyncio


from API import API_KEY, API_SEKRET
from binance.client import Client



client = Client(API_KEY, API_SEKRET)


#================================
symbol = '1000PEPEUSDT'
quantity_dollars = 30
round_price = 7
#================================


async def price_symbol(symbol):
    price_symbol = client.futures_mark_price(symbol=symbol)
    price_symbol = float(price_symbol['markPrice'])
    print('Ціна: ', price_symbol)
    return price_symbol

#Останній лімітний ордер
async def last_limit_order(symbol):
    trades = client.futures_account_trades(symbol=symbol)
    last_trade = float(trades[-1]['price'])
    print(last_trade)
    return last_trade


# Обчислення загального балансу в позиції
async def balans_open_positions(symbol):
    open_positions = client.futures_position_information(symbol=symbol)
    for position in open_positions:
        balans_open = float(position['positionAmt'])
    balans_open = round(balans_open * await price_symbol(symbol), 1)
    print('Баланс в позиції: ',balans_open)
    return balans_open


#Визначання збитку в позиції
async def position_on(symbol):
    positions = client.futures_position_information(symbol=symbol)
    position = positions[0]
    entry_price = float(position['entryPrice'])
    mark_price = float(position['markPrice'])
    quantity = float(position['positionAmt'])
    profit = round((mark_price - entry_price) * quantity, round_price)
    print('Прибуток/Збиток в позиції: ', profit)
    return profit

# Визначаємо кількість у позиції long
async def quantity_long(quantity_dollars):
    # balans = balans_open_positions(symbol)
    last_order_long = await last_limit_order(symbol)
    quantity_dollars_long = round(quantity_dollars/last_order_long)

    # if balans > quantity_dollars*2.1:
    #     quantity_long = round(10/last_order_long)
    # elif balans > quantity_dollars*1.1:
    #     quantity_long = round((quantity_dollars*0.6)/last_order_long)
    # else:
    #     quantity_long = quantity_t
    print('Кількість знизу: ',quantity_dollars_long)
    return quantity_dollars_long


# Визначаємо де будуть стояти лімітки long
async def limit_order_long_1():
    last_limit_order_min = await last_limit_order(symbol)

    limit_order_long1 = round(last_limit_order_min - (last_limit_order_min*0.03), round_price)
    print('Лімітка знизу: ',limit_order_long1)
    return limit_order_long1

async def limit_order_long_2():
    last_limit_order_min = await last_limit_order(symbol)

    limit_order_long1 = round(last_limit_order_min - (last_limit_order_min*0.06), round_price)
    print('Лімітка знизу: ',limit_order_long1)
    return limit_order_long1

async def on_position_long(symbol):
    position_long = client.futures_get_open_orders(symbol=symbol, side='BUY')
    a = 0
    for position in position_long:
        position_side = position['side']
        if position_side == 'BUY':
            a += 1
    print('Поставлено ліміток: ', a)
    return a

async def create_order_1():
    client.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    quantity=await quantity_long(quantity_dollars),
                    price=await limit_order_long_1(),
                    timeInForce='GTC'
                )

async def create_order_2():
    client.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    quantity=await quantity_long(quantity_dollars),
                    price=await limit_order_long_2(),
                    timeInForce='GTC'
                )
async def work_long(symbol):
    while True:
        if await on_position_long(symbol) < 1:
            await create_order_1()
            if await on_position_long(symbol) < 2:
                await create_order_2()


def work_short():
    pass


async def main():
    await work_long(symbol)
    # await price_symbol(symbol)
    # await last_limit_order(symbol)
    # await balans_open_positions(symbol)
    # await position_on(symbol)
    # await quantity_long(quantity_dollars)
    # await limit_order_long()
    # await on_position_long(symbol)

if __name__ == "__main__":
    asyncio.run(main())