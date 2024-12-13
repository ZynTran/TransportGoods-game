import pygame
import random

# Khởi tạo pygame
pygame.mixer.pre_init(frequency=44100 , size=-16 , channels=2 , buffer=512 )
pygame.init()

# Thiết lập màn hình trò chơi
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRANSPORT GOODS")

# Tải ảnh nền
background = pygame.image.load('background.jpeg').convert()  # Đảm bảo rằng ảnh của bạn tồn tại trong thư mục của dự án
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Thay đổi kích thước ảnh nền cho vừa màn hình
wait_background = pygame.image.load('wait_background2.png').convert()  # Đảm bảo rằng ảnh của bạn tồn tại trong thư mục của dự án
wait_background = pygame.transform.scale(wait_background, (WIDTH, HEIGHT))  # Thay đổi kích thước ảnh nền cho vừa màn hình

#Âm thanh
pygame.mixer.music.load("nhạc nền.mp3")
clock_sound=pygame.mixer.Sound('hết giờ.mp3')
bom_sound=pygame.mixer.Sound('bom1.mp3')
shield_sound=pygame.mixer.Sound('khiên.mp3')
pick_item=pygame.mixer.Sound('lấy hàng.mp3')
doubletime_sound=pygame.mixer.Sound('thêm thời gian.mp3')
break_sound=pygame.mixer.Sound('rác rơi trúng.mp3')
fail_sound=pygame.mixer.Sound('thua.mp3')
doublescore_sound=pygame.mixer.Sound('x2 điểm.mp3')
goal_sound=pygame.mixer.Sound('đến đích.mp3')
truck_sound=pygame.mixer.Sound('xe.mp3')
click_sound=pygame.mixer.Sound('click.mp3')
break_shield=pygame.mixer.Sound('hết khiên.mp3')

# Lấy các kênh âm thanh để phát âm thanh riêng biệt
channel_shield = pygame.mixer.Channel(0)  # Kênh cho nhạc nền
channel_pick_item = pygame.mixer.Channel(1)  # Kênh cho âm thanh đồng hồ
channel_goal = pygame.mixer.Channel(2)  # Kênh cho âm thanh hiệu ứng
channel_bom = pygame.mixer.Channel(3)
channel_doubletime = pygame.mixer.Channel(4)
channel_break = pygame.mixer.Channel(5)
channel_doublescore = pygame.mixer.Channel(6)
channel_truck = pygame.mixer.Channel(7)

# Màu sắc
BLACK = (0, 0, 0)
RED = (255, 0, 0)
yellow_white = (255, 186, 60)

# Khởi tạo đồng hồ và font chữ
clock = pygame.time.Clock()#Tạo một đối tượng Clock để điều khiển tốc độ khung hình của trò chơi (FPS).
font = pygame.font.SysFont("JosefinSans-VariableFont_wght.ttf", 50)#Tạo đối tượng font sử dụng phông chữ JosefinSans-VariableFont_wght từ tệp ttf, kích thước 30 để hiển thị văn bản trên màn hình.

# Tạo nút Play
class Play_button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(477, 329, 100, 100) #477 tọa độ x, 329 tọa độ y, 100*100 kích thước rect

class Guide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(741, 636, 212, 38)

class Escape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(875, 14, 56, 56)


menu_background = pygame.image.load('menu.png')  # Đảm bảo rằng ảnh của bạn tồn tại trong thư mục của dự án
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))  # Thay đổi kích thước ảnh nền cho vừa màn hình
class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = menu_background
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.alpha = 0  # Độ mờ (alpha) ban đầu là 255 (đầy đủ)

    def update(self):
        #self.rect.y -= 2  # Di chuyển chữ lên trên màn hình
        if(self.alpha<255):
            self.alpha += 35  # Giảm độ mờ dần dần
            #self.rect.y -= 2
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ của chữ

