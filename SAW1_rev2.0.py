import numpy as np
import matplotlib.pyplot as plt
import random

def saw(n_steps):
    # Initialize the walk as a single point at the origin
    walk = np.zeros((1, 3))

    for i in range(n_steps):
        # Generate a random step in one of the six possible directions
        step = random.choice([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
        new_pos = walk[-1] + step

        # Check if the new position is already occupied by the walk
        if np.any((walk == new_pos).all(axis=1)):
            # If so, try again with a new step
            continue

        # Append the new position to the walk
        walk = np.vstack((walk, new_pos))

    return walk, i

def calculate_rg(positions):

    N = len(positions)
    r_cm = np.mean(positions, axis=0) # centro de masa
    Rg_sq = np.sum((positions - r_cm)**2) / N #Cuadrado del RG
    return np.sqrt(Rg_sq) #Regresamos solo la raiz cuadrada porque es el promedio

def graph(positions):

    N = len(positions)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = [step[0] for step in positions]
    y = [step[1] for step in positions]
    z = [step[2] for step in positions]
    ax.plot(x, y, z)
    plt.title("{:.2f} steps".format(N))
    plt.savefig("Self-avoiding Walk {:.2f}.pdf".format(N), format='pdf')
    plt.show()



N_list = [20, 50, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000] #DIstintos números de paso
#rev: aqui guardas los pasos reales que dio cada cadena
N_real = []

num_walks = len(N_list)
positions_list = []
for i in range(num_walks):
    positions, real_steps = saw(N_list[i])#aqui recibes los dos parametros
    positions_list.append(positions)
    N_real.append(real_steps)
    graph(positions)

#Calculo del Rg para cada caminata
Rg_list = []
for positions in positions_list:
    Rg = calculate_rg(positions)
    Rg_list.append(Rg)
    


# Gráfica loaritmica
plt.plot(N_real, Rg_list, '-o')
plt.xlabel('Number of steps')
plt.ylabel('Radius of gyration')
plt.xscale('log')
plt.yscale('log')
plt.title('Log-log plot of radius of gyration vs. number of steps')
plt.savefig("Loglog.pdf", format='pdf')
plt.show()

#Pendiente para ontener coefciente de Flory
log_N_list = np.log10(N_real)#real
log_Rg_list = np.log10(Rg_list)
slope, intercept = np.polyfit(log_N_list, log_Rg_list, 1)
print('Flory exponent: {:.2f}'.format(slope))