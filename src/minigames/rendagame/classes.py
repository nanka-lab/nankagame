import pygame as pg
from pygame.locals import *
from . import setup
from . import consts as c
from ...data import consts as cc
from ... import state
import os

def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', '.jpg', '.bmp', '.gif')):
        graphics = {}
        for pic in os.listdir(directory):
            name, ext = os.path.splitext(pic)
            if ext.lower() in accept:
                img = pg.image.load(os.path.join(directory, pic))
                if img.get_alpha():
                    img = img.convert_alpha()
                else:
                    img = img.convert()
                    img.set_colorkey(colorkey)
                graphics[name] = img
        return graphics

def load_all_music(directory):
    music_list = {}
    for music in os.listdir(directory):
        name, ext = os.path.splitext(music)
        music_path = os.path.join(directory, music)
        music_list[name] = music_path
    return music_list

class Control():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.done = False
        self.keys = pg.key.get_pressed()
        self.clock = pg.time.Clock()
        self.fps = 120
        self.current_time = 0
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_status(self, state_dict, state_name):
        self.state_dict = state_dict
        self.state_name = state_name
        self.state = self.state_dict[self.state_name]

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)
        if not self.done:
            self.done = self.state.persist[c.GAME_FINISH]
    
    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                
    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
        return self.state.persist[c.GAME_CLEAR]
    