# Màn hình đợi
def wait_screen():
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    all_sprites = pygame.sprite.Group()
    menus= pygame.sprite.Group()
    summenus= pygame.sprite.Group()
    # Tạo các sprite cố định
    play_button = Play_button()
    guide = Guide()
    all_sprites.add(play_button, guide)

    # Biến kiểm soát trạng thái hiển thị menu
    showing_menu = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_button.rect.collidepoint(mouse_x, mouse_y):  # Kiểm tra nếu người chơi nhấn vào nút Play
                    click_sound.play()
                    return  # Bắt đầu trò chơi
                elif guide.rect.collidepoint(mouse_x, mouse_y):
                    menu=Menu()
                    escape=Escape()
                    summenus.add(menu, escape)
                    menus.add(menu)
                    showing_menu = True
                    click_sound.play()
                elif showing_menu == True and escape.rect.collidepoint(mouse_x, mouse_y):
                    summenus.empty()
                    menus.empty()
                    showing_menu = False
                    click_sound.play()

        # Vẽ màn hình đợi
        screen.blit(wait_background, (0, 0))
        all_sprites.update()
        menus.update()
        summenus.update()
        menus.draw(screen)

        pygame.display.flip()
        clock = pygame.time.Clock()
        clock.tick(60)  # Giới hạn khung hình ở mức 60 FPS

# Lớp điểm đích (ô xanh)
warehouse_image = pygame.image.load("warehouse.png")  # Thay "item.png" bằng đường dẫn tới file hình ảnh của bạn
warehouse_image = pygame.transform.scale(warehouse_image, (130, 90))  # Thay đổi kích thước hình ảnh nếu cần
class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = warehouse_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(88, WIDTH - 150)
        self.rect.y = random.randint(88, HEIGHT - 110)

    def reset_position(self):
        """ Đặt lại vị trí của ô xanh """
        self.rect.x = random.randint(88, WIDTH - 150)
        self.rect.y = random.randint(88, HEIGHT - 110)

