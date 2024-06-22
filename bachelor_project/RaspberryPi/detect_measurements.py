import tensorflow as tf
from keras.models import load_model
import numpy as np
from numpy import genfromtxt
import time

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
def load_keras_model(model_path):
    print('Model started loading')
    model = load_model(model_path)
    print('Model loaded successfully')
    return model

def read_input(can_input):
    return can_input
    
def process_input(can_data):
    can_data=can_data.replace('(', '')
    can_data=can_data.replace(')', '')
    can_data=can_data.replace('can0', '')
    can_data=can_data.replace('[', '')
    can_data=can_data.replace(']', '')
    can_data = can_data.split() #timestamp, id(hex), dlc, bytes(hex,no padding)
    can_data[0]=float(can_data[0])

    can_data[1]=int(can_data[1],16)
    can_data[2]=int(can_data[2])
    for i in range(can_data[2]):
      can_data[i+3]=int(can_data[i+3],16)
    np_can_data = np.zeros(11, dtype=float)
    
    np_can_data[:len(can_data)] = can_data    
    np_can_data=np.expand_dims(np_can_data, axis=0)
    
    return np_can_data #modify to return the exact struacture (to pass directly to predict)
	
def classify_data(data,model):
    start=time.time()
    predicted= model.predict(data,verbose=0)
    end=time.time()	
			
    predicted=round(predicted[0][0], 0)
    #actual=labels[index]
    #print_message(entry,predicted,actual,end-start)
    return end-start,predicted
	
def print_message(msg, predicted, actual,elapsed_time):
  msg=msg[0].tolist()
  if(predicted==1 and actual==1):#caught messages
    print(bcolors.OKBLUE + f'Elapsed time: {elapsed_time:.6f}, Timestamp:{msg[0]:.6f}, ID:{int(msg[1]):.0f}, DLC: {int(msg[2]):.0f}, Data: {int(msg[3]):#02x} {int(msg[4]):#02x} {int(msg[5]):#02x} {int(msg[6]):#02x} {int(msg[7]):#02x} {int(msg[8]):#02x} {int(msg[8]):#02x} {int(msg[10]):#02x}' + bcolors.ENDC)
  elif(predicted==0 and actual==1):#failed to catch attack
    print(bcolors.FAIL + f'Elapsed time: {elapsed_time:.6f}, Timestamp:{msg[0]:.6f}, ID:{int(msg[1]):.0f}, DLC: {int(msg[2]):.0f}, Data: {int(msg[3]):#02x} {int(msg[4]):#02x} {int(msg[5]):#02x} {int(msg[6]):#02x} {int(msg[7]):#02x} {int(msg[8]):#02x} {int(msg[8]):#02x} {int(msg[10]):#02x}' + bcolors.ENDC)
  elif(predicted==1 and actual==0):#false warning
    print(bcolors.WARNING + f'Elapsed time: {elapsed_time:.6f}, Timestamp:{msg[0]:.6f}, ID:{int(msg[1]):.0f}, DLC: {int(msg[2]):.0f}, Data: {int(msg[3]):#02x} {int(msg[4]):#02x} {int(msg[5]):#02x} {int(msg[6]):#02x} {int(msg[7]):#02x} {int(msg[8]):#02x} {int(msg[8]):#02x} {int(msg[10]):#02x}' + bcolors.ENDC)
  else:
    print(bcolors.OKGREEN + f'Elapsed time: {elapsed_time:.6f}, Timestamp:{msg[0]:.6f}, ID:{int(msg[1]):.0f}, DLC: {int(msg[2]):.0f}, Data: {int(msg[3]):#02x} {int(msg[4]):#02x} {int(msg[5]):#02x} {int(msg[6]):#02x} {int(msg[7]):#02x} {int(msg[8]):#02x} {int(msg[8]):#02x} {int(msg[10]):#02x}' + bcolors.ENDC)
 

def main():
  time_sum=0
  nr=0
  model=load_keras_model('model.h5')
  while True:
    can_input = input('')
    can_data = read_input(can_input)
    can_data= process_input(can_data)
    elapsed, prediction=classify_data(can_data,model)
    time_sum+=elapsed
    nr+=1
    if(nr==10):
      print("Stop")
      print(f'Average time: {time_sum/10}')
      break

if __name__ == "__main__":
    main()
