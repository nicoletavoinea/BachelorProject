import tensorflow as tf
from keras.models import load_model
import numpy as np
from numpy import genfromtxt
import time
import tflite_runtime.interpreter as tflite

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def load_h5_model(path):
  print('Model started loading')
  interpreter = tflite.Interpreter(path)
  input_details=interpreter.get_input_details()
  output_details=interpreter.get_output_details()
  interpreter.allocate_tensors()
  print('Model loaded successfully')
  return interpreter, input_details, output_details
  

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
  
def read_input(can_input):
    return can_input
    
def process_input(can_data):
    can_data=can_data.replace('(', '')
    can_data=can_data.replace(')', '')
    can_data=can_data.replace('can0', '')
    can_data=can_data.replace('[', '')
    can_data=can_data.replace(']', '')
    can_data = can_data.split() #timestamp(float), id(hex), dlc(int), bytes(hex,no padding)
    can_data[0]=float(can_data[0])
    can_data[1]=int(can_data[1],16)
    if can_data[1] & 0x2:
      attack=1
      can_data[1]=can_data[1]-2
    else:
      attack=0
    can_data[2]=int(can_data[2])
    for i in range(can_data[2]):
      can_data[i+3]=int(can_data[i+3],16)
    np_can_data = np.zeros(11, dtype=np.float32)
    
    np_can_data[:len(can_data)] = can_data    
    np_can_data=np.expand_dims(np_can_data, axis=0)
    
    return np_can_data,attack
    
    
def classify_data(data,interpreter,input_details,output_details):
    start=time.time()
    interpreter.set_tensor(input_details[0]['index'], data)
    interpreter.invoke()
    predicted=interpreter.get_tensor(output_details[0]['index'])
    end=time.time()	
    return end-start,round(predicted[0][0], 0)
    
  
def main():
  time_sum=0
  nr=0
  interpreter,input_details,output_details=load_h5_model('model.tflite')

  while True:
    can_input = input('')
    can_data = read_input(can_input)
    can_data,attack= process_input(can_data)
    elapsed, prediction=classify_data(can_data,interpreter,input_details,output_details)
    time_sum+=elapsed
    nr+=1
    if(nr==10):
      break
  print(f'Average time: {time_sum/10}')

if __name__ == "__main__":
    main()

