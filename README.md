# Introduction
In this project, a collection of different deep learning models implemented to process EEG Signals (currently motor imagery signals) are provided. The codes are easy to track and can be easily reproduced. This repo keeps updated.
# Implemented Models
* Deep Neural Networks (DNN)
* Convolutional Neural Networks (CNN)
# Data
* BCI comp IV dataset 2b
This data contains motor imagery EEG signals of 9 subjects. The task is a 2-class classification (Right/Left hand). The original data can be downloaded through the [BCI IV official website]([url](https://bbci.de/competition/iv/)https://bbci.de/competition/iv/). The original data is in .gdf format. In order to use it in Python, you can either use [mne library]([url](https://www.bing.com/ck/a?!&&p=b4982752c00bd681JmltdHM9MTcwMTgyMDgwMCZpZ3VpZD0xZjM0Njg2Mi1mY2NjLTY1MmItMjgzMC03YmMyZmRjNTY0NDUmaW5zaWQ9NTE5NQ&ptn=3&ver=2&hsh=3&fclid=1f346862-fccc-652b-2830-7bc2fdc56445&psq=mne+library&u=a1aHR0cHM6Ly9tbmUudG9vbHMvc3RhYmxlL2luZGV4Lmh0bWw&ntb=1)) or load data with MATLAB's [BIOSIG toolbox]([url](https://www.bing.com/ck/a?!&&p=7c9dda0073bbfdb3JmltdHM9MTcwMTgyMDgwMCZpZ3VpZD0xZjM0Njg2Mi1mY2NjLTY1MmItMjgzMC03YmMyZmRjNTY0NDUmaW5zaWQ9NTE5NA&ptn=3&ver=2&hsh=3&fclid=1f346862-fccc-652b-2830-7bc2fdc56445&psq=biosig+toolbox&u=a1aHR0cHM6Ly93d3cubWF0aHdvcmtzLmNvbS9tYXRsYWJjZW50cmFsL2ZpbGVleGNoYW5nZS83OTQyNy1iaW9zaWctYS10b29sYm94LWZvci1iaW9tZWRpY2FsLXNpZ25hbC1wcm9jZXNzaW5n&ntb=1)). You can find more information about the dataset and how to handle it in original dataset description file available in the dataset website. The file 'load.mat' in this repo provides a MATLAB code for loading the data and saving it in .mat format to use in Python. Also the folder 2b_Dataset is the output of 'load.mat' and contains all data saved in .mat for each subject. You can simply use it in Python and ignore the MATLAB implementation!
# Usage
* DNN
