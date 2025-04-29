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

# === Выделенная точка и её проекции ===
p_i = 0.35
T_i = 1400
c_i = 0.6
f_i = p_i * np.log(T_i) * (1 - c_i)

# Точка
ax.scatter(p_i, T_i, c_i, color='red', s=80)

# Проекции на оси (пунктирные линии)
ax.plot([p_i, p_i], [T_i, T_i], [0, c_i], 'r--', linewidth=1)
ax.plot([p_i, p_i], [T_vals.min(), T_i], [c_i, c_i], 'r--', linewidth=1)
ax.plot([p_vals.min(), p_i], [T_i, T_i], [c_i, c_i], 'r--', linewidth=1)

plt.tight_layout()
plt.show()
