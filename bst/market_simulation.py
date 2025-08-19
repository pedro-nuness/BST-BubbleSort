import time
import random
from order_book import OrderBookBST

def place_orders(running, lock, bids, asks, price_history):
    while running.is_set():
        time.sleep(random.uniform(0.5, 2.0))

        with lock:        
            if not price_history:
                continue
            last_price = price_history[-1]
            if random.random() > 0.5:
                bid_price = round(last_price - random.uniform(0.1, 2.5), 2)
                if bid_price < last_price:
                    bids.insert(bid_price, random.randint(5, 30))
                    print(f"Nova Ordem de Compra: {bid_price}")
            else:
                ask_price = round(last_price + random.uniform(0.1, 2.5), 2)
                if ask_price > last_price:
                    asks.insert(ask_price, random.randint(5, 30))
                    print(f"Nova Ordem de Venda: {ask_price}")

def capture_data(running, lock, bids, asks, price_history):
    initial_price = 150.0
    with lock:
        price_history.append(initial_price)
        for i in range(15):
            bids.insert(round(initial_price - random.uniform(0.1, 5.0), 2), random.randint(5, 50))
            asks.insert(round(initial_price + random.uniform(0.1, 5.0), 2), random.randint(5, 50))

    while running.is_set():
        price = round(random.uniform(140, 160), 2)
        print(f"Preço de Mercado Atual: {price:.2f}")

        with lock:
            bids_executed = [p for p, q in bids.inorder() if p >= price]
            for bid_price in bids_executed:
                print(f"EXECUÇÃO DE COMPRA! Ordem a ${bid_price:.2f} foi executada pelo preço de mercado ${price:.2f}.")
                bids.remove(bid_price)

            asks_executed = [p for p, q in asks.inorder() if p <= price]
            for ask_price in asks_executed:
                print(f"EXECUÇÃO DE VENDA! Ordem a ${ask_price:.2f} foi executada pelo preço de mercado ${price:.2f}.")
                asks.remove(ask_price)

            if not price_history or price != price_history[-1]:
                price_history.append(price)
            while len(price_history) > 30:
                price_history.pop(0)
        
        time.sleep(3)