# Lớp nhân vật
xe_image = pygame.image.load("truck.png")  # Thay "item.png" bằng đường dẫn tới file hình ảnh của bạn
xe_image = pygame.transform.scale(xe_image, (50, 100))  # Thay đổi kích thước hình ảnh nếu cần
xehang_image = pygame.image.load("truck_item.png")  # Thay "item.png" bằng đường dẫn tới file hình ảnh của bạn
xehang_image = pygame.transform.scale(xehang_image, (50, 100))  # Thay đổi kích thước hình ảnh nếu cần
xekhien_image = pygame.image.load("truck_khiên.png")  # Thay "item.png" bằng đường dẫn tới file hình ảnh của bạn
xekhien_image = pygame.transform.scale(xekhien_image, (100, 100))  # Thay đổi kích thước hình ảnh nếu cần
xehangkhien_image = pygame.image.load("truck_item_khiên.png")  # Thay "item.png" bằng đường dẫn tới file hình ảnh của bạn
xehangkhien_image = pygame.transform.scale(xehangkhien_image, (100, 100))  # Thay đổi kích thước hình ảnh nếu cần
class Character(pygame.sprite.Sprite):#cách khai báo một lớp (class) trong Python kế thừa từ lớp Sprite của thư viện Pygame.
    #pygame.sprite.Sprite là một lớp có sẵn trong Pygame, dùng để quản lý và xử lý các đối tượng đồ họa (sprites) trong trò chơi
    def __init__(self):
        super().__init__()
        self.image = xe_image # Khởi tạo hình ảnh của nhân vật
        self.rect = self.image.get_rect() # Lấy rect từ hình ảnh để quản lý vị trí    
        self.rect.center = (WIDTH // 2, HEIGHT - 60)#Đặt vị trí ban đầu cho nhân vật
        self.speed = 5
        self.angle = 0  # Biến góc quay
        self.has_item = False  # Kiểm tra xem nhân vật có mang hàng không
        self.has_doublescore = False  # Kiểm tra trạng thái nhân đôi điểm
        self.has_shield = False  # Kiểm tra trạng thái giáp
        self.has_doubletime = False  # Kiểm tra trạng thái nhân đôi thời gian
        self.has_boom = False
        self.is_moving=False

    def update(self):
        keys = pygame.key.get_pressed()
        pressing=False
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.angle = 90  # Quay sang trái
            pressing = True
            #channel_truck.stop()
        #else: channel_truck.play(truck_sound)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.angle = -90  # Quay sang phải
            pressing = True
           # channel_truck.play(truck_sound)
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.angle = 0  # Quay lên
            pressing = True
           # channel_truck.play(truck_sound)
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.angle = 180  # Quay xuống
            pressing = True
            #channel_truck.play(truck_sound)

        if(pressing and not self.is_moving):
            channel_truck.set_volume(0.4)
            channel_truck.play(truck_sound, loops=-1, maxtime=0)
            self.is_moving= True
        elif(not pressing and self.is_moving):
            channel_truck.stop()
            self.is_moving = False

        # Nếu nhân vật mang hàng, không thay đổi góc quay mà chỉ thay đổi hình ảnh
        if self.has_item and not self.has_shield:
            #pick_item.play()
            self.image = xehang_image
        elif self.has_item and self.has_shield:
            self.image = xehangkhien_image
        elif not self.has_item and self.has_shield:
            self.image = xekhien_image
        else:
            self.image = xe_image
        # Quay hình ảnh dựa trên góc hiện tại
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Cập nhật lại vị trí sau khi xoay
        
        # Kiểm tra hết thời gian nhân đôi điểm
        if self.has_doublescore and pygame.time.get_ticks() - self.time_doublescore > 10000:  # 50 giây
            self.has_doublescore = False
    
    def deliver_item(self, goal):
        if self.rect.colliderect(goal.rect) and self.has_item:
            self.has_item = False  # Đã giao hàng
            #doubletime_sound.play()
            return True
        return False
    
    def pick_up_doublescore(self):
        self.has_doublescore = True
        self.time_doublescore=pygame.time.get_ticks()
    
    def pick_up_shield(self):
        """Kích hoạt giáp và duy trì vô thời hạn cho đến khi va chạm"""
        self.has_shield = True  # Kích hoạt giáp

    def activity_shield(self):
        if self.has_shield:
            self.has_shield=False
            return False
        return True

# Lớp vật cản
obstacle1_image = pygame.image.load("obstacle1.png")  
obstacle1_image = pygame.transform.scale(obstacle1_image, (41, 56)) 
obstacle2_image = pygame.image.load("obstacle2.png") 
obstacle2_image = pygame.transform.scale(obstacle2_image, (50, 50)) 
obstacle3_image = pygame.image.load("obstacle3.png")  
obstacle3_image = pygame.transform.scale(obstacle3_image, (38, 57))  
obstacle4_image = pygame.image.load("obstacle4.png")  
obstacle4_image = pygame.transform.scale(obstacle4_image, (57, 38))  
obstacle5_image = pygame.image.load("obstacle5.png") 
obstacle5_image = pygame.transform.scale(obstacle5_image, (50, 50)) 
obstacle6_image = pygame.image.load("obstacle6.png") 
obstacle6_image = pygame.transform.scale(obstacle6_image, (56, 38)) 
obstacle7_image = pygame.image.load("obstacle7.png")
obstacle7_image = pygame.transform.scale(obstacle7_image, (40, 56))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,speed,temporary):
        super().__init__()
        if(temporary==1):
            self.image=obstacle1_image
        elif(temporary==2):
            self.image=obstacle2_image
        elif(temporary==3):
            self.image=obstacle3_image
        elif(temporary==4):
            self.image=obstacle4_image
        elif(temporary==4):
            self.image=obstacle5_image
        elif(temporary==4):
            self.image=obstacle6_image
        else:
            self.image=obstacle7_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-400, -50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 50)
            self.rect.y = random.randint(-400, -50)

# Lớp vật phẩm cứu viện *2 điểm
doublescore_image = pygame.image.load("doublescore.png")  # Thay "item.png" bằng đường dẫn tới file hình ảnh của bạn
doublescore_image = pygame.transform.scale(doublescore_image, (50, 50))  # Thay đổi kích thước hình ảnh nếu cần
class Doublescore(pygame.sprite.Sprite):
    def __init__(self,speed):
        super().__init__()
        self.image = doublescore_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-400, -50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

