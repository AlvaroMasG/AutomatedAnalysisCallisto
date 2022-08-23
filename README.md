# Automated Analysis-Callisto
### Description:
It is a series of programs for downloading and analyzing e-Callisto data in search of solar bursts.
### Installation:
Move to the directory where you have downloaded this repository, move to Data_extraction directory, open a terminal/cmd and run ` pip install -r requirements.txt`
### Contributors:
The main collaborator in this project is Álvaro Mas. However, the programs for data download belong to Carlos Yanguas and Mario Fernández available at https://github.com/c-yanguas/Menu-Callisto

## Steps to follow-Callisto
- First, the programs 'BurstDownloader.py', 'CallistoDownloader.py', 'utils.py' and 'main.py' will be used.
- Running 'main.py' will display a menu for downloading and the following instructions must be followed:
1. Please select one of th following options: "3".
2. Please choose one posible extension for the data: "3".
3. Introduce the start date: (example: March 28, 2022) "28-03-2022".
4. Introduce the start date: (example: March 31, 2022) "31-03-2022".
5. Currently available stations: (example: Australia-ASSA) "10".
6. Would you like to download also the solar burst? 0/1: "1".
7. Introduce th number of divisions you would like to make on the image: "15".
- With all these instructions completed, the desired files will be downloaded to the 'Instruments' folder under 'Data'. Instruments' folder under 'Data'. 
- Once the files are downloaded, move the .gz files to the 'Images' folder under 'Data'.
- The 'cleanBurstData.py' script should be run to remove any corrupt or faulty files.
- To analyze the files, the script 'extractBurstData.py' must be run and the result of this analysis can be found in the Excel file 'BurstData.xlsx' in the 'Data' folder.

## Steps to follow-NOAA
To perform a statistical analysis, it is useful to cross-reference data from another data source. In this case it has been facilitated to be able to use the NOAA network.
- To download files from the NOAA network is via FTP protocol.
- Once the files have been downloaded, move the text files to the 'NOAAtxt' folder under 'Data' .
- To analyze the NOAA network files, you must run the script 'extractNOAA.py' and the result of this analysis can be found in the Excel file 'BurstData.xlsx' in the 'Data' folder.

## Parameters of results
As discussed above, the result of the file analysis is found in the Excel file 'BurstData.xlsx' in the 'Data' folder. This analysis divides the solar bursts found in 17 sections:
- From: indicates to which network it belongs whether to e-CALLISTO or NOAA.
- Station: indicates which station it belongs to.
- Year: indicates the year it belongs to.
- Month: indicates to which month it belongs.
- Day: indicates which day it belongs to.
- Freq Max: indicates, in MHz, the maximum frequency of the spectrogram.
- Freq Min: indicates, in MHz, the minimum frequency of the spectrogram.
- Freq: indicates the group in which the frequency range is located. There are three types of groups:
	- 90-15 MHz: these are the ones where the maximum frequency is less than 100 MHz.
	- 180-45 MHz: those in which the maximum frequency is equal to or more than 100 MHz and less than 200 MHz.
less than 200 MHz.
	- 525-110 MHz: maximum frequency is equal to or more than 200 MHz.
- Hour Start: indicates at what time it starts.
- Min Start: indicates at what minute it starts.
- Quarter Start: indicates at what quarter of an hour it starts. It is divided into four groups:
	- 1Q: the first quarter hour, from 0 to 14 minutes.
	- 2Q: the second quarter hour, from 15 to 29 minutes.
	- 3Q: the third quarter hour, from 30 to 44 minutes.
	- 4Q: the last quarter hour, from 45 to 59 minutes.
- Duration (min): duration of the sunburst in minutes.
- Duration (s): duration of the solar burst in seconds.
- Part Duration: for the e-CALLISTO network, it indicates the group in which the solar burst duration is located duration of the solar burst. It is divided into four groups:
	- 1P: from 0 to 4 seconds duration.
	- 2P: from 5 to 14 seconds duration.
	- 3P: from 15 to 59 seconds of duration.
	- 4P: 60 seconds or more in duration.
For the NOAA network, which only indicates the duration in minutes, it is divided into two groups:
	- 1P: from 0 to 59 seconds in duration.
	- 4P: 60 seconds or more in duration.
- Image Start: unique to the e-CALLISTO network, it indicates where the solar burst is in the spectrogram the solar burst is located.
	- FL: far left of the image.
	- L: to the left of the image.
	- C: centered in the image.
	- R: to the right of the image.
	- FR: far right of the image.
- Intensity (dB): unique to the e-CALLISTO network, indicates the peak intensity in decibels.
- Relevance: indicates the relevance of the solar burst according to the peak intensity. It is divided into three groups:
	- 1: less than 3 dB intensity.
	- 2: from equal or more than 3 dB to less than 5 dB of intensity.
	- 3: equal or more than 5 dB of intensity.# AutomatedAnlysisCallisto
