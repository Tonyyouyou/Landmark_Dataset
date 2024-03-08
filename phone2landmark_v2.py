class AcousticLandmarkDetector:
    def __init__(self, file_path, sample_rate):
        self.file_path = file_path
        self.sample_rate = sample_rate
        self.landmarks = {}

    def parse_phone_line(self, line):
        parts = line.split()
        if len(parts) == 3:
            start, end, phone = parts
            return int(start), int(end), phone
        return None

    def identify_landmarks(self, phone):
        stop_landmarks = ['+b', '-b']
        affricate_landmarks = ['+f', '-f', '+b', '-b']
        fricative_landmarks = ['+f', '-f']
        voiced_fricative_landmarks = ['+v', '-v']
        nasal_landmarks = ['+s', '-s']
        vowel_landmarks = ['+g', '-g', '+p', '-p']


        b_plus = ['s', 'sh', 'f', 'th', 'p', 't', 'k']
        b_mins = [rest]

        g_plus = [vowels, voiced_fricatives, 'd', 'g', 'p', 'dx', 'q']
        g_mins = [unvoice]
    

        s_plus = [Glides, nasals]
        s_mins = [rest]


        Glides = ['l', 'r', 'w', 'y', 'hh', 'hv', 'el']
        stops = ['b', 'd', 'g', 'p', 't', 'k', 'dx', 'q']
        affricates = ['jh', 'ch']
        fricatives = ['s', 'sh', 'f', 'th']
        voiced_fricatives = ['z', 'zh', 'v', 'dh']
        nasals = ['m', 'n', 'ng', 'em', 'en', 'eng', 'nx'] 
        vowels = ['iy', 'ih', 'eh', 'ey', 'ae', 'aa', 'aw', 'ay', 'ah', 'ao', 'oy', 'ow', 'uh', 'uw', 'ux', 'er', 'ax', 'ix', 'axr', 'ax-h']

        # liquid = ['l', 'r']

        if phone in stops:
            return stop_landmarks
        elif phone in affricates:
            return affricate_landmarks
        elif phone in fricatives:
            return fricative_landmarks
        elif phone in voiced_fricatives:
            return voiced_fricative_landmarks
        elif phone in nasals:
            return nasal_landmarks
        elif phone in vowels:
            return vowel_landmarks
        else:
            return []
        
    def calculate_landmark_time(self, phone_data, lm_type):
        start, end = phone_data
        start_time = int(start) / self.sample_rate * 1000
        end_time = int(end) / self.sample_rate * 1000
        mid_time = (start_time + end_time) / 2
        quarter_time = (end_time - start_time) / 4

        if lm_type in ['+g']:
            return start_time
        elif lm_type in ['-g']:
            return end_time
        elif lm_type == '+p':
            return start_time + quarter_time
        elif lm_type == '-p':
            return end_time - quarter_time 
        
        if lm_type in ['+b', '-b']:
            return start_time if '+' in lm_type else end_time
        elif lm_type == '+f':
            return mid_time - quarter_time / 2
        elif lm_type == '-f':
            return mid_time + quarter_time / 2
        
        elif lm_type in ['+s', '-s', '+v', '-v']:
             return start_time if '+' in lm_type else end_time

    def process_phones(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                phone_data = self.parse_phone_line(line)
                if phone_data:
                    start_time, end_time, phone = phone_data
                    lm_types = self.identify_landmarks(phone)

                    for lm in lm_types:
                        time = self.calculate_landmark_time([start_time, end_time], lm)
                        if lm not in self.landmarks:
                            self.landmarks[lm] = []
                        self.landmarks[lm].append(time)

        return self.landmarks

    
    def save_landmarks_to_file(self, output_file):
        self.process_phones()
        with open(output_file, 'w') as file:
            for lm, times in self.landmarks.items():
                file.write(f"{lm}: {times}\n")