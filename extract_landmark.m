% set path
audioFolderPath = 'C:\Users\z5459037\Downloads\segment_data\dev'; 
outputFilePath = 'C:\Users\z5459037\OneDrive - UNSW\桌面\dev.txt'; 

errorFilePath = 'C:\Users\z5459037\OneDrive - UNSW\桌面\dev_error.txt';


audioFiles = dir(fullfile(audioFolderPath, '*.wav')); % 假设音频文件的扩展名为.wav


fileID = fopen(outputFilePath, 'w');
errorFileID = fopen(errorFilePath, 'w'); % 打开错误日志文件以写入


for i = 1:length(audioFiles)
    audioFile = fullfile(audioFolderPath, audioFiles(i).name);
    
    try
      
        landmarkData = landmarks(audioFile);
        secondRowData = landmarkData(2, :);
        
     
        labelsMatrix = lm_labels(secondRowData);

      
        labelsList = {};
        for j = 1:size(labelsMatrix, 1)
            label = strtrim(labelsMatrix(j, :));
            if strcmp(label, 'F')
                continue; % 如果是" F"，则跳过
            elseif length(label) == 2 && label(1) == ' '
                label = label(2);
            end
            labelsList{end+1} = label;
        end

   
        outputLine = sprintf('%s %s', audioFiles(i).name(1:end-4), strjoin(labelsList, ' '));

       
        fprintf(fileID, '%s\n', outputLine);

    catch ME 
        fprintf('Error processing file: %s\n', audioFiles(i).name);
        fprintf('Error message: %s\n', ME.message);
        
    
        fprintf(errorFileID, '%s %s\n', audioFiles(i).name, ME.message);
    end
end


fclose(fileID);
fclose(errorFileID);