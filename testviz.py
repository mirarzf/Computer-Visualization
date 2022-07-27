import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# ax.broken_barh([(110, 30), (150, 10)], (13, 4), facecolors='tab:blue')
ax.broken_barh([(10, 50), (100, 20), (130, 10)], 
                (3, 1), 
                facecolors=('tab:orange', 'tab:green', 'tab:red'))
# ax.set_ylim(5, 35)
ax.set_ylim(3,4)
ax.set_xlim(0, 200)
ax.set_xlabel('seconds since start')
ax.set_yticks([], labels = [])
# ax.set_xticks(list(range(0,200,5)), labels = [])
# ax.set_yticks([15, 25], labels=['Bill', 'Jim'])
# ax.axis("off")
# ax.grid(True)
ax.annotate('race interrupted', (61, 25),
            xytext=(0.8, 0.9), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            fontsize=16,
            horizontalalignment='right', verticalalignment='top')

plt.show()