EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:gassensor
LIBS:ads1015
LIBS:lf347n
LIBS:GasPCB-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L GasSensor U1
U 1 1 58AF746C
P 4500 2450
F 0 "U1" H 4500 3000 60  0000 C CNN
F 1 "GasSensor" H 4500 1900 60  0000 C CNN
F 2 "MyFootprints:GasSensor" H 4500 2450 60  0001 C CNN
F 3 "" H 4500 2450 60  0001 C CNN
	1    4500 2450
	1    0    0    -1  
$EndComp
$Comp
L LF347N U3
U 1 1 58B06C26
P 6150 2050
F 0 "U3" V 6600 2200 60  0000 C CNN
F 1 "LF347N" V 5650 2200 60  0000 C CNN
F 2 "Housings_DIP:DIP-14_W7.62mm" H 6150 2050 60  0001 C CNN
F 3 "" H 6150 2050 60  0001 C CNN
	1    6150 2050
	0    1    1    0   
$EndComp
$Comp
L C C2
U 1 1 58B06C92
P 5300 3300
F 0 "C2" H 5325 3400 50  0000 L CNN
F 1 "0.1uF" H 5325 3200 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 5338 3150 50  0001 C CNN
F 3 "" H 5300 3300 50  0000 C CNN
	1    5300 3300
	0    1    1    0   
$EndComp
$Comp
L C C1
U 1 1 58B06CCB
P 5100 1650
F 0 "C1" H 5125 1750 50  0000 L CNN
F 1 "0.1uF" H 5125 1550 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 5138 1500 50  0001 C CNN
F 3 "" H 5100 1650 50  0000 C CNN
	1    5100 1650
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 58B06D1C
P 3600 800
F 0 "R1" V 3680 800 50  0000 C CNN
F 1 "R" V 3600 800 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 3530 800 50  0001 C CNN
F 3 "" H 3600 800 50  0000 C CNN
	1    3600 800 
	0    1    1    0   
$EndComp
$Comp
L R R5
U 1 1 58B06D4E
P 4850 3300
F 0 "R5" V 4930 3300 50  0000 C CNN
F 1 "150" V 4850 3300 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 4780 3300 50  0001 C CNN
F 3 "" H 4850 3300 50  0000 C CNN
	1    4850 3300
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 58B06DB4
P 4350 3800
F 0 "R3" V 4430 3800 50  0000 C CNN
F 1 "R" V 4350 3800 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 4280 3800 50  0001 C CNN
F 3 "" H 4350 3800 50  0000 C CNN
	1    4350 3800
	0    1    1    0   
$EndComp
Text GLabel 3200 800  0    60   Input ~ 0
V+
Text GLabel 5950 2700 2    60   Output ~ 0
VOUT0
$Comp
L GND #PWR01
U 1 1 58B071EE
P 3750 1500
F 0 "#PWR01" H 3750 1250 50  0001 C CNN
F 1 "GND" H 3750 1350 50  0000 C CNN
F 2 "" H 3750 1500 50  0000 C CNN
F 3 "" H 3750 1500 50  0000 C CNN
	1    3750 1500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 58B0956E
P 4750 4400
F 0 "#PWR02" H 4750 4150 50  0001 C CNN
F 1 "GND" H 4750 4250 50  0000 C CNN
F 2 "" H 4750 4400 50  0000 C CNN
F 3 "" H 4750 4400 50  0000 C CNN
	1    4750 4400
	1    0    0    -1  
$EndComp
$Comp
L GasSensor U2
U 1 1 58B0A57B
P 8100 1650
F 0 "U2" H 8100 2200 60  0000 C CNN
F 1 "GasSensor" H 8100 1100 60  0000 C CNN
F 2 "MyFootprints:GasSensor" H 8100 1650 60  0001 C CNN
F 3 "" H 8100 1650 60  0001 C CNN
	1    8100 1650
	-1   0    0    1   
$EndComp
$Comp
L C C4
U 1 1 58B0A582
P 7300 800
F 0 "C4" H 7325 900 50  0000 L CNN
F 1 "0.1uF" H 7325 700 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 7338 650 50  0001 C CNN
F 3 "" H 7300 800 50  0000 C CNN
	1    7300 800 
	0    -1   -1   0   
