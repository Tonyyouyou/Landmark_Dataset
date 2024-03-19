function extract_blandmark(rootDir, outputFileName)
    % 定义特定phonemes列表
    targetPhonemes = {'b', 'd', 'g', 'p', 't', 'k', 'dx', 'q', 'jh', 'ch'};
    
    % 打开输出文件
    outputFileID = fopen(outputFileName, 'w');
    
    % 遍历目录下的所有WAV文件
    wavFiles = dir(fullfile(rootDir, '**', '*.WAV'));

    for i = 1:length(wavFiles)
        wavFileName = fullfile(wavFiles(i).folder, wavFiles(i).name);
        txtFileName = strrep(wavFileName, '.WAV', '.PHN');
        
        % 调用landmarks函数提取landmarks
        landmarksMatrix = landmarks(wavFileName); % 假设返回的是三维矩阵
        times = landmarksMatrix(1, :) * 16000; % 转换时间到样本单位
        types = landmarksMatrix(2, :);
        
        % 读取对应的文本文件
        [phonemeStarts, phonemeEnds, phonemes] = read_phoneme_file(txtFileName, 16000);
        
        % 准备存储同一个文件中的所有符合条件的landmarks
        validLandmarksStr = [];
        
        % 遍历landmarks
        for j = 1:length(times)
            landmarkTime = times(j);
            landmarkType = types(j);
            % 对每个landmark检查是否在特定phoneme的时间范围
            if landmarkType == 3 || landmarkType == 4
                landmarkLabel = (landmarkType == 3) * 'b-' + (landmarkType == 4) * 'b+';
                for k = 1:length(phonemes)
                    if any(strcmp(phonemes{k}, targetPhonemes)) && ...
                        landmarkTime >= phonemeStarts(k) && landmarkTime <= phonemeEnds(k)
                        % 将符合条件的landmark添加到字符串中
      
                        validLandmarksStr = [validLandmarksStr sprintf(' %s:%d', landmarkLabel, landmarkTime)];
                        % 不再假设每个landmark只属于一个phoneme，因此不中断循环
                    end
                end
            end
        end
        % 如果找到了符合条件的landmarks，则输出到文件
        if ~isempty(validLandmarksStr)
            fprintf(outputFileID, '%s%s\n', wavFileName, validLandmarksStr);
        end
    end
    
    % 关闭输出文件
    fclose(outputFileID);
end


function [startTimes, endTimes, phonemes] = read_phoneme_file(txtFileName, sampleRate)
    % 打开文件
    fid = fopen(txtFileName, 'rt');
    if fid == -1
        error('无法打开文件：%s', txtFileName);
    end
    
    % 读取文件内容
    C = textscan(fid, '%d %d %s');
    fclose(fid);
    
    % 提取开始时间、结束时间和phoneme
    % 假定TIMIT标注文件中时间单位是采样点数，直接转换为对应的样本单位
    startTimes = C{1};
    endTimes = C{2};
    phonemes = C{3};
end

