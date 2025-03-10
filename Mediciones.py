# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:47:40 2025

@author: Publico
"""

import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
#%%

#p = float(input("presión [Torr]"))
#d = float(input("distancia [cm]"))
#pede = p*d


per = 100 #[s]
#%%
rm = visa.ResourceManager()

rm.list_resources()
#%%

gen = "USB0::0x0699::0x0346::C034167::INSTR"
gen_instance = rm.open_resource(gen)



#%% multímetros NOTA: LOS MULTÍMETROS DE BANCO TIENEN UN TIEMPO DE INTEGRACIÓN SEGÚN LOS DÍGITOS QUE LE PIDO


mult1 = "GPIB0::22::INSTR" #tensión
mult2="GPIB0::24::INSTR" #corriente
m1_instance = rm.open_resource(mult1)
m2_instance=rm.open_resource(mult2)
#%%

freq = 1/per
amp = 1
off = 1



'''
gen_instance.write("*RST")
gen_instance.write("FUNCtion:SHAPe RAMP")

'''


#gen_instance.write("PHAS 90") #tanto esta línea como la anterior no están haciendo nada
gen_instance.write(f"FREQuency {freq}")

gen_instance.write(f"VOLTage {amp} ")
gen_instance.write(f"VOLTage:OFFSet {off}")
'''
gen_instance.write("FUNCtion:RAMP:SYMMetry 50")
'''

#%%
gen_instance.write("OUTPUT1:STATE ON")



tmed = per*2
Tlist = []
Clist = []
E1list = []
E2list = []

t0 = time.time()
volts = np.linspace(0.5,2,200)
j = 0
for i in np.linspace(0,per,200):
 
    gen_instance.write(f"VOLT:OFFS {volts[j]}")
    j +=1
    print(j)
    T = m1_instance.query("MEASURE:VOLTAGE:DC?")
    Tlist.append(float(T))
    E1 = m1_instance.query("VOLT:DC:RANGE?")
    E1list.append(E1)
    
    C = m2_instance.query("MEASURE:VOLTAGE:DC?")
    E2 = m2_instance.query("VOLT:DC:RANGE?")
    E2list.append(E2)
    Clist.append(float(C))
    print(T)
    print(C)
    t = time.time()
    #print(round(tmed-(t - t0),1))
    if t - t0 > tmed:
        break
    else:
        continue



gen_instance.write("OUTPUT1:STATE OFF")
#%%

Tlist = [float(voltaje) for voltaje in Tlist] 


Clist = [float(voltaje) for voltaje in Clist] 

#%%
mitad = len(Tlist)//2
Tdif = np.diff(Tlist)
indice = np.where(Tdif[mitad:]>0)[0][0] + 2

plt.figure(1), plt.clf()
plt.plot(Clist, Tlist, ".-")
plt.plot(Clist[indice], Tlist[indice], "o")
#%%
Tl = []
Cl = []

Vmin = 0
V0 = m1_instance.query("MEASURE:VOLTAGE:DC?")

a = 0


#%%    
tf = time.time()
dt = tf - t0
#%%
gen_instance.close()
m1_instance.close()
m2_instance.close()





#%%
df = pd.DataFrame()
df["Tensión"] = Clist
df["Tensión Corriente"] = Tlist
df["ET"] = E2list
df["ETC"] = E1list
nombre = input("Nombre: ")

path = 'C:/Users/publico/Desktop/LABO 4 ESPECTACULAR/Glow/'


df.to_csv(str(path) + str(nombre)+ ".csv")

#%%



df_sorted = df.sort_values("Tensión Corriente")


#%%

Vt = []
#%%
for i in range(len(df_sorted["Tensión Corriente"])):
    i = i+1
    if df_sorted["Tensión Corriente"][i]-df_sorted["Tensión Corriente"][i-1] > 0:
        continue
    else:
        Vt.append(df_sorted["Tensión"][i])
        print(df_sorted["Tensión"][i])
        break