$EndComp
$Comp
L C C3
U 1 1 58B0A589
P 7500 2450
F 0 "C3" H 7525 2550 50  0000 L CNN
F 1 "0.1uF" H 7525 2350 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 7538 2300 50  0001 C CNN
F 3 "" H 7500 2450 50  0000 C CNN
	1    7500 2450
	-1   0    0    1   
$EndComp
$Comp
L R R7
U 1 1 58B0A590
P 9000 3150
F 0 "R7" V 9080 3150 50  0000 C CNN
F 1 "R" V 9000 3150 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8930 3150 50  0001 C CNN
F 3 "" H 9000 3150 50  0000 C CNN
	1    9000 3150
	0    -1   -1   0   
$EndComp
$Comp
L R R11
U 1 1 58B0A597
P 7750 800
F 0 "R11" V 7830 800 50  0000 C CNN
F 1 "150" V 7750 800 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 7680 800 50  0001 C CNN
F 3 "" H 7750 800 50  0000 C CNN
	1    7750 800 
	0    -1   -1   0   
$EndComp
$Comp
L R R9
U 1 1 58B0A5A5
P 8250 300
F 0 "R9" V 8330 300 50  0000 C CNN
F 1 "R" V 8250 300 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8180 300 50  0001 C CNN
F 3 "" H 8250 300 50  0000 C CNN
	1    8250 300 
	0    -1   -1   0   
$EndComp
Text GLabel 9400 3150 2    60   Input ~ 0
V+
$Comp
L GND #PWR03
U 1 1 58B0A5BB
P 8850 2600
F 0 "#PWR03" H 8850 2350 50  0001 C CNN
F 1 "GND" H 8850 2450 50  0000 C CNN
F 2 "" H 8850 2600 50  0000 C CNN
F 3 "" H 8850 2600 50  0000 C CNN
	1    8850 2600
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR04
U 1 1 58B0A5E8
P 7850 -300
F 0 "#PWR04" H 7850 -550 50  0001 C CNN
F 1 "GND" H 7850 -450 50  0000 C CNN
F 2 "" H 7850 -300 50  0000 C CNN
F 3 "" H 7850 -300 50  0000 C CNN
	1    7850 -300
	-1   0    0    1   
$EndComp
Text GLabel 6500 1150 2    60   Output ~ 0
VOUT1
$Comp
L GasSensor U4
U 1 1 58B0E68B
P 5550 6500
F 0 "U4" H 5550 7050 60  0000 C CNN
F 1 "GasSensor" H 5550 5950 60  0000 C CNN
F 2 "MyFootprints:GasSensor" H 5550 6500 60  0001 C CNN
F 3 "" H 5550 6500 60  0001 C CNN
	1    5550 6500
	1    0    0    -1  
$EndComp
$Comp
L LF347N U6
U 1 1 58B0E692
P 7200 6100
F 0 "U6" V 7650 6250 60  0000 C CNN
F 1 "LF347N" V 6700 6250 60  0000 C CNN
F 2 "Housings_DIP:DIP-14_W7.62mm" H 7200 6100 60  0001 C CNN
F 3 "" H 7200 6100 60  0001 C CNN
	1    7200 6100
	0    1    1    0   
$EndComp
$Comp
L C C6
U 1 1 58B0E699
P 6350 7350
F 0 "C6" H 6375 7450 50  0000 L CNN
F 1 "0.1uF" H 6375 7250 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 6388 7200 50  0001 C CNN
F 3 "" H 6350 7350 50  0000 C CNN
	1    6350 7350
	0    1    1    0   
$EndComp
$Comp
L C C5
U 1 1 58B0E6A0
P 6150 5700
F 0 "C5" H 6175 5800 50  0000 L CNN
F 1 "0.1uF" H 6175 5600 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 6188 5550 50  0001 C CNN
F 3 "" H 6150 5700 50  0000 C CNN
	1    6150 5700
	1    0    0    -1  
$EndComp
$Comp
L R R13
U 1 1 58B0E6A7
P 4650 4850
F 0 "R13" V 4730 4850 50  0000 C CNN
F 1 "R" V 4650 4850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 4580 4850 50  0001 C CNN
F 3 "" H 4650 4850 50  0000 C CNN
	1    4650 4850
	0    1    1    0   
