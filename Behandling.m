clear all;

% Load the CSV file
audio_data = csvread('audio_data.csv');

% Flatten the matrix into a single vector
audio_data_flattened = audio_data(:);  % Convert the matrix to a single column vector

% Define the sample rate
rate = 44100;  % Sample rate in Hz
chunk_size = 1024;

% Create a time vector for the x-axis
time = (0:length(audio_data_flattened)-1) / rate;  % Time vector in seconds

% Plot the raw audio data with time on the x-axis
figure;
plot(time, audio_data_flattened);
xlabel('Time (seconds)');
ylabel('Amplitude');
title('Raw Audio Data');



num_chunks = size(audio_data, 1);

fft_data_matrix = zeros(chunk_size, num_chunks);

for i = 1:num_chunks
    % Get the current chunk
    current_chunk = audio_data(i, :);
    
    % Perform the FFT on the current chunk
    fft_result = fft(current_chunk);
    
    % Store the FFT magnitude
    fft_data_matrix(:, i) = abs(fft_result);
end

average_magnitude = mean(fft_data_matrix, 2);
% Limit to the first half of the spectrum (positive frequencies)
average_magnitude = average_magnitude(1:floor(chunk_size/2));

frequency_resolution = rate / chunk_size;
frequencies = (0:floor(chunk_size/2)-1) * frequency_resolution;  % Frequency axis (in Hz)

% Perform the FFT on the entire audio data
%N = length(audio_data_flattened);  % Number of samples in the signal
%fft_data = fft(audio_data_flattened);  % FFT of the audio data

% Calculate the magnitude of the FFT and limit to the first half (positive frequencies)
%magnitude = abs(fft_data(1:floor(N/2)));

% Plot the frequency domain graph
figure;
plot(frequencies, average_magnitude);
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Frequency Domain Representation of Audio Data');
