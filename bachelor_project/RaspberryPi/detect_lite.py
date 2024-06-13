import tensorflow as tf
from keras.models import load_model
import numpy as np
from numpy import genfromtxt
import time
import tflite_runtime.interpreter as tflite

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_h5_model(path):
  print('Model started loading')
  interpreter = tflite.Interpreter(path)
  input_details=interpreter.get_input_details()
  output_details=interpreter.get_output_details()
  interpreter.allocate_tensors()
  print('Model loaded successfully')
  return interpreter, input_details, output_details
  

def print_message(msg, predicted, atual,elapsed_time):
  if(predicted==1 and actual==1):#caught messages
    print(bcolors.OKCYAN + f'Elapsed time: {elapsed_time}, Timestamp:{msg[0]} Length:{msg[1]}, Data: {msg[2]} {msg[3]} {msg[4]} {msg[5]} {msg[6]} {msg[7]} {msg[8]} {msg[9]}')
  elif(predicted==0 and actual==1):#failed to catch attack
    print(bcolors.FAIL + f'Elapsed time: {elapsed_time}, Timestamp:{msg[0]} Length:{msg[1]}, Data: {msg[2]} {msg[3]} {msg[4]} {msg[5]} {msg[6]} {msg[7]} {msg[8]} {msg[9]}')
  elif(predicted==1 and actual==0):#false warning
    print(bcolors.WARNING + f'Elapsed time: {elapsed_time}, Timestamp:{msg[0]} Length:{msg[1]}, Data: {msg[2]} {msg[3]} {msg[4]} {msg[5]} {msg[6]} {msg[7]} {msg[8]} {msg[9]}')
  else:#ok
    print(bcolors.OKGREEN + f'Elapsed time: {elapsed_time}, Timestamp:{msg[0]} Length:{msg[1]}, Data: {msg[2]} {msg[3]} {msg[4]} {msg[5]} {msg[6]} {msg[7]} {msg[8]} {msg[9]}')
  
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
    can_data[2]=int(can_data[2])
    for i in range(can_data[2]):
      can_data[i+3]=int(can_data[i+3],16)
    np_can_data = np.zeros(11, dtype=np.float32)
    
    np_can_data[:len(can_data)] = can_data    
    np_can_data=np.expand_dims(np_can_data, axis=0)
    
    return np_can_data #modify to return the exact struacture (to pass directly to predict)
    
    
def classify_data(data,interpreter,input_details,output_details):
    start=time.time()
    interpreter.set_tensor(input_details[0]['index'], data)
    interpreter.invoke()
    predicted=interpreter.get_tensor(output_details[0]['index'])
    end=time.time()	
    predicted=round(predicted[0][0], 0)
    #print_message(entry,predicted,actual,end-start)
    return end-start,predicted
    
  
def main():
  time_sum=0
  nr=0
  interpreter,input_details,output_details=load_h5_model('model.tflite')

  while True:
    can_input = input('')
    can_data = read_input(can_input)
    can_data= process_input(can_data)
    elapsed, prediction=classify_data(can_data,interpreter,input_details,output_details)
    time_sum+=elapsed
    nr+=1
    if(nr==1000):
      break
    #print_data(can_data,prediction,prediction,elapsed)
    #print(can_data)
  print(f'Average time: {time_sum/1000}')

if __name__ == "__main__":
    main()

