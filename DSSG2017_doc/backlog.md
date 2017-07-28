Backlog
==========
**Issues, Solutions, and Future Suggestions**



##Hardware Issues and Potential Solutions
### Gas sensor board
* [**Need to Check**] ADC Address Assignment<br>ADC behavior is inconsistent depending on the address pin assginment. According to the spec, connecting the address pin to GND sets its address to 0x48. Similarly, this pin to VDD (0x49), SDA (0x4A), and SDL(0x4B). However, only GND (0x48) shows a consistent ADC behavior, and others vary randomly. So if you want to use an address other than 0x48 for a testing purpose, you need to check the signals beforehand.
* [**To-Do**] Gas sensor value adjustment<br>One thing that we found is that baseline ADC readings for each gas sensor was different from each other. This means we cannot use a simple formula to calculate actual gas values in ppb. 