$EndComp
$Comp
L R R17
U 1 1 58B0E6AE
P 5900 7350
F 0 "R17" V 5980 7350 50  0000 C CNN
F 1 "150" V 5900 7350 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5830 7350 50  0001 C CNN
F 3 "" H 5900 7350 50  0000 C CNN
	1    5900 7350
	0    1    1    0   
$EndComp
$Comp
L R R15
U 1 1 58B0E6BC
P 5400 7850
F 0 "R15" V 5480 7850 50  0000 C CNN
F 1 "R" V 5400 7850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5330 7850 50  0001 C CNN
F 3 "" H 5400 7850 50  0000 C CNN
	1    5400 7850
	0    1    1    0   
$EndComp
Text GLabel 4250 4850 0    60   Input ~ 0
V+
Text GLabel 7000 6750 2    60   Output ~ 0
VOUT2
$Comp
L GND #PWR05
U 1 1 58B0E6D3
P 4800 5550
F 0 "#PWR05" H 4800 5300 50  0001 C CNN
F 1 "GND" H 4800 5400 50  0000 C CNN
F 2 "" H 4800 5550 50  0000 C CNN
F 3 "" H 4800 5550 50  0000 C CNN
	1    4800 5550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 58B0E6D9
P 5800 8450
F 0 "#PWR06" H 5800 8200 50  0001 C CNN
F 1 "GND" H 5800 8300 50  0000 C CNN
F 2 "" H 5800 8450 50  0000 C CNN
F 3 "" H 5800 8450 50  0000 C CNN
	1    5800 8450
	1    0    0    -1  
$EndComp
$Comp
L GasSensor U5
U 1 1 58B0E6DF
P 9150 5700
F 0 "U5" H 9150 6250 60  0000 C CNN
F 1 "GasSensor" H 9150 5150 60  0000 C CNN
F 2 "MyFootprints:GasSensor" H 9150 5700 60  0001 C CNN
F 3 "" H 9150 5700 60  0001 C CNN
	1    9150 5700
	-1   0    0    1   
$EndComp
$Comp
L C C8
U 1 1 58B0E6E6
P 8350 4850
F 0 "C8" H 8375 4950 50  0000 L CNN
F 1 "0.1uF" H 8375 4750 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8388 4700 50  0001 C CNN
F 3 "" H 8350 4850 50  0000 C CNN
	1    8350 4850
	0    -1   -1   0   
$EndComp
$Comp
L C C7
U 1 1 58B0E6ED
P 8550 6500
F 0 "C7" H 8575 6600 50  0000 L CNN
F 1 "0.1uF" H 8575 6400 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8588 6350 50  0001 C CNN
F 3 "" H 8550 6500 50  0000 C CNN
	1    8550 6500
	-1   0    0    1   
$EndComp
$Comp
L R R19
U 1 1 58B0E6F4
P 10050 7200
F 0 "R19" V 10130 7200 50  0000 C CNN
F 1 "R" V 10050 7200 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 9980 7200 50  0001 C CNN
F 3 "" H 10050 7200 50  0000 C CNN
	1    10050 7200
	0    -1   -1   0   
$EndComp
$Comp
L R R23
U 1 1 58B0E6FB
P 8800 4850
F 0 "R23" V 8880 4850 50  0000 C CNN
F 1 "150" V 8800 4850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8730 4850 50  0001 C CNN
F 3 "" H 8800 4850 50  0000 C CNN
	1    8800 4850
	0    -1   -1   0   
$EndComp
$Comp
L R R21
U 1 1 58B0E709
P 9300 4350
F 0 "R21" V 9380 4350 50  0000 C CNN
F 1 "R" V 9300 4350 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 9230 4350 50  0001 C CNN
F 3 "" H 9300 4350 50  0000 C CNN
	1    9300 4350
	0    -1   -1   0   
$EndComp
Text GLabel 10450 7200 2    60   Input ~ 0
V+
$Comp
L GND #PWR07
U 1 1 58B0E71F
P 9900 6650
F 0 "#PWR07" H 9900 6400 50  0001 C CNN
F 1 "GND" H 9900 6500 50  0000 C CNN
F 2 "" H 9900 6650 50  0000 C CNN
F 3 "" H 9900 6650 50  0000 C CNN
	1    9900 6650
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR08
U 1 1 58B0E725
P 8900 3750
F 0 "#PWR08" H 8900 3500 50  0001 C CNN
F 1 "GND" H 8900 3600 50  0000 C CNN
F 2 "" H 8900 3750 50  0000 C CNN
F 3 "" H 8900 3750 50  0000 C CNN
	1    8900 3750
	-1   0    0    1   