label_doublescore_image = pygame.image.load("doublescore.png")
label_doublescore_image = pygame.transform.scale(label_doublescore_image, (55, 55))
class Label_doublescore (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = label_doublescore_image
        self.rect = self.image.get_rect()
        self.rect.x = 395
        self.rect.y = 17
        self.alpha = 0  # Độ mờ (alpha) ban đầu là 255 (đầy đủ)

    current_time1=pygame.time.get_ticks()
    def update(self):
        if(self.alpha<255):
            self.alpha = min(255, self.alpha+ 35)  # Giảm độ mờ dần dần
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ của chữ

# Lớp vật phẩm cứu viện thêm thời gian
clock_image = pygame.image.load("clock.png")  
clock_image = pygame.transform.scale(clock_image, (50, 50))  # Thay đổi kích thước hình ảnh nếu cần
class Doubletime(pygame.sprite.Sprite):
    def __init__(self,speed):
        super().__init__()
        self.image = clock_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-400, -50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Lớp vật phẩm cứu viện giáp
shield_image = pygame.image.load("shield.png")  
shield_image = pygame.transform.scale(shield_image, (50, 50))  # Thay đổi kích thước hình ảnh nếu cần
class Shield(pygame.sprite.Sprite):
    def __init__(self,speed):
        super().__init__()
        self.image = shield_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-400, -50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Lớp vật phẩm cứu viện bơm
bom_image = pygame.image.load("bom.png")  
bom_image = pygame.transform.scale(bom_image, (50, 50))  # Thay đổi kích thước hình ảnh nếu cần
class Boom(pygame.sprite.Sprite):
    def __init__(self,speed):
        super().__init__()
        self.image = bom_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-400, -50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Lớp vật phẩm (hàng hóa)
item_image = pygame.image.load("item.png") 
item_image = pygame.transform.scale(item_image, (50, 50))  # Thay đổi kích thước hình ảnh nếu cần
class Item(pygame.sprite.Sprite):
    def __init__(self, goal_rect):
        super().__init__()
        self.image = item_image
        self.rect = self.image.get_rect()
        if goal_rect.centerx >= 500:
            self.rect.x = goal_rect.centerx - random.randint(300, goal_rect.centerx )+ 20
        else:
            self.rect.x = goal_rect.centerx + random.randint(300, WIDTH - goal_rect.centerx) - 70

        if goal_rect.centery >= 400:
            self.rect.y = goal_rect.centery - random.randint(300, goal_rect.centery) + 88
        else:
            self.rect.y = goal_rect.centery + random.randint(300, (HEIGHT - goal_rect.centery)) -70


class ScoreEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, score_value):
        super().__init__()
        font.set_bold(False)
        self.image = font.render(f"+{score_value}", True, BLACK)  # Tạo văn bản với màu đen, True là làm mịn...False là răng cưa
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alpha = 255  # Độ mờ (alpha) ban đầu là 255 (đầy đủ)

    def update(self):
        self.rect.y -= 2  # Di chuyển chữ lên trên màn hình
        self.alpha -= 5  # Giảm độ mờ dần dần
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ của chữ
        if self.alpha <= 0:
            self.kill()  # Xóa hiệu ứng khi chữ hoàn toàn mờ đi

class TimeEffect(pygame.sprite.Sprite):
    def __init__(self, temporary):
        super().__init__()
        if(temporary==1): 
            font.set_bold(False)
            self.image = font.render('+5', True, BLACK)  
        else:
            font.set_bold(False)
            self.image = font.render('*2', True, BLACK) 
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-70,100)
        self.alpha = 255  

    def update(self):
        self.rect.y -= 1  
        self.alpha -= 5  
        self.image.set_alpha(self.alpha)  
        if self.alpha <= 0:
            self.kill()  

# Hàm để vẽ đồng hồ đếm ngược
font_size = 66
font_scale_direction = 1
def draw_timing(remaining_time):
    global font_size,font_scale_direction
    if remaining_time <= 5:
        # Hiệu ứng phóng to thu nhỏ
        font_size += font_scale_direction
        if font_size >=85:  # Giới hạn kích thước lớn nhất
            font_scale_direction = -1
        elif font_size <= 66:  # Giới hạn kích thước nhỏ nhất
            font_scale_direction = 1
        clock_sound.set_volume(0.6)
        clock_sound.play()
    else: 
        font_size=66
        clock_sound.stop()

    # Cập nhật font với kích thước thay đổi
    dynamic_font = pygame.font.Font("JosefinSans-VariableFont_wght.ttf", font_size)
    dynamic_font.set_bold(True)
    text = dynamic_font.render(str(remaining_time), True, yellow_white)

    if remaining_time <= 5:
        # Chế độ gây cấn khi còn lại 5 giây
        if remaining_time % 2 == 0:
            text = dynamic_font.render(str(remaining_time), True, RED)  # Màu đỏ và nhấp nháy
        else:
            text = dynamic_font.render(str(remaining_time), True, yellow_white)  # Màu trắng khi không nhấp nháy
    screen.blit(text, (915 , 18))

