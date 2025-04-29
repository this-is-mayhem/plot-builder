import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams["mathtext.fontset"] = 'stix'

# Обновлённые диапазоны
p_vals = np.linspace(0.1, 1.0, 10)
T_vals = np.linspace(500, 2000, 10)
c_vals = np.linspace(0.0, 1.0, 5)

# Построение сетки
P, T, C = np.meshgrid(p_vals, T_vals, c_vals, indexing='ij')
points = np.vstack([P.ravel(), T.ravel(), C.ravel()]).T

# Примерная функция f
f_vals = points[:, 0] * np.log(points[:, 1]) * (1 - points[:, 2])

# Построение scatter
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=f_vals, cmap='viridis', s=20)

# Устанавливаем тики на осях
ax.set_xticks(p_vals)

# На ось T ставим, например, 5 подписей
num_ticks_T = 5
T_ticks = np.linspace(T_vals.min(), T_vals.max(), num_ticks_T)
ax.set_yticks(T_ticks)

ax.set_zticks(c_vals)

# Названия осей
ax.set_xlabel('$p$, МПа', fontsize=16, labelpad=15)
ax.set_ylabel('$T$, К', fontsize=16, labelpad=15)
ax.set_zlabel('$c$', fontsize=16, labelpad=15)

# Размер чисел-меток на осях
ax.tick_params(axis='both', labelsize=16)
ax.tick_params(axis='z', labelsize=16)

plt.tight_layout()
ax.view_init(elev=6, azim=-55)
plt.savefig("kdtree.png", dpi=600)
# plt.show()
