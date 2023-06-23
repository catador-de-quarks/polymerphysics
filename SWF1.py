import numpy as np
import matplotlib.pyplot as plt
import random

def random_walk_3D(num_steps):

    x, y, z = 0, 0, 0

    coords = np.zeros((num_steps+1, 3))
    coords[0] = [x, y, z]

    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    for i in range(num_steps):

        dx, dy, dz = random.choice(directions)
        x += dx
        y += dy
        z += dz

        coords[i+1] = [x, y, z]

    x = [step[0] for step in coords]
    y = [step[1] for step in coords]
    z = [step[2] for step in coords]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x,y,z)
    plt.title("{:.2f} steps".format(num_steps))
    plt.savefig("RandomWalk {:.2f}.pdf".format(num_steps), format='pdf')
    plt.show()

    return coords

def calculate_rg(positions):

    N = len(positions)
    r_cm = np.mean(positions, axis=0) # centro de masa
    Rg_sq = np.sum((positions - r_cm)**2) / N #Cuadrado del RG
    return np.sqrt(Rg_sq) #Regresamos solo la raiz cuadrada porque es el promedio

N_list = [5, 10, 20, 50, 100, 200, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000] #DIstintos números de paso
num_walks = len(N_list)
positions_list = []
for i in range(num_walks):
    positions = random_walk_3D(N_list[i])
    positions_list.append(positions)

#Calculo del Rg para cada caminata
Rg_list = []
for positions in positions_list:
    Rg = calculate_rg(positions)
    Rg_list.append(Rg)

# Gráfica loaritmica
plt.plot(N_list, Rg_list, '-o')
plt.xlabel('Number of steps')
plt.ylabel('Radius of gyration')
plt.xscale('log')
plt.yscale('log')
plt.title('Log-log plot of radius of gyration vs. number of steps')
plt.savefig("Loglog.pdf", format='pdf')
plt.show()

#Pendiente para ontener coefciente de Flory
log_N_list = np.log10(N_list)
log_Rg_list = np.log10(Rg_list)
slope, intercept = np.polyfit(log_N_list, log_Rg_list, 1)
print('Flory exponent: {:.2f}'.format(slope))