class State():
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.first = True
        self.next = None
        self.persist = {c.GAME_CLEAR: False,
                        c.GAME_FINISH: False}
    
    def cleanup(self):
        self.done = False
        self.first = True
        return self.persist    
    
    def draw_button(self, **kwargs):
        screen = kwargs.get("screen")
        font_path = kwargs.get("font_path", state.font_path)
        font_size = kwargs.get("font_size", 28)
        text = kwargs.get("text", "default_text")
        text_color = kwargs.get("text_color", cc.BLACK)
        text_x = kwargs.get("text_x", cc.WINDOW_WIDTH // 2)
        text_y = kwargs.get("text_y", cc.WINDOW_HEIGHT // 2 + 25)
        button_color = kwargs.get("button_color", cc.GREEN)
        button_x = kwargs.get("button_x", cc.WINDOW_WIDTH // 2 - 100)
        button_y = kwargs.get("button_y", cc.WINDOW_HEIGHT // 2)
        button_width = kwargs.get("button_width", 200)
        button_height = kwargs.get("button_height", 50)
        
        button = pg.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        button_font = pg.font.Font(font_path, font_size)
        button_text = button_font.render(button_text, True, button_text_color)
        button_text_rect = button_text.get_rect(center = (text_x, text_y))
        screen.blit(button_text, buttton_text_rect)

class Start(State):
    def __init__(self):
        State.__init__(self)
        persist = {c.GAME_CLEAR: False,
                   c.GAME_FINISH: False}
        self.startup(0.0, persist)
    
    def startup(self, current_time, persist):
        self.next = c.COUNT_DOWN
        self.last_enter_pushed = True
        self.persist = persist

    def update(self, screen, keys, current_time):
        self.draw(screen)
        self.handle_event(keys)
    
    def handle_event(self, keys):
        if keys[K_RETURN] and not self.last_enter_pushed:
            self.done = True
        self.last_enter_pushed = keys[K_RETURN]

    def draw(self, screen):
        screen.fill(cc.BLACK)

        back_ground_image = setup.GFX["level_1_4"]
        screen.blit(back_ground_image, (0,0))

        #タイトル作ります
        title_font = pg.font.Font(state.font_path, 74) #タイトルを描画するフォントを設定
        title_text = title_font.render(c.GAME_TITLE, True, cc.RED)
        title_text_rect = title_text.get_rect(center = (cc.WINDOW_WIDTH // 2 , cc.WINDOW_HEIGHT // 2 - 150))
        screen.blit(title_text, title_text_rect)

        message_font = pg.font.Font(state.font_path, 74) #タイトルを描画するフォントを設定
        message_text = message_font.render("〜燃えろ俺の指先〜", True, cc.RED)
        message_text_rect = message_text.get_rect(center = (cc.WINDOW_WIDTH // 2 , cc.WINDOW_HEIGHT // 2 - 50))
        screen.blit(message_text, message_text_rect)

        message1_font = pg.font.Font(state.font_path, 60) #タイトルを描画するフォントを設定
        message1_text = message1_font.render("press ENTER to start", True, cc.WHITE)
        message1_text_rect = message1_text.get_rect(center = (cc.WINDOW_WIDTH // 2 , cc.WINDOW_HEIGHT // 2 + 40))
        screen.blit(message1_text, message1_text_rect)


class Count_down(State):
    def __init__(self):
        State.__init__(self)
        persist = None #不要説
        #self.startup(0.0, persist)
        
    def startup(self, current_time, persist):
        self.next = c.PLAY
        self.count = 3
        self.past_time = None
        self.first = True
        self.wait_seconds = 1 * cc.SECOND
        self.persist = persist

    def update(self, screen, keys, current_time):
        self.draw(screen)
        self.count_timer(current_time)
    
    def count_timer(self, current_time):
        if self.first:
            self.past_time = current_time
            self.first = False
        elapsed_time = current_time - self.past_time
        if elapsed_time > self.wait_seconds:
            self.count -= 1
            self.past_time = current_time
        if self.count < 0:
            self.done = True

    def draw(self, screen):
        screen.fill(cc.BLACK)
        title_font = pg.font.Font(state.font_path, 74) #タイトルを描画するフォントを設定
        #0->start
        if self.count <= 0:
            title_text = title_font.render("スタート!", True, cc.WHITE)
        #3,2,1まで
        else:
            title_text = title_font.render(str(self.count), True, cc.WHITE)
        title_text_rect = title_text.get_rect(center = (cc.WINDOW_WIDTH // 2 , cc.WINDOW_HEIGHT // 2 - 150))
        screen.blit(title_text, title_text_rect)

class Play(State):
    def __init__(self):
        State.__init__(self)
        persist = None #不要説
        #self.startup(0.0, persist)

    def startup(self, current_time, persist):
        self.next = c.RESULT
        self.count = 0
        self.last_pressed = None
        self.goal = 210
        self.time_limit = 20 * cc.SECOND
        self.remaining_time = self.time_limit
        self.past_time = None
        self.clear = False
        self.persist = persist
    
    def update(self, screen, keys, current_time):
        self.count_timer(current_time)
        self.handle_event(keys)
        self.draw(screen)
        self.persist[c.GAME_CLEAR] = self.clear
    
    def handle_event(self, keys):
        pressed = keys[K_SPACE]
        if keys[K_SPACE] and not self.last_pressed:
            self.count += 1
        self.last_pressed = pressed
        if self.count == self.goal:
            self.clear = True
            self.done = True
    
    def count_timer(self, current_time):
        if self.first:
            self.past_time = current_time
            self.first = False
        self.remaining_time -= current_time - self.past_time
        self.past_time = current_time
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.done = True
    
    def draw(self, screen):
        screen.fill(cc.BLACK)

        title_font = pg.font.Font(state.font_path, 74)
        title_text = title_font.render(f"残り時間: {(self.remaining_time / cc.SECOND):.2f}", True, cc.WHITE)
        title_text_render = title_text.get_rect(center = (cc.WINDOW_WIDTH // 2 , cc.WINDOW_HEIGHT // 2 - 150))
        screen.blit(title_text, title_text_render)

        count_font = pg.font.Font(state.font_path, 70)
        count_text = count_font.render(f"現在: {self.count}回  目標: {self.goal}", True, cc.WHITE)
        count_text_render = count_text.get_rect(center = (cc.WINDOW_WIDTH // 2, cc.WINDOW_HEIGHT // 2 + 190))
        screen.blit(count_text, count_text_render)


class Result(State):
    def __init__(self):
        State.__init__(self)
        persist = None #不要説
        #self.startup(0.0, persist)
    
    def startup(self, current_time, persist):
        self.next = c.START
        self.persist = persist
        self.game_clear = self.persist[c.GAME_CLEAR]


    def update(self, screen, keys, current_time):
        self.draw(screen)
        self.handle_event(keys)
    
    def handle_event(self, keys):
        if keys[K_RETURN] and self.persist[c.GAME_CLEAR]:
            self.persist[c.GAME_FINISH] = True
        elif keys[K_RETURN] and not self.persist[c.GAME_CLEAR]:
            self.done = True
    def draw(self, screen):
        screen.fill(cc.BLACK)

        if self.game_clear:
            title_font = pg.font.Font(state.font_path, 74)
            title_text = title_font.render("ゲームクリア", True, cc.WHITE)
            title_text_render = title_text.get_rect(center = (cc.WINDOW_WIDTH // 2, cc.WINDOW_HEIGHT // 2 - 150))
            screen.blit(title_text, title_text_render)

            message_font = pg.font.Font(state.font_path, 50)
            message_text = message_font.render("enterキーでマップに戻ります", True, cc.WHITE)
            message_text_render = message_text.get_rect(center = (cc.WINDOW_WIDTH // 2, cc.WINDOW_HEIGHT // 2 + 150))
            screen.blit(message_text, message_text_render)
        else:
            title_font = pg.font.Font(state.font_path, 74)
            title_text = title_font.render("失敗 (´・ω・`)", True, cc.WHITE)
            title_text_render = title_text.get_rect(center = (cc.WINDOW_WIDTH // 2, cc.WINDOW_HEIGHT // 2 - 150))
            screen.blit(title_text, title_text_render)

            # テキストを分割
            message_lines = [
                "最初からやり直してね!", 
                "enterキーを押すとタイトルに戻るよ ( $ _ $ ) → ポチッ"
            ]
            # 各行のフォントをレンダリングし、それぞれの位置を調整
            y_offset = 150  # 最初の行のY座標
            line_spacing = 50  # 行間のスペース
            message_font = pg.font.Font(state.font_path, 36)
            for i, line in enumerate(message_lines):
                message_text = message_font.render(line, True, cc.WHITE)
                message_text_rect = message_text.get_rect(center=(cc.WINDOW_WIDTH // 2, cc.WINDOW_HEIGHT // 2 + y_offset + i * line_spacing))
                screen.blit(message_text, message_text_rect)



