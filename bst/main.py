# main.py

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import threading
import time
from order_book import OrderBookBST
from market_simulation import capture_data, place_orders

def plot_glow_line(ax, x, y, color, base_linewidth=2, num_layers=5, label=None):
    for i in range(num_layers, 0, -1):
        ax.plot(x, y, color=color, linewidth=base_linewidth + i * 1.5, alpha=0.05 * (num_layers - i + 1), solid_capstyle='round')
    ax.plot(x, y, color=color, linewidth=base_linewidth, alpha=0.8, solid_capstyle='round', label=label)

def main():
    bids = OrderBookBST()
    asks = OrderBookBST()
    price_history = []
    lock = threading.Lock()
    running = threading.Event()
    running.set() 

    print("Observando o mercado simulado em tempo real... (Ctrl+C para parar)")


    t1 = threading.Thread(target=capture_data, args=(running, lock, bids, asks, price_history), daemon=True)
    t2 = threading.Thread(target=place_orders, args=(running, lock, bids, asks, price_history), daemon=True)
    t1.start()
    t2.start()

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.set_facecolor('#101010')
    ax.set_facecolor('#181818')
    plt.ion()

    try:
        while running.is_set():
            with lock:
                bid_book = bids.inorder()
                ask_book = asks.inorder()
                prices = list(price_history)

            if len(prices) > 1:
                ax.clear()

                current_price = prices[-1]
                previous_price = prices[-2]
                price_change = current_price - previous_price
                
                time_axis = range(len(prices))
                current_time_idx = time_axis[-1]

                all_quantities = [q for p, q in bid_book] + [q for p, q in ask_book]
                max_quantity = max(all_quantities) if all_quantities else 1
                quantity_scale_factor = 7 

                ax.set_facecolor('#181818')
                for spine in ax.spines.values():
                    spine.set_color('#404040')
                ax.tick_params(axis='x', colors='silver')
                ax.tick_params(axis='y', colors='silver')
                ax.grid(True, color='#404040', linestyle='--', linewidth=0.5, alpha=0.5)

                for price, quantity in bid_book:
                    scaled_length = (quantity / max_quantity) * quantity_scale_factor
                    ax.plot([current_time_idx - scaled_length, current_time_idx], [price, price], 
                            color='#00ff55', linewidth=1.5, alpha=0.7, solid_capstyle='round')

                for price, quantity in ask_book:
                    scaled_length = (quantity / max_quantity) * quantity_scale_factor
                    ax.plot([current_time_idx, current_time_idx + scaled_length], [price, price], 
                            color='#ff2255', linewidth=1.5, alpha=0.7, solid_capstyle='round')
                    
                plot_glow_line(ax, time_axis, prices, color='#00bbff')
                ax.fill_between(time_axis, prices, color="#ffffff", alpha=0.05)

                change_char = "▲" if price_change > 0 else "▼" if price_change < 0 else "▬"
                color_char = 'lime' if price_change > 0 else 'red' if price_change < 0 else 'gray'
                
                title_text = f"AAPL: ${current_price:.2f} "
                ax.set_title(title_text, fontsize=18, color='white', loc='left', pad=20) # Aumenta o padding
                ax.text(0.35, 1.01, f"{change_char} ${price_change:+.2f}", 
                        transform=ax.transAxes, fontsize=18, color=color_char, ha='left')

                ax.set_xlabel("Tempo (Capturas Recentes)", color='silver')
                ax.set_ylabel("Preço ($)", color='silver')
            
                y_min = min(p for p, q in bid_book) if bid_book else current_price - 1
                y_max = max(p for p, q in ask_book) if ask_book else current_price + 1
                ax.set_ylim(y_min - 0.5, y_max + 0.5)
                ax.set_xlim(left=max(-10, current_time_idx - 20), right=current_time_idx + 10)

                legend_elements = [
                    mlines.Line2D([], [], color='#00bbff', marker='_', markersize=15, label='Histórico de Preço'),
                    mlines.Line2D([], [], color='#00ff55', marker='_', markersize=15, label='Ordens de Compra (Bids)'),
                    mlines.Line2D([], [], color='#ff2255', marker='_', markersize=15, label='Ordens de Venda (Asks)')
                ]
                ax.legend(handles=legend_elements, loc='upper right', frameon=True, facecolor='#2a2a2a', edgecolor='#404040', labelcolor='white')


                plt.tight_layout(pad=1.5)
                plt.pause(0.1)
            else:
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        running.clear()
        t1.join()
        t2.join()
        plt.ioff()
        plt.close()
        print("Aplicação encerrada.")

if __name__ == "__main__":
    main()