$EndComp
Text GLabel 7550 5200 2    60   Output ~ 0
VOUT3
$Comp
L ADS1015 U7
U 1 1 58B0EB98
P 10250 2250
F 0 "U7" V 11100 2550 60  0000 C CNN
F 1 "ADS1015" V 9850 2600 60  0000 C CNN
F 2 "Connectors_Terminal_Blocks:TerminalBlock_Pheonix_MPT-2.54mm_10pol" H 10250 2250 60  0001 C CNN
F 3 "" H 10250 2250 60  0001 C CNN
	1    10250 2250
	0    1    1    0   
$EndComp
Text GLabel 10200 2650 0    60   Input ~ 0
VOUT0
Text GLabel 10200 2750 0    60   Input ~ 0
VOUT1
Text GLabel 10200 2850 0    60   Input ~ 0
VOUT2
Text GLabel 10200 2950 0    60   Input ~ 0
VOUT3
$Comp
L GND #PWR09
U 1 1 58B0F26E
P 9650 2250
F 0 "#PWR09" H 9650 2000 50  0001 C CNN
F 1 "GND" H 9650 2100 50  0000 C CNN
F 2 "" H 9650 2250 50  0000 C CNN
F 3 "" H 9650 2250 50  0000 C CNN
	1    9650 2250
	1    0    0    -1  
$EndComp
NoConn ~ 10200 2250
NoConn ~ 10200 2350
NoConn ~ 10200 2450
NoConn ~ 10200 2550
NoConn ~ 8600 1750
NoConn ~ 8600 1550
NoConn ~ 4000 2550
NoConn ~ 4000 2350
NoConn ~ 5050 6600
NoConn ~ 5050 6400
NoConn ~ 9650 5800
NoConn ~ 9650 5600
NoConn ~ 1800 2700
Text GLabel 6300 850  2    60   Output ~ 0
V+
Text GLabel 5850 2050 0    60   Input ~ 0
V+
Text GLabel 6900 6100 0    60   Input ~ 0
V+
$Comp
L R R2
U 1 1 58B5B732
P 3750 1200
F 0 "R2" V 3830 1200 50  0000 C CNN
F 1 "R" V 3750 1200 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 3680 1200 50  0001 C CNN
F 3 "" H 3750 1200 50  0000 C CNN
	1    3750 1200
	-1   0    0    1   
$EndComp
$Comp
L C C9
U 1 1 58B5BFAB
P 6150 950
F 0 "C9" H 6175 1050 50  0000 L CNN
F 1 "10uF" H 6175 850 50  0000 L CNN
F 2 "Capacitors_THT:CP_Radial_Tantal_D8.0mm_P2.50mm" H 6188 800 50  0001 C CNN
F 3 "" H 6150 950 50  0000 C CNN
	1    6150 950 
	1    0    0    -1  
$EndComp
$Comp
L R R8
U 1 1 58B5EFCC
P 8850 2850
F 0 "R8" V 8930 2850 50  0000 C CNN
F 1 "R" V 8850 2850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8780 2850 50  0001 C CNN
F 3 "" H 8850 2850 50  0000 C CNN
	1    8850 2850
	1    0    0    -1  
$EndComp
$Comp
L R R14
U 1 1 58B5FAAF
P 4800 5300
F 0 "R14" V 4880 5300 50  0000 C CNN
F 1 "R" V 4800 5300 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 4730 5300 50  0001 C CNN
F 3 "" H 4800 5300 50  0000 C CNN
	1    4800 5300
	-1   0    0    1   
$EndComp
$Comp
L R R20
U 1 1 58B60411
P 9900 6900
F 0 "R20" V 9980 6900 50  0000 C CNN
F 1 "R" V 9900 6900 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 9830 6900 50  0001 C CNN
F 3 "" H 9900 6900 50  0000 C CNN
	1    9900 6900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR010
