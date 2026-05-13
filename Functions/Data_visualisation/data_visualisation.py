from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec

path = Path('/media/gabriele/My Passport/MaLGait_sync_paper/user_00_sync/case_1')

imu_1 = pd.read_csv(path / "IMUs/imu_1_data_sync.csv")
# imu_0 = pd.read_csv(path / "IMUs/imu_0_data_sync.csv")

# imu_2 = pd.read_csv(path / "IMUs/imu_2_data_sync.csv")
imu_3 = pd.read_csv(path / "IMUs/imu_3_data_sync.csv")

# gravity_user = pd.read_csv(path / "User_Phone/Gravity_sync.csv")

fig = plt.figure(figsize = (20, 15))

fig.suptitle('Ankles IMU', fontsize = 30, y = 1)

gs = GridSpec(3, 3, figure = fig, hspace=0.6)

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_ylabel('$g_x$', fontsize = 15)
ax1.set_xlabel('$t$', fontsize = 15)
# ax1.set_ylim([-3.5, 2])
ax1.tick_params(axis = 'both', labelsize = 8)
ax1.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax1.transAxes,
         fontsize = 10)
ax1.text(0, 1, r'$[\frac{m}{s^2}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax1.transAxes,
         fontsize = 10)

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_ylabel('$g_y$', fontsize = 15)
ax2.set_xlabel('$t$', fontsize = 15)
# ax1.set_ylim([-3.5, 2])
ax2.tick_params(axis = 'both', labelsize = 8)
ax2.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax2.transAxes,
         fontsize = 10)
ax2.text(0, 1, r'$[\frac{m}{s^2}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax2.transAxes,
         fontsize = 10)

ax3 = fig.add_subplot(gs[0, 2])
ax3.set_ylabel('$g_z$', fontsize = 15)
ax3.set_xlabel('$t$', fontsize = 15)
# ax3.set_ylim([-3.5, 2])
ax3.tick_params(axis = 'both', labelsize = 8)
ax3.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax3.transAxes,
         fontsize = 10)
ax3.text(0, 1, r'$[\frac{m}{s^2}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax3.transAxes,
         fontsize = 10)


ax4 = fig.add_subplot(gs[1, 0])
ax4.set_ylabel('$a_x$', fontsize = 15)
ax4.set_xlabel('$t$', fontsize = 15)
# ax1.set_ylim([-3.5, 2])
ax4.tick_params(axis = 'both', labelsize = 8)
ax4.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax4.transAxes,
         fontsize = 10)
ax4.text(0, 1, r'$[\frac{m}{s^2}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax4.transAxes,
         fontsize = 10)

ax5 = fig.add_subplot(gs[1, 1])
ax5.set_ylabel('$a_y$', fontsize = 15)
ax5.set_xlabel('$t$', fontsize = 15)
# ax1.set_ylim([-3.5, 2])
ax5.tick_params(axis = 'both', labelsize = 8)
ax5.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax5.transAxes,
         fontsize = 10)
ax5.text(0, 1, r'$[\frac{m}{s^2}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax5.transAxes,
         fontsize = 10)

ax6 = fig.add_subplot(gs[1, 2])
ax6.set_ylabel('$a_z$', fontsize = 15)
ax6.set_xlabel('$t$', fontsize = 15)
# ax3.set_ylim([-3.5, 2])
ax6.tick_params(axis = 'both', labelsize = 8)
ax6.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax6.transAxes,
         fontsize = 10)
ax6.text(0, 1, r'$[\frac{m}{s^2}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax6.transAxes,
         fontsize = 10)


ax7 = fig.add_subplot(gs[2, 0])
ax7.set_ylabel(r'$\omega_x$', fontsize = 15)
ax7.set_xlabel('$t$', fontsize = 15)
# ax1.set_ylim([-3.5, 2])
ax7.tick_params(axis = 'both', labelsize = 8)
ax7.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax7.transAxes,
         fontsize = 10)
ax7.text(0, 1, r'$[\frac{rad}{s}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax7.transAxes,
         fontsize = 10)

ax8 = fig.add_subplot(gs[2, 1])
ax8.set_ylabel(r'$\omega_y$', fontsize = 15)
ax8.set_xlabel('$t$', fontsize = 15)
# ax1.set_ylim([-3.5, 2])
ax8.tick_params(axis = 'both', labelsize = 8)
ax8.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax8.transAxes,
         fontsize = 10)
ax8.text(0, 1, r'$[\frac{rad}{s}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax8.transAxes,
         fontsize = 10)

ax9 = fig.add_subplot(gs[2, 2])
ax9.set_ylabel(r'$\omega_z$', fontsize = 15)
ax9.set_xlabel('$t$', fontsize = 15)
# ax3.set_ylim([-3.5, 2])
ax9.tick_params(axis = 'both', labelsize = 8)
ax9.text(1, 0, '$[ms]$', 
         horizontalalignment = 'left', 
         verticalalignment = 'top', 
         transform = ax9.transAxes,
         fontsize = 10)
ax9.text(0, 1, r'$[\frac{rad}{s}]$', 
         horizontalalignment = 'right', 
         verticalalignment = 'bottom', 
         transform = ax9.transAxes,
         fontsize = 10)



ax2.set_title("Gravity", fontsize=20, pad=20)
ax5.set_title("Acceleration", fontsize=20, pad=20)
ax8.set_title("Angular Velocity", fontsize=20, pad=20)



start = 1000
end = 1200

# print(acc)

t = imu_1["time_ms_loc"][start:end]

markersize = 2
linewidth = 0.5

ax1.plot(t, imu_3["gx"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax1.plot(t, imu_1["gx"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax1.legend()

ax2.plot(t, imu_3["gy"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax2.plot(t, imu_1["gy"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax2.legend()

ax3.plot(t, imu_3["gz"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax3.plot(t, imu_1["gz"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax3.legend()

ax4.plot(t, imu_3["ax"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax4.plot(t, imu_1["ax"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax4.legend()

ax5.plot(t, imu_3["ay"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax5.plot(t, imu_1["ay"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax5.legend()

ax6.plot(t, imu_3["az"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax6.plot(t, imu_1["az"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax6.legend()

ax7.plot(t, imu_3["wx"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax7.plot(t, imu_1["wx"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax7.legend()

ax8.plot(t, imu_3["wy"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax8.plot(t, imu_1["wy"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax8.legend()

ax9.plot(t, imu_3["wz"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "right")
ax9.plot(t, imu_1["wz"][start:end], '-o', markersize = markersize, linewidth = linewidth, label = "left")
ax9.legend()

plt.savefig("./plot.png")
plt.show()

