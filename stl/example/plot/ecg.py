import numpy as np  
import matplotlib.pyplot as plt  
import scipy

# turn on grid on matplotlib plot





# https://stackoverflow.com/questions/4387878/simulator-of-realistic-ecg-signal-from-rr-data-for-matlab-or-python
import scipy
import scipy.signal as sig

# The RR interval, the time elapsed between two successive R waves of the QRS signal on the electrocardiogram 
# rr = [1.0, 1.0, 0.5, 1.5, 1.0, 1.0] # rr time in seconds
rr = [5, 6]
fs = 8000.0 # default rate
pqrst = sig.wavelets.daub(20) # just to simulate a signal, whatever

ecg = scipy.concatenate([sig.resample(pqrst, int(r*fs)) for r in rr])
t = scipy.arange(len(ecg))/fs
plt.grid()
plt.plot(t, ecg)

print(ecg)
print(len(ecg))

print(t)
print(len(t))

# signal = Signal()
# for i in range(0, ecg)
plt.show()

# properties to be checked
# amp stands for amplitude

# satisfy
#
# G[0, 10](amp > -0.4 & amp < 0.7)
# G[6.21, 6.26](amp < 0)
#
# F[0, 2](amp > 0.6)
# F[4, 6](amp > 0.6)
#
# X[0](amp != 0)
# X[0](amp > 0)
#
# operators left: U, R, W, M
