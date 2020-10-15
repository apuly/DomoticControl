# data frame structure

This document describes the different packets send to and from the domotic centre


## base frame:

bytes:  0                  1-2             3-4          5..
        protocol version   frame length    command id   packet data

Length of the command ID is defined in domiticcom.py in ID_LENGTH.
Changing this variable will also change the data frame structure.

the different packet data contents is described below.
Every packet has a corrisponding command id.
All packets are innumerated in dommoticcom.py. The names of these enumerations will be used as packet names

## module frame

module packets are used after a module has received its unique ID, the DC ID and a timestamp.
they extend the base packet with the ID and the timestamp stored in the module

bytes: --baseframe-- 5-36        37..
                     module ID   packet data



## to domoticcentre

### REQUEST_ID
builds on base frame  

frame length: 5  
command id: 0  
packet data: empty  

### REQUEST_INFO.
build on base frame

frame length: 5  
command id: 1  
packet data: empty  

### MODULE_INFO
builds on module frame

module_info sends the information for the module to the DC.
This contains the module type

frame length 69
command id: 2
packet data: 0-1
             module type



## to module

### SET_ID
builds on base frame

frame length 5+64  
command id: 0  
packet data: 0-64: uuid  

### DC_INFO
builds on base frame

frame length 5+64  
command id: 1  
packet data: 0-64: DC ID  

