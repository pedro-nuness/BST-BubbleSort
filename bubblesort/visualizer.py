import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SortVisualizer:
    def __init__(self, result_map):
        self.result_map = result_map
        self.players = list(result_map.keys())

        self.root = tk.Tk()
        self.root.title("Bubble Sort & Match Stats")

        self.fig, self.axes = plt.subplots(2, 1, figsize=(12, 12), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.animation_data = list(zip(self.players, [self.result_map[p]["points_earned"] for p in self.players]))
        self.n = len(self.animation_data)
        
        self.current_i = 0
        self.current_j = 0
        self.swapped_in_pass = False
        self.animation_delay = 50

        self.bar_container = None
        self.background = None 

    def _initial_draw_ranking(self):
        ax = self.axes[0]
        names = [p.nickname for p, _ in self.animation_data]
        points = [pts for _, pts in self.animation_data]
        
        self.bar_container = ax.bar(names, points, color='skyblue', animated=True)

        ax.set_ylabel('Points Gained')
        ax.set_title('Ranking (Bubble Sort Animation)')
        if points:
            ax.set_ylim(0, max(points) * 1.15)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
    
    def _final_draw_ranking(self):
        ax = self.axes[0]

        for bar in self.bar_container:
            bar.set_animated(False)

        names = [p.nickname for p, _ in self.animation_data]
        points = [pts for _, pts in self.animation_data]
        colors = ['gold' if i == 0 else 'silver' if i == 1 else '#cd7f32' if i == 2 else 'skyblue' for i in range(len(self.animation_data))]
        for i, bar in enumerate(self.bar_container):
            bar.set_height(points[i])
            bar.set_color(colors[i])
        
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45)
        
        self.canvas.draw()

    def _draw_stats(self):
        ax = self.axes[1]
        sorted_players = sorted(self.players, key=lambda p: p.nickname)
        names = [p.nickname for p in sorted_players]
        kills = [self.result_map[p]["kills"] for p in sorted_players]
        assists = [self.result_map[p]["assists"] for p in sorted_players]
        deaths = [self.result_map[p]["deaths"] for p in sorted_players]
        damage = [self.result_map[p]["damage"] for p in sorted_players]
        bar_width, index = 0.2, list(range(len(sorted_players)))
        ax.bar([i - bar_width for i in index], kills, width=bar_width, label='Kills', color='green')
        ax.bar(index, assists, width=bar_width, label='Assists', color='blue')
        ax.bar([i + bar_width for i in index], deaths, width=bar_width, label='Deaths', color='red')
        ax.set_ylabel('Count')
        ax.set_xticks(index)
        ax.set_xticklabels(names, rotation=45, ha="right")
        ax.set_title('Detailed Player Stats')
        ax.legend(loc='upper left')
        ax2 = ax.twinx()
        ax2.plot(names, damage, label='Damage', color='orange', marker='o', linewidth=2)
        ax2.set_ylabel('Damage Dealt')
        ax2.legend(loc='upper right')

    def _animate_sort_step(self):
        if self.current_i >= self.n - 1:
            print("Sorting complete!")
            self._final_draw_ranking()
            return
        
        ax = self.axes[0]
        self.canvas.restore_region(self.background)

        if self.current_j < self.n - self.current_i - 1:
            if self.animation_data[self.current_j][1] < self.animation_data[self.current_j + 1][1]:
                self.animation_data[self.current_j], self.animation_data[self.current_j + 1] = self.animation_data[self.current_j + 1], self.animation_data[self.current_j]
                self.swapped_in_pass = True

            names = [p.nickname for p, _ in self.animation_data]
            points = [pts for _, pts in self.animation_data]
            colors = ['skyblue'] * self.n
            colors[self.current_j] = 'red'
            colors[self.current_j + 1] = 'red'
            
            for i, bar in enumerate(self.bar_container):
                bar.set_height(points[i])
                bar.set_color(colors[i])
                ax.draw_artist(bar) 

            ax.set_xticks(range(len(names)))
            xticklabels = ax.set_xticklabels(names, rotation=45, ha="right")
            for label in xticklabels:
                ax.draw_artist(label)

            self.canvas.blit(ax.bbox)
            self.canvas.flush_events()
            
            self.current_j += 1
        else:
            if not self.swapped_in_pass:
                self.current_i = self.n
            else:
                self.current_i += 1
                self.current_j = 0
                self.swapped_in_pass = False

        self.root.after(self.animation_delay, self._animate_sort_step)

    def run(self):
        self._draw_stats()
        self._initial_draw_ranking()
        
        self.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.axes[0].bbox)

        self.root.after(1000, self._animate_sort_step)
        self.root.mainloop()