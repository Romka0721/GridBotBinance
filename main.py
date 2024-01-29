from time import sleep
from logic import SymbolInfo, LimitOrderPosition, CreateOrder


def main(symbol, quant):
    while True:
        try:
            if SymbolInfo(symbol).balance_on_position()[1] > quant*-2:
                sleep(5)
                if SymbolInfo(symbol).open_quantity_position() < 2:
                    sleep(120)
                    work = LimitOrderPosition(symbol, quant)
                    create_order = CreateOrder(symbol)
                    create_order.delete_orders()
                    create_order.create_order_long(work.quantity_order_long(),
                                                   work.limit_order_long())
                    create_order.create_order_short(work.quantity_order_short(),
                                                    work.limit_order_short())
                else:
                    pass

            else:
                CreateOrder(symbol).close_position()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main('SUIUSDT', 20)
