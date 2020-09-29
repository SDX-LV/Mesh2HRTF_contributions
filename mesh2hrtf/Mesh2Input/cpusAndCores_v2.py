#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:12:36 2020

@author: root
"""

# export variables - try different parameters and see if everything works as expected
cpuFirst          = 1
cpuLast           = 1
numCoresPerCPU    = 2
numEars           = 2

minFrequency      = 0       # new Variable must be added to Export-GUI
maxFrequency      = 22_050

# either 'frequencyStepSize' or 'frequencySteps' must be 0
frequencyStepSize = 0
# new variabel must be added to Export-GUI
numFrequencySteps = 129


# new variable in script:
# maximum number of allowed cpus - previously hard coded as number
# could be maxCPUs = cpuLast if the rests of Mesh2HRTF works with that
maxCPUs  = 10

# new variable in script:
# maximum nuber of allowed cores - previously hard coded as number
# could be maxCores = numCoresPerCPU if the rest of Mesh2HRTF works with that
maxCores = 8


# %% original script at line 454
numCPUs = cpuLast-cpuFirst+1


# %% original script lines 464-475

# remove this block in the script


# %% original block starting at 639

# number of cores per ear and in total
numCoresUsedPerEar    = numCPUs*numCoresPerCPU//numEars
if not numCoresUsedPerEar:
    raise Exception("At least two cores must be available for calculating both ears, i.e., two CPUs with one core each or one CPU with two cores.")

# Number of frequencies and frequency step size
if (numFrequencySteps==0 and frequencyStepSize==0) or (numFrequencySteps!=0 and frequencyStepSize!=0):
    raise Exception("Either 'frequencyStepSize' or 'FrequencySteps' must be zero while the other must not.")

if frequencyStepSize:
    frequencySteps = divmod(maxFrequency-minFrequency, frequencyStepSize)
else:
    if numFrequencySteps < 2:
        raise Exception("'numFrequencySteps' must be at least 2.")
    frequencySteps = (numFrequencySteps, 0)
    frequencyStepSize = (maxFrequency-minFrequency)/(numFrequencySteps-1)

if not frequencySteps[1] == 0:
    raise Exception("Error, frequencyStepSize is not a divisor of maxFrequency-minFrequency")

# all frequencies to be calculated
f = [ff*frequencyStepSize+minFrequency for ff in range(frequencySteps[0])]

# remove 0 Hz if included in the list
if f[0] == 0:
    f.pop(0)
    frequencySteps = (frequencySteps[0]-1, 0)
    print('Warning: 0 Hz can not be calculated and was removed from the list of frequencies.')

# check number of cores and frequencies
if len(f) < numCoresUsedPerEar:
    raise Exception("More cores than frequencies, i.e., numCPUs*numCoresPerCPU//numEars < numFrequencies.")

# distribution of frequencies across numCoresUsedPerEar
F = [[] for ff in range(numCoresUsedPerEar)]
for nn, ff in enumerate(f):
    F[nn%numCoresUsedPerEar].append(ff)

# Initialize cpusAndCores:
# Nested list that indicates which cpu and core is used to calculate data for
# which ear (e.g. cpuAndCores[0][1] holds the entry for the second core on the
# first cpu). Entries: 0=idle, 1=leftEar/right ear if calculating one ear,
# 2=rightEar if calculating two ears.
cpusAndCores = [[0]*maxCores for cc in range(maxCPUs)]

# Initialize frequencies:
# Nested list that holds the frequencies that are calculated by each cpu/core
# (e.g. frequencies[0][1] holds a list of frequencies calculated by the second
# core on the first cpu.
tmp         = [[] for cc in range(maxCores)]
frequencies = [tmp.copy() for cc in range(maxCPUs)]

# distribute ears and frequencies across cpus and cores.
# Left ear is calculated on cpus 0 to numCoresUsedPerEar-1
# Right ear is calculated on cpus numCoresUsedPerEar to numCoresAvailable
for count in range(numCoresUsedPerEar*numEars):
    cpu, core = divmod(count + (cpuFirst-1)*numCoresPerCPU, numCoresPerCPU)
    cpusAndCores[cpu][core] = count//numCoresUsedPerEar + 1
    frequencies[cpu][core]  = F[count%len(F)]
    # output for debugging
    print(f"CPU {cpu+1:2d}, core {core+1}, ear {count//numCoresUsedPerEar + 1}, freqList {count%len(F)}")


# %% deprecated variables

# only used for documentation replace with 'len(f)//numCoresUsedPerEar'
# frequencyStepsPerCore = divmod(frequencySteps[0], numCoresUsedPerEar)
# only used for documentation replace with 'numCoresUsedPerEar*numEars'
# numCoresAvailable = numCoresUsedPerEar*numEars

# remove all occurences
# lowFrequencyCores = 0
# lowFrequency = 0