# Hàm vẽ điểm số
def draw_score(score):
    dynamic_font = pygame.font.Font("JosefinSans-VariableFont_wght.ttf", 66)
    dynamic_font.set_bold(True)
    score_text = dynamic_font.render(str(score), True, yellow_white)
    screen.blit(score_text, (245,18))#vẽ một surface lên màn hình.

last_background = pygame.image.load('nền game over.png').convert()  
last_background = pygame.transform.scale(last_background, (WIDTH, HEIGHT))  # Thay đổi kích thước ảnh nền cho vừa màn hình
class End_game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = last_background
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.alpha = 0 

    def update(self):
        if(self.alpha<255):
            self.alpha += 35  
        self.image.set_alpha(self.alpha)  

game_over_image = pygame.image.load('game_over.png')  
game_over_image = pygame.transform.scale(game_over_image, (887, 198)) 
class Fail(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_over_image
        self.rect = self.image.get_rect()
        self.rect.x = 70
        self.rect.y = HEIGHT
        self.alpha = 0  # Độ mờ (alpha) ban đầu là 255 (đầy đủ)

    def update(self):
        if(self.rect.y > 56):
            self.rect.y = max(56, self.rect.y - 15)
        if(self.alpha<255):
            self.alpha = min(255, self.alpha + 15)  
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ của chữ

yourscore_image = pygame.image.load('your score (2).png') 
yourscore_image = pygame.transform.scale(yourscore_image, (647, 364)) 
class Scoreend(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = yourscore_image
        self.rect = self.image.get_rect()
        self.rect.x = 209
        self.rect.y = HEIGHT
        self.alpha = 0  

    def update(self):
        if(self.rect.y > 110):
            self.rect.y = max(110, self.rect.y - 15)  # Di chuyển chữ lên trên màn hình
        if(self.alpha<255):
            self.alpha = min(255, self.alpha + 15)  # tăng độ mờ dần dần
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ của chữ

class FinalScore(pygame.sprite.Sprite):
    def __init__(self, score):
        super().__init__()
        self.font = pygame.font.Font("PermanentMarker-Regular.ttf", 81)
        self.image = self.font.render(str(score), True, BLACK)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT+100))
        self.alpha = 0  # Bắt đầu với độ mờ 0

    def update(self):
        if self.rect.y > 301:
            self.rect.y = max(301, self.rect.y - 15)  # Di chuyển lên vị trí giữa
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 15)  # Tăng độ mờ
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ

replay_image = pygame.image.load('replay2.png')  
replay_image = pygame.transform.scale(replay_image, (90, 90)) 
class Replay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = replay_image
        self.rect = self.image.get_rect()
        self.rect.x = 454
        self.rect.y = HEIGHT+100
        self.alpha = 0  # Độ mờ (alpha) ban đầu là 255 (đầy đủ)

    def update(self):
        if(self.rect.y > 405):
            self.rect.y = max(405, self.rect.y - 15)
        if(self.alpha<255):
            self.alpha = min(255, self.alpha + 15)  # Giảm độ mờ dần dần
        self.image.set_alpha(self.alpha)  # Cập nhật độ mờ của chữ

def gamed(game_over, score):
    all_endgame = pygame.sprite.Group()
    fail = Fail()
    scoreend = Scoreend()
    replay = Replay()
    final_score = FinalScore(score)  # Điểm cuối cùng
    all_endgame.add(fail, scoreend, replay, final_score)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = False
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if replay.rect.collidepoint(mouse_x, mouse_y):  # Kiểm tra nếu người chơi nhấn vào nút replay
                    click_sound.play()
                    fail_sound.stop()
                    run_game()
                    return

        all_endgame.update()  # Gọi update() để tăng alpha
        screen.blit(last_background, (0, 0))  # Hiển thị nền trước
        clock = pygame.time.Clock()
        all_endgame.draw(screen)  # Vẽ tất cả sprite trong nhóm
        pygame.display.flip()
        clock.tick(60)  # Giới hạn tốc độ khung hình