U 1 1 58B708E2
P 6850 2050
F 0 "#PWR010" H 6850 1800 50  0001 C CNN
F 1 "GND" H 6850 1900 50  0000 C CNN
F 2 "" H 6850 2050 50  0000 C CNN
F 3 "" H 6850 2050 50  0000 C CNN
	1    6850 2050
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR011
U 1 1 58B70A6A
P 6150 1250
F 0 "#PWR011" H 6150 1000 50  0001 C CNN
F 1 "GND" H 6150 1100 50  0000 C CNN
F 2 "" H 6150 1250 50  0000 C CNN
F 3 "" H 6150 1250 50  0000 C CNN
	1    6150 1250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 58B71CFA
P 7900 6100
F 0 "#PWR012" H 7900 5850 50  0001 C CNN
F 1 "GND" H 7900 5950 50  0000 C CNN
F 2 "" H 7900 6100 50  0000 C CNN
F 3 "" H 7900 6100 50  0000 C CNN
	1    7900 6100
	0    -1   -1   0   
$EndComp
$Comp
L R R6
U 1 1 5910B92A
P 5300 3000
F 0 "R6" V 5380 3000 50  0000 C CNN
F 1 "R" V 5300 3000 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5230 3000 50  0001 C CNN
F 3 "" H 5300 3000 50  0000 C CNN
	1    5300 3000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3200 800  3450 800 
Wire Wire Line
	3750 800  3750 1050
Connection ~ 3350 800 
Wire Wire Line
	5000 3300 5150 3300
Wire Wire Line
	4700 1500 4700 2000
Wire Wire Line
	4500 1850 5850 1850
Wire Wire Line
	4500 1850 4500 2000
Wire Wire Line
	5100 1800 5100 1850
Connection ~ 5100 1850
Wire Wire Line
	4700 1500 5600 1500
Wire Wire Line
	5600 1500 5600 1750
Wire Wire Line
	5600 1750 5850 1750
Connection ~ 5100 1500
Wire Wire Line
	3750 800  5400 800 
Wire Wire Line
	5400 800  5400 1950
Wire Wire Line
	5400 1950 5850 1950
Wire Wire Line
	4600 2900 4600 3300
Wire Wire Line
	4400 3300 4700 3300
Wire Wire Line
	4400 2900 4400 3300
Connection ~ 4600 3300
Wire Wire Line
	5700 3300 5450 3300
Wire Wire Line
	5700 2350 5700 3300
Wire Wire Line
	5700 2350 5850 2350
Connection ~ 5500 3300
Wire Wire Line
	5100 2250 5100 3300
Connection ~ 5100 3300
Wire Wire Line
	5100 2250 5850 2250
Connection ~ 5100 3000
Wire Wire Line
	4750 3800 4750 3950
Wire Wire Line
	4500 3800 5600 3800
Wire Wire Line
	3350 800  3350 3800
Wire Wire Line
	3350 3800 4200 3800
Wire Wire Line
	5600 3800 5600 2150
Wire Wire Line
	5600 2150 5850 2150
Connection ~ 4750 3800
Wire Wire Line
	5950 2700 5700 2700
Connection ~ 5700 2700
Wire Wire Line
	9150 3150 9400 3150
Wire Wire Line
	8850 3000 8850 3150
Connection ~ 9250 3150
Wire Wire Line
	7450 800  7600 800 
Wire Wire Line
	7900 2600 7900 2100
Wire Wire Line
	6750 2250 8100 2250
Wire Wire Line
	8100 2250 8100 2100
Wire Wire Line
	7500 2300 7500 2250
Connection ~ 7500 2250
Wire Wire Line
	7000 2600 7900 2600
Wire Wire Line
	7000 2600 7000 2350
Wire Wire Line
	7000 2350 6750 2350
Connection ~ 7500 2600
Wire Wire Line
	8850 3150 7200 3150
Wire Wire Line
	7200 3150 7200 2150
Wire Wire Line
	7200 2150 6750 2150
Wire Wire Line
	8000 1200 8000 800 
Wire Wire Line
	7900 800  8200 800 
Wire Wire Line
	8200 800  8200 1200
Connection ~ 8000 800 
Wire Wire Line
	6900 800  7150 800 
Wire Wire Line
	6900 800  6900 1750
Wire Wire Line
	6900 1750 6750 1750
