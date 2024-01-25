from time import sleep
from test import SymbolInfo, LimitOrderPosition, CreateOrder

SYMBOL = 'SUIUSDT'
QU_DOLLARS = 30


def main():
    while True:
        if trade_work.balance_on_position()[1] > QU_DOLLARS*-2:
            sleep(2)
            price_test = trade_work.last_open_limit_order()
            print(price_test, '1')
            if trade_work.open_quantity_position() < 2:
                sleep(2)
                create_order.delete_orders()
                price_test = trade_work.last_open_limit_order()
                print(price_test, '2')
                create_order.create_order_long()
            else:
                pass

        else:
            pass


if __name__ == "__main__":
    trade_work = SymbolInfo(SYMBOL)
    trade_work_position = LimitOrderPosition(SYMBOL, QU_DOLLARS)
    create_order = CreateOrder(SYMBOL)
    main()
