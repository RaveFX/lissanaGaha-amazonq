import pygame
import os
import sys

def test_audio():
    print("Testing PyGame audio functionality...")
    
    # Initialize pygame
    pygame.init()
    
    # Check if mixer module is available
    if not pygame.mixer:
        print("Error: pygame.mixer module not available!")
        return False
    
    # Initialize mixer
    try:
        pygame.mixer.init()
        print("Mixer initialized successfully")
    except pygame.error as e:
        print(f"Error initializing mixer: {e}")
        return False
    
    # Check if mixer is initialized
    if not pygame.mixer.get_init():
        print("Error: Mixer failed to initialize!")
        return False
    
    print(f"Mixer initialized with frequency={pygame.mixer.get_init()[0]}Hz, format={pygame.mixer.get_init()[1]}, channels={pygame.mixer.get_init()[2]}")
    
    # Get the absolute path to the assets directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, 'assets')
    
    # Check if assets directory exists
    if not os.path.isdir(assets_dir):
        print(f"Error: Assets directory not found at {assets_dir}")
        print("Creating assets directory...")
        try:
            os.makedirs(assets_dir, exist_ok=True)
            print(f"Created assets directory at {assets_dir}")
        except Exception as e:
            print(f"Error creating assets directory: {e}")
            return False
    
    # List files in assets directory
    print(f"\nFiles in assets directory ({assets_dir}):")
    try:
        files = os.listdir(assets_dir)
        if not files:
            print("  No files found in assets directory")
        else:
            for file in files:
                print(f"  - {file}")
    except Exception as e:
        print(f"Error listing files: {e}")
    
    # Check for required sound files
    required_sounds = ['climb.wav', 'slip.wav', 'fall.wav', 'hit.wav', 'win.wav']
    missing_sounds = []
    
    print("\nChecking for required sound files:")
    for sound_file in required_sounds:
        sound_path = os.path.join(assets_dir, sound_file)
        if os.path.isfile(sound_path):
            print(f"  ✓ {sound_file} found")
            
            # Try to load the sound
            try:
                sound = pygame.mixer.Sound(sound_path)
                print(f"    - Successfully loaded {sound_file}")
                
                # Try to play the sound
                channel = sound.play()
                if channel is not None:
                    print(f"    - Successfully played {sound_file}")
                else:
                    print(f"    - Warning: Could not play {sound_file} (no channel available)")
                
                # Wait a moment to hear the sound
                pygame.time.wait(500)
                
            except Exception as e:
                print(f"    - Error loading {sound_file}: {e}")
        else:
            print(f"  ✗ {sound_file} not found")
            missing_sounds.append(sound_file)
    
    if missing_sounds:
        print(f"\nMissing sound files: {', '.join(missing_sounds)}")
        print("Please add these files to the assets directory.")
    else:
        print("\nAll required sound files are present.")
    
    # Check system audio configuration
    print("\nSystem audio information:")
    try:
        import subprocess
        result = subprocess.run(['which', 'pulseaudio'], capture_output=True, text=True)
        print(f"PulseAudio available: {'Yes' if result.returncode == 0 else 'No'}")
        
        result = subprocess.run(['which', 'aplay'], capture_output=True, text=True)
        print(f"ALSA aplay available: {'Yes' if result.returncode == 0 else 'No'}")
    except Exception as e:
        print(f"Error checking system audio: {e}")
    
    pygame.quit()
    return True

if __name__ == "__main__":
    test_audio()
