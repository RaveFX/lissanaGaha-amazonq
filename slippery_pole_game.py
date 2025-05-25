import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Pygame mixer initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize sound system: {e}")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POLE_WIDTH = 40
CLIMBER_WIDTH = 60
CLIMBER_HEIGHT = 80
COCONUT_SIZE = 30
GRAVITY = 0.2
CLIMB_SPEED = 2
SLIP_SPEED = 1
FALL_SPEED = 4
COCONUT_SPEED = 3
COCONUT_SPAWN_RATE = 60  # frames between coconut spawns

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lissana Gaha Nagima")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.load_assets()
        self.reset_game()

    def load_assets(self):
        # Get the absolute path to the assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, 'assets')
        print(f"Loading assets from: {assets_dir}")
        
        # Load images
        # Use placeholder colors if images aren't available
        try:
            self.background = pygame.image.load(os.path.join(assets_dir, 'background.png')).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print("Successfully loaded background image")
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.background = None
            
        try:
            self.pole_img = pygame.image.load(os.path.join(assets_dir, 'pole.png')).convert_alpha()
            self.pole_img = pygame.transform.scale(self.pole_img, (POLE_WIDTH, SCREEN_HEIGHT))
            print("Successfully loaded pole image")
        except Exception as e:
            print(f"Could not load pole image: {e}")
            self.pole_img = None
            
        try:
            self.climber_img = pygame.image.load(os.path.join(assets_dir, 'climber.png')).convert_alpha()
            self.climber_img = pygame.transform.scale(self.climber_img, (CLIMBER_WIDTH, CLIMBER_HEIGHT))
            print("Successfully loaded climber image")
        except Exception as e:
            print(f"Could not load climber image: {e}")
            self.climber_img = None
            
        try:
            self.coconut_img = pygame.image.load(os.path.join(assets_dir, 'coconut.png')).convert_alpha()
            self.coconut_img = pygame.transform.scale(self.coconut_img, (COCONUT_SIZE, COCONUT_SIZE))
            print("Successfully loaded coconut image")
        except Exception as e:
            print(f"Could not load coconut image: {e}")
            self.coconut_img = None
        
        # Re-initialize mixer with explicit settings
        pygame.mixer.quit()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        print("Re-initialized pygame mixer")
        
        # Create default sound objects
        self.climb_sound = None
        self.slip_sound = None
        self.fall_sound = None
        self.hit_sound = None
        self.win_sound = None
        
        # List files in assets directory
        print("Files in assets directory:")
        for file in os.listdir(assets_dir):
            if not file.endswith(":Zone.Identifier"):  # Skip Windows metadata files
                print(f"  - {file}")
        
        # Load each sound file individually with explicit error handling
        try:
            if os.path.exists(os.path.join(assets_dir, 'fall.wav')):
                self.fall_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'fall.wav'))
                self.fall_sound.set_volume(0.5)
                print("Successfully loaded fall.wav")
        except Exception as e:
            print(f"Error loading fall.wav: {e}")
            
        try:
            if os.path.exists(os.path.join(assets_dir, 'win.wav')):
                self.win_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'win.wav'))
                self.win_sound.set_volume(0.5)
                print("Successfully loaded win.wav")
        except Exception as e:
            print(f"Error loading win.wav: {e}")
            
        # Create placeholder sounds for missing files
        if not self.climb_sound:
            print("Creating placeholder for climb sound")
            self.climb_sound = self.create_placeholder_sound(frequency=440, duration=100)
            
        if not self.slip_sound:
            print("Creating placeholder for slip sound")
            self.slip_sound = self.create_placeholder_sound(frequency=220, duration=200)
            
        if not self.hit_sound:
            print("Creating placeholder for hit sound")
            self.hit_sound = self.create_placeholder_sound(frequency=110, duration=300)
            
    def create_placeholder_sound(self, frequency=440, duration=100):
        """Create a simple placeholder sound using numpy if available, otherwise return None"""
        try:
            import numpy as np
            sample_rate = 44100
            t = np.linspace(0, duration/1000, int(duration * sample_rate/1000), False)
            tone = np.sin(frequency * 2 * np.pi * t)
            tone = np.asarray([32767 * tone, 32767 * tone]).T.astype(np.int16)
            buffer = pygame.sndarray.make_sound(tone)
            buffer.set_volume(0.5)
            return buffer
        except ImportError:
            print("Numpy not available for placeholder sounds")
            return None
        except Exception as e:
            print(f"Error creating placeholder sound: {e}")
            return None

    def reset_game(self):
        self.game_over = False
        self.win = False
        self.score = 0
        self.pole_top = 50  # Top of the pole position
        self.pole_bottom = SCREEN_HEIGHT - 50  # Bottom of the pole position
        self.pole_height = self.pole_bottom - self.pole_top
        
        # Climber properties
        self.climber_x = SCREEN_WIDTH // 2 - CLIMBER_WIDTH // 2
        self.climber_y = SCREEN_HEIGHT - CLIMBER_HEIGHT - 50
        self.is_slipping = False
        self.slip_timer = 0
        self.balance_key_needed = None
        self.coconuts = []
        self.coconut_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.game_over or self.win:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    # Balance mechanic
                    if self.is_slipping:
                        if (self.balance_key_needed == 'A' and event.key == pygame.K_a) or \
                           (self.balance_key_needed == 'D' and event.key == pygame.K_d):
                            self.is_slipping = False
                            self.balance_key_needed = None
                            if self.slip_sound:
                                try:
                                    self.slip_sound.play()
                                except:
                                    pass

    def update(self):
        if self.game_over or self.win:
            return
            
        keys = pygame.key.get_pressed()
        
        # Climbing mechanic
        if keys[pygame.K_UP] and not self.is_slipping:
            self.climber_y -= CLIMB_SPEED
            if self.climb_sound:
                # Only play occasionally to avoid sound spam
                if random.random() < 0.05:
                    try:
                        self.climb_sound.play()
                    except:
                        pass
        
        # Random slipping mechanic
        if not self.is_slipping and random.random() < 0.01:
            self.is_slipping = True
            self.balance_key_needed = random.choice(['A', 'D'])
            if self.slip_sound:
                try:
                    self.slip_sound.play()
                except:
                    pass
        
        # Handle slipping
        if self.is_slipping:
            self.slip_timer += 1
            self.climber_y += SLIP_SPEED
            
            # If player doesn't balance in time, they fall
            if self.slip_timer > 60:  # 1 second at 60 FPS
                self.climber_y += FALL_SPEED
                if self.fall_sound and random.random() < 0.1:
                    try:
                        self.fall_sound.play()
                    except:
                        pass
                
                # Reset slip state after falling for a bit
                if self.slip_timer > 90:
                    self.is_slipping = False
                    self.balance_key_needed = None
                    self.slip_timer = 0
        
        # Spawn coconuts
        self.coconut_timer += 1
        if self.coconut_timer >= COCONUT_SPAWN_RATE:
            self.coconut_timer = 0
            if random.random() < 0.5:  # 50% chance to spawn a coconut
                coconut_x = random.randint(0, SCREEN_WIDTH)
                self.coconuts.append([coconut_x, 0])
        
        # Update coconuts
        for coconut in self.coconuts[:]:
            coconut[1] += COCONUT_SPEED
            
            # Check for collision with climber
            if (self.climber_x < coconut[0] < self.climber_x + CLIMBER_WIDTH and
                self.climber_y < coconut[1] < self.climber_y + CLIMBER_HEIGHT):
                self.coconuts.remove(coconut)
                self.climber_y += FALL_SPEED * 5  # Fall a significant amount
                if self.hit_sound:
                    try:
                        self.hit_sound.play()
                    except:
                        pass
            
            # Remove coconuts that go off screen
            if coconut[1] > SCREEN_HEIGHT:
                self.coconuts.remove(coconut)
        
        # Keep climber on the pole
        pole_center = SCREEN_WIDTH // 2
        self.climber_x = pole_center - CLIMBER_WIDTH // 2
        
        # Constrain climber to pole
        if self.climber_y < self.pole_top:
            self.climber_y = self.pole_top
            self.win = True
            if self.win_sound:
                try:
                    self.win_sound.play()
                except:
                    pass
        elif self.climber_y > self.pole_bottom - CLIMBER_HEIGHT:
            self.climber_y = self.pole_bottom - CLIMBER_HEIGHT
            self.game_over = True
        
        # Update score based on height climbed
        self.score = int((self.pole_bottom - self.climber_y - CLIMBER_HEIGHT) / self.pole_height * 100)

    def draw(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLUE)  # Sky blue background
        
        # Draw pole
        pole_x = SCREEN_WIDTH // 2 - POLE_WIDTH // 2
        if self.pole_img:
            self.screen.blit(self.pole_img, (pole_x, 0))
        else:
            pygame.draw.rect(self.screen, BROWN, (pole_x, 0, POLE_WIDTH, SCREEN_HEIGHT))
        
        # Draw climber
        if self.climber_img:
            self.screen.blit(self.climber_img, (self.climber_x, self.climber_y))
        else:
            pygame.draw.rect(self.screen, GREEN, (self.climber_x, self.climber_y, CLIMBER_WIDTH, CLIMBER_HEIGHT))
        
        # Draw coconuts
        for coconut in self.coconuts:
            if self.coconut_img:
                self.screen.blit(self.coconut_img, (coconut[0], coconut[1]))
            else:
                pygame.draw.circle(self.screen, BROWN, (coconut[0], coconut[1]), COCONUT_SIZE // 2)
        
        # Draw score
        score_text = self.font.render(f"Height: {self.score}%", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw balance prompt if slipping
        if self.is_slipping:
            balance_text = self.font.render(f"Press '{self.balance_key_needed}' to balance!", True, RED)
            self.screen.blit(balance_text, (SCREEN_WIDTH // 2 - balance_text.get_width() // 2, 50))
        
        # Draw game over or win screen
        if self.game_over:
            self.draw_message("Game Over! Press 'R' to restart", RED)
        elif self.win:
            self.draw_message("You Win! Press 'R' to play again", GREEN)
        
        pygame.display.flip()

    def draw_message(self, message, color):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        text = self.font.render(message, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
