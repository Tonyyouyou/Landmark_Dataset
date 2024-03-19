import os
class Landmarker:
    def __init__(self):
        # read phone and save in list
        # self.phone_data = self.read_phone_data(file_path)
        # define phone
        self.stops = ['b', 'd', 'g', 'p', 't', 'k', 'dx', 'q']
        self.affricates = ['jh', 'ch']
        self.fricatives = ['s', 'sh', 'f', 'th']
        self.voiced_fricatives = ['z', 'zh', 'v', 'dh']
        self.nasals = ['m', 'n', 'ng', 'em', 'en', 'eng', 'nx']
        Glides = ['l', 'r', 'w', 'y', 'hh', 'hv', 'el']
        self.vowels = ['iy', 'ih', 'eh', 'ey', 'ae', 'aa', 'aw', 'ay', 'ah', 'ao', 'oy', 'ow', 'uh', 'uw', 'ux', 'er', 'ax', 'ix', 'axr', 'ax-h']
        # landmark result dict
        self.landmarks = {
            'v+': [], 'v-': [], 'f+': [], 'f-': [], 's+': [], 's-': [], 'b+': [], 'b-': [], 'g+': [], 'g-': []
        }

    def read_phone_data(self, phone_data_file):
        phone_data = []
        with open(phone_data_file, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    start_time, end_time, phone = parts
                    phone_data.append((int(start_time), int(end_time), phone))
        return phone_data

    def annotate_voiced_frication_landmark(self):
        for start_time, end_time, phone in self.phone_data:
            if phone in self.voiced_fricatives:
                self.landmarks['v+'].append(start_time)
                self.landmarks['v-'].append(end_time)
    
    def annotate_frication_landmark(self):
        for start_time, end_time, phone in self.phone_data:
            if phone in self.fricatives:
                self.landmarks['f+'].append(start_time)
                self.landmarks['f-'].append(end_time)

    def annotate_syllabic_landmark(self):
        for start_time, end_time, phone in self.phone_data:
            if phone in self.nasals or phone == 'l':
                self.landmarks['s+'].append(start_time)
                self.landmarks['s-'].append(end_time)

    def annotate_brust_landmark(self):
        brust_realted_phoneme = self.stops + self.affricates 
        for start_time, end_time, phone in self.phone_data:
            if phone in brust_realted_phoneme:
                self.landmarks['b+'].append(start_time)
            if phone in self.affricates:
                self.landmarks['b+'].append(start_time)

            if phone in self.fricatives:
                self.landmarks['b-'].append(end_time)
            if phone in self.stops:
                self.landmarks['b-'].append(end_time)
    
    def annotate_glottal_landmark(self):
        voiced_phone = self.vowels + self.voiced_fricatives + self.nasals
        voiced_phone = set(voiced_phone + ['b', 'd', 'g'])

        g_plus_marked = False
        last_voiced_end_time = None

        for i in range(len(self.phone_data)):
            start_time, end_time, phoneme = self.phone_data[i]
            
            if phoneme in voiced_phone:
                if not g_plus_marked:
                    self.landmarks['g+'].append(start_time)
                    g_plus_marked = True
                last_voiced_end_time = end_time

            else:
                if g_plus_marked:
                    self.landmarks['g-'].append(last_voiced_end_time)
                    g_plus_marked = False

        if g_plus_marked:
            self.landmarks['g-'].append(last_voiced_end_time)
    
    def process(self):
        self.annotate_voiced_frication_landmark()
        self.annotate_frication_landmark()
        self.annotate_syllabic_landmark()
        self.annotate_brust_landmark()
        self.annotate_glottal_landmark()
    
    def get_ordered_landmarks(self):
        all_landmarks = []
        for landmark, times in self.landmarks.items():
            all_landmarks.extend((time, landmark) for time in times)

        all_landmarks.sort()

        return all_landmarks

    def reset_landmarks(self):
        self.landmarks = {landmark: [] for landmark in self.landmarks}
    
    def process_file(self, file_path):
        self.reset_landmarks()
        self.phone_data = self.read_phone_data(file_path)
        self.process()
        return self.get_ordered_landmarks()

    def process_directory(self, directory, output_file_notime, output_file_wittime):
        with open(output_file_wittime, 'w') as outfile:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.PHN'):
                        file_path = os.path.join(root, file)
                        ordered_landmarks = self.process_file(file_path)
                        landmarks_str = ' '.join(f'{time}:{landmark}' for time, landmark in ordered_landmarks)
                        outfile.write(f'{file_path}: {landmarks_str}\n')

        with open(output_file_notime, 'w') as outfile:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.PHN'):
                        file_path = os.path.join(root, file)
                        ordered_landmarks = self.process_file(file_path)
                        landmarks_str = ' '.join(f'{landmark}' for _, landmark in ordered_landmarks)
                        outfile.write(f'{file_path}: {landmarks_str}\n')

def main():
    annotator = Landmarker()
    input_directory = '/g/data/wa66/Xiangyu/Data/Timit/timit/raw/TIMIT/TEST'
    output_file_notime = '/g/data/wa66/Xiangyu/Landmark_dataset/Ground_truth/test_landmark'
    output_file_wittime = '/g/data/wa66/Xiangyu/Landmark_dataset/Ground_truth/test_landmark_time'
    annotator.process_directory(input_directory, output_file_notime, output_file_wittime)

if __name__ == "__main__":
    main()