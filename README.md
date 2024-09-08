# Acoustic Landmark Dataset based on TIMIT

This repository provides a **standard acoustic landmark dataset** built upon the TIMIT corpus. The dataset contains both training and testing landmark data, which can be found in the `Landmark_Dataset/Data` directory.

## Repository Structure

The repository is organized as follows:

Landmark_Dataset/  
│  
├── Data/  
│   ├── train_landmark.txt      # Training data landmarks  
│   └── test_landmark.txt       # Testing data landmarks  
└── README.md                   # Project description



## Landmark Data Format

The acoustic landmark data is stored in the `train_landmark.txt` and `test_landmark.txt` files. Each line in these files follows the format below:

<file_path>: <time>:<landmark> <time>:<landmark> ...


### Example Entry:
/g/data/wa66/Xiangyu/Data/Timit/timit/raw/TIMIT/TRAIN/DR2/MARC0/SI1188.PHN: 2210:g+ 2210:s+ 2673:s- 3759:g- 4600:g+ 4772:b- 5973:v+ 6266:v- 7477:g- 9760:b+ 11110:b- 11110:g+ 12840:g- 13480:b+ 14120:b- 14120:g+ 16793:f+ 16793:g- 20595:b- 20595:f- 


### Explanation:
- **File Path**: `/g/data/wa66/Xiangyu/Data/Timit/timit/raw/TIMIT/TRAIN/DR2/MARC0/SI1188.PHN`
  - The path to the TIMIT speech file.
  
- **Time Information**: `2210`, `2673`, `3759`, etc.
  - These numbers represent the sample points in the audio file. In the TIMIT dataset, the sample rate is **16,000 Hz**, meaning there are 16,000 samples per second.

- **Converting Sample Points to Time**:
  To convert the sample points to actual time (in seconds), use the following formula:

  \[
  \text{Time (in seconds)} = \frac{\text{Sample Point}}{16000}
  \]

  For example:
  - **4600** sample points correspond to \( \frac{4600}{16000} = 0.2875 \) seconds.
  - **2210** sample points correspond to \( \frac{2210}{16000} = 0.1381 \) seconds.

- **Landmark Types**:
  - Each time point is associated with an acoustic landmark, such as:
    - `g+`: Glottal onset
    - `g-`: Glottal offset
    - `s+`: Syllabic onset
    - `s-`: Syllabic offset
    - `b+`: Burst onset
    - `b-`: Burst offset
    - `v+`: Voiced frication onset
    - `v-`: Voiced frication offset
    - `f+`: Fricative onset
    - `f-`: Fricative offset

### Key Features:
- **Training Landmarks**: Located in `train_landmark.txt`, which contains the landmarks for the training dataset.
- **Testing Landmarks**: Located in `test_landmark.txt`, which contains the landmarks for the testing dataset.
- **Precise Time Annotations**: Each landmark is associated with a precise time in the TIMIT corpus.

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/Tonyyouyou/Landmark_Dataset.git
    ```

2. Navigate to the `Landmark_Dataset/Data` directory to access the landmark files:
    ```bash
    cd Landmark_Dataset/Data
    ```

3. Open the `train_landmark.txt` and `test_landmark.txt` files to explore the acoustic landmark data.

## About the Dataset

The **TIMIT Acoustic-Phonetic Continuous Speech Corpus** is widely used for training and evaluating speech recognition systems. This repository focuses on generating and storing **acoustic landmark annotations** for the TIMIT dataset, which can be used for research in speech recognition, phonetics, and linguistics.


## Python-based Toolkits
We have also developed a Python-based tool for automatic landmark extraction, and its basic functionality has been completed. You can find it at the following link: [Auto-Landmark](https://github.com/Tonyyouyou/Auto-Landmark)
