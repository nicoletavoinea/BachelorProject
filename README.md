# DETECTING INTRUSIONS ON CAN BUSES INSIDE PASSENGER CARS WITH MACHINE LEARNING ALGORITHMS -Bachelor's Degree Project

Since this project is composed of multiple parts, this README file will provide informations regarding each phase.

## CANoe Simulation

For generating intrusions into the dataset, there was used a CANoe simulation. For performing this phase, you need to have CANoe installed, together with a valid licence. The files needed can be found at 'bachelor_project/CANoe'.  Then, follow the steps:
   1. Load the configuration by clicking File > Open >Select 'AttackConfiguration.cfg'
   2. For creating attacks, enable one of the nodes: 'general_attack', 'fuzzing_attack', 'replay_attack', by selecting them and pressing Space key. Then, to start the simulation press 'Start', the first button on the left when opening 'Home' tab.
   3. For running a live demo, disable all above attacks with the same key and enable the node called 'live_demo'. Start the simulation in the same way and then follow the steps presented in RaspberryPi section.


## Machine Learning Training

This phase was developed using Google Colaboratory. For running the code, upload the file CANAttacksDetection.ipynb into Google Colab environment. Then follow the next steps:
   1. Connect to Google Drive, where you should have the necessary files for training. The files can be accessed from [here](https://drive.google.com/drive/folders/1Z_gJYalmKNEBEdQrNC7AT7APILjp1_J6?usp=drive_link). 
   2. For Input Data Analysis details, run the cells from the section with the same name. 
   3. For doing the Data Cleaning process, run the cells from the section with the same name. It is not mandatory to do this process since at the end of the cleaning, some new files were stored on drive.
   4. For training the model and getting some results, run the 'Classification' section from the project.
   5. For conversion to .tflite model (used for running the code on RaspberryPi), run the section 'Convert keras model -> TensorFlow Lite Model'. This will save the new model on the drive as 'model.tflite'.

## RaspberryPi

For this phase you need to have a RaspberryPi with all the needed packages installed. They can be found in the [documentation](https://github.com/nicoletavoinea/BachelorProject/blob/328d50f966ab203e96d835c2beb742bbf1650b3b/Voinea_Nicoleta-Valentina_Documentatie_CTIEN_Licenta.pdf), starting with page 34. Connect the board to the device on which it runs CANoe simulation. Then follow the steps:
   1. Open a terminal in the folder where you saved the contents of folder 'bachelor_project/RaspberryPi'.
   2. Configure the CAN communication by running in the terminal:
      `sudo ip link set can0 up type can bitrate 500000`
   4. Start the communication by running in the terminal:
      `sudo ifconfig can0 up`
   5. Execute the live demo program by running in the terminal:
      `candump -t z can0 | python3 detect_lite.py`