# Hàm chính của trò chơi
def run_game():
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    # Khởi tạo các nhóm sprite
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    items = pygame.sprite.Group()
    doublescores = pygame.sprite.Group()
    doubletimes = pygame.sprite.Group()
    label_doublecores= pygame.sprite.Group()
    shields = pygame.sprite.Group()
    label_shields = pygame.sprite.Group()
    booms = pygame.sprite.Group()
    rescues = pygame.sprite.Group()
    score_effects = pygame.sprite.Group()  # Nhóm hiệu ứng điểm
    time_effects= pygame.sprite.Group()

    #Khởi tạo các sprites
    goal = Goal()
    goals.add(goal)
    item = Item(goal.rect)
    items.add(item)
    character = Character()
    all_sprites.add(goal,item,character)

    #khởi tạo biến
    score = 0
    game_over = False
    time_limit = 15# Giới hạn thời gian là 15 giây
    start_time = pygame.time.get_ticks()  # Thời gian bắt đầu trò chơi
    rescue_time = 0 # là một biến dùng để lưu trữ thời điểm cuối cùng vật phẩm cứu trợ được tạo ra.

    # Vòng lặp trò chơi
    while not game_over:
        # Kiểm tra thời gian còn lại
        time_left = time_limit - (pygame.time.get_ticks() - start_time) // 1000 #pygame.time.get_ticks() - start_time: Tính toán thời gian đã trôi qua (tính từ khi start_time được ghi lại).
        #pygame.time.get_ticks(): Trả về thời gian hiện tại (tính từ khi chương trình bắt đầu) tính bằng mili giây. Đây là giá trị mà Pygame sử dụng để theo dõi thời gian đã trôi qua từ khi chương trình bắt đầu chạy.
        #start_time: Lưu trữ thời gian bắt đầu trò chơi (hoặc một mốc thời gian quan trọng nào đó) bằng cách sử dụng pygame.time.get_ticks()
        #// 1000: Chia kết quả trên cho 1000 để chuyển đổi từ mili giây sang giây, vì pygame.time.get_ticks() trả về thời gian tính bằng mili giây (1 giây = 1000 mili giây)
        if time_left == 0:
            game_over = True  # Kết thúc trò chơi khi hết thời gian

        if pygame.time.get_ticks() - rescue_time > 25000 and len(rescues) < 1 + (score // 200):
            rescue_time = pygame.time.get_ticks()
            speed=random.randint(1,3) + 0.5*(score // 150)
            temporary= random.randint(1,4)
            if(temporary==1):
                doublescore=Doublescore(speed)
                all_sprites.add(doublescore)
                rescues.add(doublescore)
                doublescores.add(doublescore)
            elif(temporary==2):
                doubletime=Doubletime(speed)
                all_sprites.add(doubletime)
                rescues.add(doubletime)
                doubletimes.add(doubletime)
            elif(temporary==3):
                shield=Shield(speed)
                all_sprites.add(shield)
                rescues.add(shield)
                shields.add(shield)
            else:
                boom=Boom(speed)
                all_sprites.add(boom)
                rescues.add(boom)
                booms.add(boom)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Kiểm tra lấy hàng
        if pygame.sprite.spritecollide(character, items, True) and character.has_item == False:
            channel_pick_item.set_volume(0.8)
            channel_pick_item.play(pick_item)
            character.has_item= True
        
        # Kiểm tra giao hàng
        if character.deliver_item(goal):
            channel_goal.play(goal_sound)
            time_effect=TimeEffect(1)
            all_sprites.add(time_effect)
            time_effects.add(time_effect)
            time_limit +=5
            goal.reset_position()  # Đặt lại vị trí ô xanh sau khi giao hàng thành công
            if character.has_doublescore:
                score+=20
            else:
                score+=10

        # Tạo hiệu ứng điểm +10 hoặc +20
            if character.has_doublescore:
                score_effect = ScoreEffect(character.rect.centerx, character.rect.top - 50, 20)  # Hiệu ứng +20
            else:
                score_effect = ScoreEffect(character.rect.centerx, character.rect.top - 50, 10)  # Hiệu ứng +10
            all_sprites.add(score_effect)
            score_effects.add(score_effect)

        # Tạo hiệu ứng điểm +10 hoặc +20
            if character.has_doublescore:
                score_effect = ScoreEffect(character.rect.centerx, character.rect.top - 50, 20)  # Hiệu ứng +20
            else:
                score_effect = ScoreEffect(character.rect.centerx, character.rect.top - 50, 10)  # Hiệu ứng +10
            all_sprites.add(score_effect)
            score_effects.add(score_effect)

        # Thêm món hàng mới
            item = Item(goal.rect)
            all_sprites.add(item)
            items.add(item)

        # Trong vòng lặp trò chơi, khi người chơi lấy vật phẩm nhân đôi số điểm
        if pygame.sprite.spritecollide(character, doublescores, True):  # Kiểm tra va chạm với vật phẩm giáp
            character.pick_up_doublescore()  # Kích hoạt nhân đôi điểm
            label_doublescore = Label_doublescore()
            all_sprites.add(label_doublescore)
            label_doublecores.add(label_doublescore)
            channel_doublescore.set_volume(0.8)
            channel_doublescore.play(doublescore_sound)

        if(not character.has_doublescore):
            for label_doublescore in label_doublecores:
                label_doublescore.kill()

        # Trong vòng lặp trò chơi, khi người chơi lấy vật phẩm nhân đôi tg
        if pygame.sprite.spritecollide(character, doubletimes, True):  # Kiểm tra va chạm với vật phẩm giáp
            time_limit += time_left
            time_effect=TimeEffect(2)
            all_sprites.add(time_effect)
            time_effects.add(time_effect)
            channel_doubletime.set_volume(0.8)
            channel_doubletime.play(doubletime_sound)

        # Trong vòng lặp trò chơi, khi người chơi lấy vật phẩm giáp
        if pygame.sprite.spritecollide(character, shields, True):  # Kiểm tra va chạm với vật phẩm giáp
            character.pick_up_shield()  # Kích hoạt giáp
            channel_shield.set_volume(0.8)
            channel_shield.play(shield_sound)

        if(not character.has_shield):
            for label_shield in label_shields:
                label_shield.kill()

        # Trong vòng lặp trò chơi, khi người chơi lấy vật phẩm bom
        if pygame.sprite.spritecollide(character, booms, True):  # Kiểm tra va chạm với vật phẩm giáp
            for obstacle in obstacles:
                obstacle.kill()
            for _ in range(2):
                speed=random.randint(2,4)
                bien=random.randint(1,7)
                obstacle=Obstacle(speed,bien)
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            channel_bom.set_volume(0.8)
            channel_bom.play(bom_sound)

        if pygame.sprite.spritecollide(character, obstacles, True):#False: Nếu bạn truyền giá trị False, thì va chạm sẽ được kiểm tra nhưng không xóa các đối tượng trong nhóm obstacles sau khi va chạm xảy ra.
            if character.activity_shield():
                game_over = True # Đánh dấu trò chơi kết thúc nếu va chạm
                channel_break.set_volume(0.8)
                channel_break.play(break_sound)
            else:
                channel_break.play(break_shield)
        
        if score % 100 == 0 and len(obstacles) < 2 + (score // 100):
            speed=random.randint(2,4) + 0.2*(score // 100)
            bien=random.randint(1,7)
            obstacle = Obstacle(speed,bien)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
      
        # Kiểm tra trạng thái game over
        if game_over:
            clock_sound.stop()
            pygame.mixer.music.stop()
            fail_sound.play()
            channel_truck.stop()
            gamed(game_over , score)

        # Vẽ ảnh nền
        screen.blit(background, (0, 0))
        # Cập nhật các sprite
        all_sprites.update()
        # Vẽ màn hình
        all_sprites.draw(screen)
        draw_score(score)
        draw_timing(time_left) 
        # Vẽ hiệu ứng điểm
        score_effects.update()  # Cập nhật hiệu ứng
        score_effects.draw(screen)  # Vẽ các hiệu ứng điểm lên màn hình
        time_effects.update()  # Cập nhật hiệu ứng
        time_effects.draw(screen)  # Vẽ các hiệu ứng âm thanh lên màn hình

        # Cập nhật màn hình
        pygame.display.flip()
        # Điều khiển tốc độ trò chơi
        clock.tick(60)
    

    pygame.quit()

if __name__ == "__main__":
    wait_screen()
    run_game()