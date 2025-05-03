import pygame

class TextInput:
    """
    A class for handling text input in Pygame.
    """
    def __init__(self, x, y, width, height, font, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)
        self.text = text
        self.font = font
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 500  # milliseconds
    
    def handle_event(self, event):
        """Handle events for text input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < 15:  # Limit text length
                self.text += event.unicode
            
            return True
        
        return False
    
    def update(self):
        """Update the cursor blink state."""
        self.cursor_timer += 1
        if self.cursor_timer >= self.cursor_blink_rate / 16.67:  # Convert ms to frames at 60fps
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        """Draw the text input box and text."""
        # Draw the rectangle
        border_color = (100, 100, 200) if self.active else (100, 100, 100)
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Render text
        text_surf = self.font.render(self.text, True, self.color)
        
        # Position text
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
        screen.blit(text_surf, text_rect)
        
        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            if cursor_x < self.rect.right - 5:
                pygame.draw.line(
                    screen, 
                    self.color, 
                    (cursor_x, self.rect.y + 5), 
                    (cursor_x, self.rect.bottom - 5), 
                    2
                )


class Button:
    """
    A class for creating buttons in Pygame.
    """
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
    
    def draw(self, screen):
        """Draw the button."""
        # Button colors
        bg_color = (60, 60, 60) if not self.hovered else (80, 80, 80)
        border_color = (200, 200, 200) if not self.hovered else (255, 255, 255)
        text_color = (255, 255, 255)
        
        # Draw button background
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)
        
        # Draw text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        """Check if mouse is hovering over button."""
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def check_click(self, pos):
        """Check if button was clicked."""
        if self.rect.collidepoint(pos):
            if self.action is not None:  # Check if action is not None
                return self.action
        return None