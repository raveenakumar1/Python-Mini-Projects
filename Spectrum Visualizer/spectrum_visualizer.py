import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import time

#audio configuration settings for the spectrum analyzer
#we need to define how many samples to process at once
#and the format of the audio data we're working with
CHUNK = 1024 * 2             #how many samples to grab in each chunk of audio
FORMAT = pyaudio.paInt16     #using 16-bit integers for audio samples
CHANNELS = 1                 #only using one microphone channel
RATE = 44100                 #standard sample rate for audio

#create the visual display for our spectrum analyzer
#using a black background for that professional look
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

#initialize the audio system and prepare to find devices
p = pyaudio.PyAudio()

#check what audio devices are available on the system
#this helps us figure out what we can use for input
print("Available audio devices:")
print("=" * 50)
input_devices = []
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    print(f"{i}: {dev_info['name']} (Input channels: {dev_info['maxInputChannels']})")
    if dev_info['maxInputChannels'] > 0:
        input_devices.append((i, dev_info['name']))

print("=" * 50)
print(f"Found {len(input_devices)} input devices")

#now we try to open an audio stream for recording
#if we can't find a real microphone, we'll make fake test data
stream = None
device_info = None

if input_devices:
    #first try to use whatever windows says is the default microphone
    try:
        device_info = p.get_default_input_device_info()
        print(f"Trying default input device: {device_info['index']} - {device_info['name']}")
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_info['index'],
            frames_per_buffer=CHUNK
        )
        print("Successfully opened audio stream with default device!")
    except Exception as e:
        print(f"Failed to open stream with default device: {e}")
        
        #if the default device didn't work, try the first available one
        try:
            device_index, device_name = input_devices[0]
            print(f"Trying device {device_index}: {device_name}")
            
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK
            )
            print("Successfully opened audio stream with first available device!")
        except Exception as e2:
            print(f"Failed to open stream: {e2}")
            stream = None
else:
    print("No input devices found. Using test signal mode.")

#if we don't have a real microphone, we'll generate fake audio data
#this makes sure the visualizer works even without hardware
test_signal_freq = 440  #this is the A4 musical note frequency
test_signal_phase = 0   #we need to keep track of where we are in the wave

#function to create artificial audio data for testing
#this generates a sine wave with some harmonics added
def generate_test_signal():
    global test_signal_phase
    t = np.arange(CHUNK) / RATE
    signal = 16000 * np.sin(2 * np.pi * test_signal_freq * t + test_signal_phase)
    test_signal_phase += 2 * np.pi * test_signal_freq * CHUNK / RATE
    
    #add some harmonics to make the spectrum more interesting
    #real sounds have multiple frequencies not just one
    signal += 8000 * np.sin(2 * np.pi * 2 * test_signal_freq * t + test_signal_phase)
    signal += 4000 * np.sin(2 * np.pi * 3 * test_signal_freq * t + test_signal_phase)
    
    return signal.astype(np.int16)

#set up the visual display line that we'll animate
#this line will show the frequency spectrum moving in real time
x = np.linspace(0, RATE / 2, CHUNK)
line, = ax.semilogx(x, np.random.rand(CHUNK), 'c-', lw=2)

#configure how the graph looks and what it displays
#we want a logarithmic frequency scale because that's how humans hear
ax.set_xlim(20, RATE / 2)    #human hearing range is about 20Hz to 20kHz
ax.set_ylim(0, 255)          #amplitude scale from 0 to 255
ax.set_xlabel('Frequency [Hz]', color='white', fontsize=12)
ax.set_ylabel('Amplitude', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.grid(True, color='gray', linestyle='--', alpha=0.5)

#add a title that tells us if we're using real audio or test data
if stream is not None:
    title = 'Real-Time Audio Spectrum Analyzer (Live Input)'
else:
    title = 'Real-Time Audio Spectrum Analyzer (Test Signal)'
    
plt.title(title, color='cyan', fontsize=14, fontweight='bold')

#add a color bar to make it look more scientific and professional
#even though it's just for visual effect and doesn't represent real data
cmap = plt.cm.get_cmap('viridis')
norm = plt.Normalize(0, 255)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Intensity', color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

#this is the main function that runs repeatedly to update the display
#it gets called many times per second to create the animation
def update_plot(frame):
    global test_signal_freq
    
    try:
        if stream is not None:
            #read actual audio data from the microphone if available
            data = stream.read(CHUNK, exception_on_overflow=False)
            data_np = np.frombuffer(data, dtype=np.int16)
        else:
            #generate artificial audio data for testing purposes
            data_np = generate_test_signal()
            #slowly change the frequency to make the test more interesting
            test_signal_freq = 100 + 50 * np.sin(frame * 0.05)
        
        #apply a mathematical window function to the audio data
        #this reduces artifacts in the frequency analysis
        windowed = data_np * np.hanning(len(data_np))
        
        #perform the fast fourier transform to convert to frequency domain
        #this is the mathematical magic that lets us see frequencies
        fft = np.abs(np.fft.fft(windowed).real)
        
        #normalize the data to fit nicely on our display
        #we add a tiny amount to avoid division by zero errors
        fft = fft[:CHUNK]  
        fft = fft / (np.max(fft) + 0.001) * 255
        
        #update the visual display with the new frequency data
        line.set_ydata(fft)
        
        #change the line color based on how loud the audio is
        #this adds visual interest to the display
        avg_freq = np.mean(fft)
        color_val = avg_freq / 255.0
        line.set_color(plt.cm.viridis(color_val))
        
        return line,
    except Exception as e:
        print(f"Error: {e}")
        return line,

#this ties our update function to the visual display
ani = animation.FuncAnimation(
    fig, 
    update_plot, 
    interval=15, 
    blit=True,
    cache_frame_data=False
)

#show the visualizer on screen
plt.tight_layout()
plt.show()

#clean up resources when we're done with the program
#this is important to avoid leaving audio devices locked
if stream is not None:
    stream.stop_stream()
    stream.close()
p.terminate()