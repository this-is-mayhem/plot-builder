# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import rcParams
#
# rcParams['font.family'] = 'serif'
# rcParams['font.serif'] = 'Times New Roman'
# rcParams["mathtext.fontset"] = 'stix'
#
# # Обновлённые диапазоны
# p_vals = np.linspace(0.1, 1.0, 10)
# T_vals = np.linspace(500, 2000, 10)
# c_vals = np.linspace(0.0, 1.0, 5)
#
# # Построение сетки
# P, T, C = np.meshgrid(p_vals, T_vals, c_vals, indexing='ij')
# points = np.vstack([P.ravel(), T.ravel(), C.ravel()]).T
#
# # Примерная функция f
# f_vals = points[:, 0] * np.log(points[:, 1]) * (1 - points[:, 2])
#
# # Построение scatter
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
#
# sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=f_vals, cmap='viridis', s=20)
#
# # Устанавливаем тики на осях
# ax.set_xticks(p_vals)
#
# # На ось T ставим, например, 5 подписей
# num_ticks_T = 5
# T_ticks = np.linspace(T_vals.min(), T_vals.max(), num_ticks_T)
# ax.set_yticks(T_ticks)
#
# ax.set_zticks(c_vals)
#
# # Названия осей
# ax.set_xlabel('$p$, МПа', fontsize=16, labelpad=15)
# ax.set_ylabel('$T$, К', fontsize=16, labelpad=15)
# ax.set_zlabel('$c$', fontsize=16, labelpad=15)
#
# # Размер чисел-меток на осях
# ax.tick_params(axis='both', labelsize=16)
# ax.tick_params(axis='z', labelsize=16)
#
# # === Выделенная точка и её проекции ===
# p_i = 0.35
# T_i = 1400
# c_i = 0.6
# f_i = p_i * np.log(T_i) * (1 - c_i)
#
# # Точка
# ax.scatter(p_i, T_i, c_i, color='red', s=80)
#
# # Проекции на оси (пунктирные линии)
# ax.plot([p_i, p_i], [T_i, T_i], [0, c_i], 'r--', linewidth=1)
# ax.plot([p_i, p_i], [T_vals.min(), T_i], [c_i, c_i], 'r--', linewidth=1)
# ax.plot([p_vals.min(), p_i], [T_i, T_i], [c_i, c_i], 'r--', linewidth=1)
#
# plt.tight_layout()
# ax.view_init(elev=7, azim=-65)
# plt.savefig("3d_scatter.png", dpi=600)
# # plt.show()

#############################################################################
###################### 2D плоскости p-c и p-T ###############################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams["mathtext.fontset"] = 'stix'

# Диапазоны переменных
p_vals = np.arange(0.1, 1.01, 0.1)
T_vals = np.linspace(500, 2000, 10)
c_vals = np.linspace(0.0, 1.0, 5)

# Плоскость p–c при фиксированном T
T_fixed = 1400
P_pc, C_pc = np.meshgrid(p_vals, c_vals, indexing='ij')
f_pc = P_pc * np.log(T_fixed) * (1 - C_pc)

# Плоскость p–T при фиксированном c
c_fixed = 0.6
P_pT, T_pT = np.meshgrid(p_vals, T_vals, indexing='ij')
f_pT = P_pT * np.log(T_pT) * (1 - c_fixed)

# Красные точки
p0_pc, c0_pc = 0.35, 0.6
p0_pT, T0_pT = 0.35, 1400

# Тики по p
p_ticks = np.arange(0, 1.1, 0.2)

# Создание графиков
figure_size = [16, 6]
cm = 1 / 2.54  # перевод сантиметров в дюймы для установки размера картинки
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(figure_size[0] * cm, figure_size[1] * cm))

# --- График p–c ---
ax1.scatter(P_pc.ravel(), C_pc.ravel(), c=f_pc.ravel(), cmap='viridis', s=40)
ax1.scatter(p0_pc, c0_pc, color='red', s=70)
ax1.axhline(c0_pc, color='gray', linestyle='--', linewidth=1)
ax1.axvline(p0_pc, color='gray', linestyle='--', linewidth=1)
ax1.set_xticks(p_ticks)
ax1.set_xlabel('$p$, МПа', fontsize=14)
ax1.set_ylabel('$c$', fontsize=14)
ax1.set_title(f'$T = {T_fixed}$ K', fontsize=14)
ax1.tick_params(labelsize=12)

# --- График p–T ---
ax2.scatter(P_pT.ravel(), T_pT.ravel(), c=f_pT.ravel(), cmap='viridis', s=40)
ax2.scatter(p0_pT, T0_pT, color='red', s=70)
ax2.axhline(T0_pT, color='gray', linestyle='--', linewidth=1)
ax2.axvline(p0_pT, color='gray', linestyle='--', linewidth=1)
ax2.set_xticks(p_ticks)
ax2.set_xlabel('$p$, МПа', fontsize=14)
ax2.set_ylabel('$T$, K', fontsize=14)
ax2.set_title(f'$c = {c_fixed}$', fontsize=14)
ax2.tick_params(labelsize=12)

plt.tight_layout()
plt.savefig("2d_scatter.png", dpi=600)


# plt.show()
