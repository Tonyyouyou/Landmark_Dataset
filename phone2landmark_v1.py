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

    def calculate_landmark_time(self, phone_data, lm_type):
        # 根据不同的地标类型调整时间
        start, end = phone_data
        start_time = int(start) / self.sample_rate * 1000
        end_time = int(end) / self.sample_rate * 1000
        if lm_type in ['+b', '+f', '+g', '+p', '+s', '+v']:
            return start_time  # onset通常在音素开始时
        elif lm_type in ['-b', '-f', '-g', '-p', '-s', '-v']:
            return end_time  # offset通常在音素结束时
        return start_time

    def identify_landmarks(self, phone):
        # 根据音素类型映射到声学地标
        stop_landmarks = ['+b', '-b']
        affricate_landmarks = ['+f', '-f', '+b', '-b']
        fricative_landmarks = ['+f', '-f']  # 清摩擦音
        voiced_fricative_landmarks = ['+v', '-v']  # 浊摩擦音
        nasal_landmarks = ['+s', '-s']
        vowel_landmarks = ['+g', '-g', '+p', '-p']

        stops = ['b', 'd', 'g', 'p', 't', 'k', 'dx', 'q']
        affricates = ['jh', 'ch']
        fricatives = ['s', 'sh', 'f', 'th']  # 清摩擦音
        voiced_fricatives = ['z', 'zh', 'v', 'dh']  # 浊摩擦音
        nasals = ['m', 'n', 'ng', 'em', 'en', 'eng', 'nx']
        vowels = ['iy', 'ih', 'eh', 'ey', 'ae', 'aa', 'aw', 'ay', 'ah', 'ao', 'oy', 'ow', 'uh', 'uw', 'ux', 'er', 'ax', 'ix', 'axr', 'ax-h']

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

    def print_landmarks(self):
        for lm, times in self.landmarks.items():
            print(f"{lm}: {times}")

# 使用示例
detector = AcousticLandmarkDetector('path_to_your_file.txt', 16000)
landmarks = detector.process_phones()
detector.print_landmarks()
