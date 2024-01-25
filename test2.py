from time import sleep
from test import SymbolInfo, LimitOrderPosition, CreateOrder

SYMBOL = 'SUIUSDT'
QU_DOLLARS = 20


def main():
    while True:
        if trade_work.balance_on_position()[1] > QU_DOLLARS*-0.5:
            sleep(2)
            if trade_work.open_quantity_position() < 2:
                sleep(10)
                create_order.delete_orders()
                create_order.create_order_long(trade_work_position.quantity_order_long(),
                                               trade_work_position.limit_order_long())
                create_order.create_order_short(trade_work_position.quantity_order_short(),
                                                trade_work_position.limit_order_short())
            else:
                pass

        else:
            pass


if __name__ == "__main__":
    trade_work = SymbolInfo(SYMBOL)
    trade_work_position = LimitOrderPosition(SYMBOL, QU_DOLLARS)
    create_order = CreateOrder(SYMBOL)
    main()