Wire Wire Line
	7100 1100 7100 800 
Connection ~ 7100 800 
Wire Wire Line
	7500 800  7500 1850
Connection ~ 7500 800 
Wire Wire Line
	7500 1850 6750 1850
Connection ~ 7500 1100
Wire Wire Line
	7850 150  7850 300 
Wire Wire Line
	7000 300  8100 300 
Wire Wire Line
	9250 3150 9250 300 
Wire Wire Line
	9250 300  8400 300 
Wire Wire Line
	7000 300  7000 1950
Wire Wire Line
	7000 1950 6750 1950
Connection ~ 7850 300 
Wire Wire Line
	6400 1400 6900 1400
Connection ~ 6900 1400
Wire Wire Line
	6400 1400 6400 1150
Wire Wire Line
	6400 1150 6500 1150
Wire Wire Line
	4250 4850 4500 4850
Wire Wire Line
	4800 4850 4800 5150
Connection ~ 4400 4850
Wire Wire Line
	6050 7350 6200 7350
Wire Wire Line
	5750 5550 5750 6050
Wire Wire Line
	5550 5900 6900 5900
Wire Wire Line
	5550 5900 5550 6050
Wire Wire Line
	6150 5850 6150 5900
Connection ~ 6150 5900
Wire Wire Line
	5750 5550 6650 5550
Wire Wire Line
	6650 5550 6650 5800
Wire Wire Line
	6650 5800 6900 5800
Connection ~ 6150 5550
Wire Wire Line
	4800 4850 6450 4850
Wire Wire Line
	6450 4850 6450 6000
Wire Wire Line
	6450 6000 6900 6000
Wire Wire Line
	5650 6950 5650 7350
Wire Wire Line
	5450 7350 5750 7350
Wire Wire Line
	5450 6950 5450 7350
Connection ~ 5650 7350
Wire Wire Line
	6750 7350 6500 7350
Wire Wire Line
	6750 6400 6750 7350
Wire Wire Line
	6750 6400 6900 6400
Connection ~ 6550 7350
Wire Wire Line
	6150 6300 6150 7350
Connection ~ 6150 7350
Wire Wire Line
	6150 6300 6900 6300
Wire Wire Line
	5800 7850 5800 8000
Wire Wire Line
	5550 7850 6650 7850
Wire Wire Line
	4400 4850 4400 7850
Wire Wire Line
	4400 7850 5250 7850
Wire Wire Line
	6650 7850 6650 6200
Wire Wire Line
	6650 6200 6900 6200
Connection ~ 5800 7850
Wire Wire Line
	7000 6750 6750 6750
Connection ~ 6750 6750
Wire Wire Line
	10200 7200 10450 7200
Wire Wire Line
	9900 7050 9900 7200
Connection ~ 10300 7200
Wire Wire Line
	8500 4850 8650 4850
Wire Wire Line
	8950 6650 8950 6150
Wire Wire Line
	7800 6300 9150 6300
Wire Wire Line
	9150 6300 9150 6150
Wire Wire Line
	8550 6350 8550 6300
Connection ~ 8550 6300
Wire Wire Line
	8050 6650 8950 6650
Wire Wire Line
	8050 6650 8050 6400
Wire Wire Line
	8050 6400 7800 6400
Connection ~ 8550 6650
Wire Wire Line
	9900 7200 8250 7200
Wire Wire Line
	8250 7200 8250 6200
Wire Wire Line
	8250 6200 7800 6200
Wire Wire Line
	9050 5250 9050 4850
Wire Wire Line
	8950 4850 9250 4850
Wire Wire Line
	9250 4850 9250 5250
Connection ~ 9050 4850
Wire Wire Line
	7950 4850 8200 4850
Wire Wire Line
	7950 4850 7950 5800
Wire Wire Line
	7950 5800 7800 5800
Wire Wire Line
	8150 5150 8150 4850
Connection ~ 8150 4850
Wire Wire Line
	8550 4850 8550 5900
Connection ~ 8550 4850
Wire Wire Line
	8550 5900 7800 5900
Connection ~ 8550 5150
Wire Wire Line
	8900 4250 8900 4350
Wire Wire Line
	8050 4350 9150 4350
Wire Wire Line
	10300 7200 10300 4350
Wire Wire Line
	10300 4350 9450 4350
