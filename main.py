from time import sleep

from bot import send_message
from logic import SymbolInfo, LimitOrderPosition, CreateOrder


def main(symbol, quant):
    while True:
        try:
            if SymbolInfo(symbol).balance_on_position()[1] > quant * -2:
                sleep(2)
                if SymbolInfo(symbol).open_quantity_position() < 2:
                    sleep(60)
                    work = LimitOrderPosition(symbol, quant)
                    send_message(f"Last limit order: {SymbolInfo(symbol).last_open_limit_order()}")
                    create_order = CreateOrder(symbol)
                    create_order.delete_orders()
                    create_order.create_order_long(work.quantity_order_long(),
                                                   work.limit_order_long())
                    create_order.create_order_short(work.quantity_order_short(),
                                                    work.limit_order_short())
                    send_message(f"Balance: {SymbolInfo(symbol).balance_on_position()}")
            else:
                CreateOrder(symbol).close_position()
        except Exception as e:
            send_message(e)
            print(e)


if __name__ == "__main__":
    main('1000PEPEUSDT', 100)
