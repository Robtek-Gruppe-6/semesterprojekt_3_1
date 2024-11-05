clear all;

% Load the CSV file
audio_data = csvread('audio_data.csv');

% Flatten the matrix into a single vector
audio_data_flattened = audio_data(:);  % Convert the matrix to a single column vector

% Define the sample rate
rate = 44100;  % Sample rate in Hz
chunk_size = 1024;
cutoff_freq = 675;
filter_order = 8; %Find ud af hvilken order det skal være via matematik




% Create a time vector for the x-axis
time = (0:length(audio_data_flattened)-1) / rate;  % Time vector in seconds

% Plot the raw audio data with time on the x-axis
figure;
plot(time, audio_data_flattened);
xlabel('Time (seconds)');
ylabel('Amplitude');
title('Raw Audio Data');

[b, a] = butter(filter_order, cutoff_freq / (rate / 2), 'high');  % Normalized cutoff frequency
filtered_audio_data = filter(b, a, audio_data_flattened);

num_chunks = size(audio_data, 1);
fft_data_matrix = zeros(chunk_size, num_chunks);

%Hamming - måske hanning, hvis der er leakage
hamming_window = hamming(chunk_size);




for i = 1:num_chunks
    % Get the current chunk
    current_chunk = audio_data(i,:);
    
    filtered_chunk = filter(b, a, current_chunk);
    
    %Hamming ser ud til at 'flade
    windowed_chunk = filtered_chunk .*hamming_window.';
    
    % Current chunk hvis uden hamming ellers windowed
    fft_result = fft(windowed_chunk);
    
    % Store the FFT magnitude
    fft_data_matrix(:, i) = abs(fft_result);
end

average_magnitude = mean(fft_data_matrix, 2);
% Limit to the first half of the spectrum (positive frequencies)
average_magnitude = average_magnitude(1:floor(chunk_size/2));

frequency_resolution = rate / chunk_size;
frequencies = (0:floor(chunk_size/2)-1) * frequency_resolution;  % Frequency axis (in Hz)



% Plot the frequency domain graph
figure;
plot(frequencies, average_magnitude);
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Frequency Domain Representation of Audio Data');