Wire Wire Line
	8050 4350 8050 6000
Wire Wire Line
	8050 6000 7800 6000
Connection ~ 8900 4350
Wire Wire Line
	7450 5450 7950 5450
Connection ~ 7950 5450
Wire Wire Line
	7450 5450 7450 5200
Wire Wire Line
	7450 5200 7550 5200
Wire Wire Line
	10200 2150 9650 2150
Wire Wire Line
	9650 2150 9650 2250
Wire Wire Line
	3750 1350 3750 1500
Wire Wire Line
	4800 5450 4800 5550
Wire Wire Line
	8900 3750 8900 3950
Wire Wire Line
	9900 6650 9900 6750
Wire Wire Line
	4750 4400 4750 4250
Wire Wire Line
	10100 1550 10100 2050
Wire Wire Line
	10100 2050 10200 2050
Wire Wire Line
	6300 850  6250 850 
Wire Wire Line
	6250 850  6250 800 
Wire Wire Line
	8850 2700 8850 2600
Connection ~ 6150 7150
Wire Wire Line
	6750 2050 6850 2050
Wire Wire Line
	6150 1250 6150 1100
Wire Wire Line
	7800 6100 7900 6100
Wire Wire Line
	5150 3000 5100 3000
Wire Wire Line
	5450 3000 5500 3000
Wire Wire Line
	5500 3000 5500 3300
$Comp
L R R4
U 1 1 5910C8E2
P 4750 4100
F 0 "R4" V 4830 4100 50  0000 C CNN
F 1 "R" V 4750 4100 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 4680 4100 50  0001 C CNN
F 3 "" H 4750 4100 50  0000 C CNN
	1    4750 4100
	-1   0    0    1   
$EndComp
$Comp
L R R10
U 1 1 5910CEA0
P 7850 0
F 0 "R10" V 7930 0   50  0000 C CNN
F 1 "R" V 7850 0   50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 7780 0   50  0001 C CNN
F 3 "" H 7850 0   50  0000 C CNN
	1    7850 0   
	1    0    0    -1  
$EndComp
Wire Wire Line
	7850 -150 7850 -300
$Comp
L R R12
U 1 1 5910D613
P 7250 1100
F 0 "R12" V 7330 1100 50  0000 C CNN
F 1 "R" V 7250 1100 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 7180 1100 50  0001 C CNN
F 3 "" H 7250 1100 50  0000 C CNN
	1    7250 1100
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7400 1100 7500 1100
$Comp
L R R16
U 1 1 5910DE7C
P 5800 8150
F 0 "R16" V 5880 8150 50  0000 C CNN
F 1 "R" V 5800 8150 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5730 8150 50  0001 C CNN
F 3 "" H 5800 8150 50  0000 C CNN
	1    5800 8150
	-1   0    0    1   
$EndComp
Wire Wire Line
	5800 8300 5800 8450
$Comp
L R R18
U 1 1 5910E3B8
P 6400 7150
F 0 "R18" V 6480 7150 50  0000 C CNN
F 1 "R" V 6400 7150 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 6330 7150 50  0001 C CNN
F 3 "" H 6400 7150 50  0000 C CNN
	1    6400 7150
	0    1    1    0   
$EndComp
Wire Wire Line
	6550 7150 6550 7350
Wire Wire Line
	6250 7150 6150 7150
$Comp
L R R22
U 1 1 5910E844
P 8900 4100
F 0 "R22" V 8980 4100 50  0000 C CNN
F 1 "R" V 8900 4100 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8830 4100 50  0001 C CNN
F 3 "" H 8900 4100 50  0000 C CNN
	1    8900 4100
	1    0    0    -1  
$EndComp
$Comp
L R R24
U 1 1 5910ECAE
P 8350 5150
F 0 "R24" V 8430 5150 50  0000 C CNN
F 1 "R" V 8350 5150 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8280 5150 50  0001 C CNN
F 3 "" H 8350 5150 50  0000 C CNN
	1    8350 5150
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8550 5150 8500 5150
Wire Wire Line
	8200 5150 8150 5150
Text GLabel 10200 1550 2    60   Input ~ 0
V+
Wire Wire Line
	10200 1550 10100 1550
Wire Wire Line
	6250 800  6150 800 
$EndSCHEMATC
