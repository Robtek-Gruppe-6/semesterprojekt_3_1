from control import *
from decoding import decoder
from filter import fil
from speaker import spk
from microphone import micro
from plotting import plot
from UI import ui
from datalink import datalinker
from dataframer import framer



def main():
    start_byte = False
    counter = 0
    len1_bool = False
    len2_bool = False
    crc1_bool = False
    crc2_bool = False
    counting_done = False
    data = ""
    length_val = 255
    
    #framer.input_binary()

    try:
        for audio_chunk in micro.capture_audio():
            filtered_chunk = fil.butter_bandpass(audio_chunk)
            frequencies, magnitude = fil.analyze_frequency(filtered_chunk)

            
            #binary_val = decoder.process_chunk(frequencies, magnitude)
            binary_val = int(input("input: "))
            

            if binary_val == 0xA and not start_byte:  # Start byte detection
                print("Start-byte detected.")
                start_byte = True
                continue

            if start_byte:
                if not len1_bool:  # First length byte
                    len1 = binary_val
                    if(len1 != None):
                        len1_bool = True
                        print(f"Length byte 1 received: {len1}")
                elif not len2_bool:  # Second length byte
                    len2 = binary_val
                    if(len2 != None):
                        length_val = (len1 << 4) | len2  # Combine length bytes
                        len2_bool = True
                        print(f"Length byte 2 received: {len2}, Total length: {length_val}")
                elif counter < length_val:  # Collect data based on length
                    if(binary_val != None):
                        data += str(binary_val)  # Append as hex string
                        counter += 1

                if counter == length_val and not counting_done:  # Stop when all data is received
                    print(f"Data collection complete: {data}")
                    counting_done = True
                    continue

                if counting_done:
                    if not crc1_bool:  # First length byte
                        crc1 = binary_val
                        if(crc1 != None):
                            crc1_bool = True
                            print(f"CRC byte 1 received: {crc1}")
                    elif not crc2_bool:  # Second length byte
                        crc2 = binary_val
                        if(crc2 != None):
                            crc_val = (crc1 << 4) | crc2  # Combine length bytes
                            crc2_bool = True
                            print(f"CRC byte 2 received: {crc2}, CRC value: {crc_val}")
                            continue

                if crc2_bool and binary_val == 0xB:
                    print("Stop byte detetcted: Data-frame complete.")
                    print(f"A{length_val}" + f"{data}" + f"{crc_val}B")
                    actual_crc = datalinker.CRC8(int(data))
                    print(f"{crc_val}" + f"{actual_crc}")

                    if(crc_val == actual_crc):
                        print("CRC matches.")

                    break

                    

            
            
            
                
           
           #if binary_val is not None:
           #    result = datalinker.receive_data(binary_val)
           #    if result:
           #         
           #         collected_data, data_length = result
           #         print("Collected Data:", [bin(int(b, 2))[2:].zfill(4) for b in collected_data])
           #         print("Data Length:", data_length)
           
           
           
    finally:
        micro.close()
        
        


if __name__ == "__main__":
    #ui.run_example() #UI example code
    #ui.run_protocol() #Runs the movementProtocol but it needs to display that into the UI SO NOT DONE!
    main()
    




