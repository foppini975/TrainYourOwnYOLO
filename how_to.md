# Setup

1. `cd /Users/fabio/Documents/Volantini`
2. `git clone https://github.com/AntonMu/TrainYourOwnYOLO TrainYourOwnYOLO`
3. `cd TrainYourOwnYOLO`
4. `python3 -m venv env`
5. `source env/bin/activate`
6. `pip install -r requirements.txt`

https://github.com/AntonMu/TrainYourOwnYOLO/tree/master/1_Image_Annotation

7. Using voot, annotate images in ~Documents/Volantini/TrainYourOwnYOLO/Data/Source_Images/Training_Images, then export the voot project to CSV

8. `python Convert_to_YOLO_format.py`, the output file is /Documents/Volantini/TrainYourOwnYOLO/Data/Source_Images/Training_Images/vott-csv-export/data_train.txt

https://github.com/AntonMu/TrainYourOwnYOLO/tree/master/2_Training

9. `cd /Users/fabio/Documents/Volantini/TrainYourOwnYOLO/2_Training`
10. `python Download_and_Convert_YOLO_weights.py`
11. `python Train_YOLO.py`

https://github.com/AntonMu/TrainYourOwnYOLO/tree/master/3_Inference

12. `cd ~/Documents/Volantini/TrainYourOwnYOLO/3_Inference`
13. `python Detector.py`
The outputs are saved to TrainYourOwnYOLO/Data/Source_Images/Test_Image_Detection_Results

# Google Cloud
* `gcloud auth login`
* `gcloud --project=groovy-producer-137216 services list`
* Set the env variable to the ProjectID: `export CLOUDSDK_CORE_PROJECT="groovy-producer-137216"`
