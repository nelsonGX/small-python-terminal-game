import pygame
import random
import os

from client.minigame.games.game01 import pause
from server import Server

class Game05:
    def __init__(self, session: Server):
        self.session = session

    async def start(self):
        FPS = 60  # 1秒中更新60次畫面
        WIDTH = 500  # 設定好之後不會隨便改的變數用大寫命名
        HEIGHT = 600

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)
        BACKGROUNDGREY = (238, 238, 238)
        BACKGROUNDWHITE = (246, 246, 246)

        # 遊戲初始化
        pygame.init()
        pygame.mixer.init()  # 音效模組初始化，這樣才可以引入這些音效

        # 創建視窗
        screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 螢幕寬度,螢幕高度
        pygame.display.set_caption('巨石生存戰')  # 左上方的標題
        clock = pygame.time.Clock()  # 管理時間

        # 載入圖片  載入之前要先把pygame做初始化
        background_img = pygame.image.load(os.path.join("img", "background.png")).convert()  # 轉換成pygame比較容易讀取的格式
        player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
        # rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
        bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
        rock_imgs = []
        for i in range(5):
            rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

        power_imgs = {}
        power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
        power_imgs['lightning'] = pygame.image.load(os.path.join("img", "lightning.png")).convert()

        # 載入音樂
        shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.mp3"))
        shoot_sound.set_volume(0.3)  # 音效改小
        expl0_sound = pygame.mixer.Sound(os.path.join("sound", "explosion0.mp3"))
        expl0_sound.set_volume(0.2)
        expl1_sound = pygame.mixer.Sound(os.path.join("sound", "explosion1.mp3"))
        expl1_sound.set_volume(0.3)
        expl_sounds = [expl0_sound, expl1_sound]
        '''expl_sounds = [
            pygame.mixer.Sound(os.path.join("sound", "explosion0.mp3")),
            pygame.mixer.Sound(os.path.join("sound", "explosion1.mp3"))
        ]'''
        pygame.mixer.music.load(os.path.join("sound", "background.mp3"))
        pygame.mixer.music.set_volume(0.3)  # 背景聲音改小

        font_name = os.path.join("SentyOrchid.ttf")  # 要引入的字體

        '''all_sprites = pygame.sprite.Group() #sprites的群組,裡面可以放sprite的物件
        rocks = pygame.sprite.Group() #石頭群組
        bullets = pygame.sprite.Group() #子彈群組
        powers = pygame.sprite.Group() #寶物群組
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0  直接放到下面，因為重新開始遊戲的話，這些都要重新設定'''
        pygame.mixer.music.play(-1)  # 括號裡面寫重複播放幾次，-1就是無限多次

        def draw_text(surf, text, size, x, y):  # 把文字寫到畫面上的動作；第一格是要寫在什麼平面上，第二格是要寫的文字，第三格是文字大小，第四、五格是要寫在哪裡(座標)
            font = pygame.font.Font(font_name, size)  # (字體,文字大小)
            text_surface = font.render(text, True, WHITE)  # 渲染出來；第一格是要寫出來的文字，第二格如果是True，就會讓字體看起來比較滑順，第三格是文字顏色
            text_rect = text_surface.get_rect()  # 文字定位
            text_rect.centerx = x
            text_rect.top = y
            surf.blit(text_surface, text_rect)  # 畫在平面上(要畫的文字,畫在哪)

        def draw_text_BLACK_score(surf, text, size, x,
                                  y):  # 把文字寫到畫面上的動作；第一格是要寫在什麼平面上，第二格是要寫的文字，第三格是文字大小，第四、五格是要寫在哪裡(座標)
            font = pygame.font.Font(font_name, size)  # (字體,文字大小)
            text_surface = font.render(text, True, BLACK)  # 渲染出來；第一格是要寫出來的文字，第二格如果是True，就會讓字體看起來比較滑順，第三格是文字顏色
            text_rect = text_surface.get_rect()  # 文字定位
            text_rect.centerx = x
            text_rect.top = y
            surf.blit(text_surface, text_rect)  # 畫在平面上(要畫的文字,畫在哪)

        def new_rock():
            rock = Rock()
            all_sprites.add(rock)  # 加回去才能被update
            rocks.add(rock)  # 加進去才可以繼續判斷是否跟子彈碰撞到

        def draw_health(surf, hp, x, y):  # 劃出生命值(畫在什麼平面,剩多少血量,x,y)
            if hp < 0:
                hp = 0
            BAR_LENGTH = 100
            BAR_HEIGHT = 10
            fill = (hp / 100) * BAR_LENGTH  # 生命條要填滿多少(剩幾%血量)
            outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # 生命條外框
            fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)  # 填滿生命條外框
            pygame.draw.rect(surf, GREEN, fill_rect)
            pygame.draw.rect(surf, BLACK, outline_rect, 2)  # 如果沒有第四格，白色就會直接填滿整個生命條，而不是只有外框

        def draw_init():
            screen.blit(background_img, (0, 0))  # 初始畫面也要背景
            draw_text(screen, '巨石生存戰', 64, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, '按A或D鍵左右移動炮台 空白鍵發射砲彈', 27, WIDTH / 2, HEIGHT / 2)
            draw_text(screen, '按任意鍵開始遊戲', 40, WIDTH / 2, HEIGHT * 3 / 4.5)
            pygame.display.update()  # 這樣才會畫出來
            # 取得現在發生的事件，如果有按下任意按鍵的事件，就讓遊戲開始
            waiting = True  # 等待鍵盤被按下去的事件
            while waiting:  # 如果還在等待
                clock.tick(FPS)  # 1秒中之內最多更新幾次畫面
                # 取得輸入
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True
                    elif event.type == pygame.KEYUP:  # 如果事件類型為按按鍵
                        waiting = False  # 遊戲開始
                        return False

        class Player(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(player_img, (100, 100))  # 第一格是要傳入的圖片，第二格是要改成什麼大小
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()  # rect拿來定位這張圖片,簡單來說就是把一張圖片框起來,框起來就可以設定屬性(top、bottom、left、right、(x,y)等等)
                self.radius = 25  # 因為用圓形來加強碰撞判斷，所以需要再給它一個屬性，為圓形半徑
                # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)#把要判斷的圓形畫在圖片上，且圓心在中心點
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
                self.speedx = 8
                self.health = 100
                self.lightning = 1  # 子彈等級
                self.lightning_time = 0  # 吃到閃電的時間

            def update(self):
                now = pygame.time.get_ticks()
                if self.lightning > 1 and now - self.lightning_time > 5000:  # 5000毫秒
                    self.lightning -= 1
                    self.lightning_time = now

                key_pressed = pygame.key.get_pressed()  # 鍵盤上的每個按鍵有沒有被按，如果有，就是True，沒有就是False
                if key_pressed[pygame.K_d]:  # 判斷右鍵有沒有被按
                    self.rect.x += self.speedx

                if key_pressed[pygame.K_a]:  # 判斷左鍵有沒有被按
                    self.rect.x -= self.speedx

                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH

                if self.rect.left < 0:
                    self.rect.left = 0

            def shoot(self):
                if self.lightning == 1:  # 如果子彈等級是1
                    bullet = Bullet(self.rect.centerx, self.rect.top)  # 傳入飛船座標
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()  # 播放
                elif self.lightning >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery)  # 傳入飛船座標
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()  # 播放

            def lightningup(self):
                self.lightning += 1  # 等級加1
                self.lightning_time = pygame.time.get_ticks()  # 把吃到閃電的時間設為現在的時間

        class Rock(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image_ori = random.choice(rock_imgs)  # 存放沒有轉動過的圖片(沒失真)
                self.image_ori.set_colorkey(BLACK)
                self.image = self.image_ori.copy()  # 存放轉動過的圖片(失真)
                self.rect = self.image.get_rect()  # rect拿來定位這張圖片,簡單來說就是把一張圖片框起來,框起來就可以設定屬性(top、bottom、left、right、(x,y)等等)
                self.radius = int(self.rect.width * 0.9 / 2)  # 轉成整數，分數才不會有小數點
                # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-180, -100)
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-3, 3)
                self.total_degree = 0
                self.rot_degree = random.randrange(-3, 3)  # 轉動幾度

            def rotate(self):
                self.total_degree += self.rot_degree
                self.total_degree = self.total_degree % 360  # 轉超過360沒有意義
                self.image = pygame.transform.rotate(self.image_ori,
                                                     self.total_degree)  # 第一格是要轉動的圖片(讓沒有失真過的圖片轉動)；第二格是要轉動幾度
                center = self.rect.center  # 原先定位的中心點
                self.rect = self.image.get_rect()  # 轉動後的圖片重新定位
                self.rect.center = center  # 把中心點設為原先的中心點

            def update(self):
                self.rotate()
                self.rect.y += self.speedy
                self.rect.x += self.speedx

                if (self.rect.top > HEIGHT) or (self.rect.left > WIDTH) or (self.rect.right < 0):  # 如果石頭已經超出畫面，就讓它重置x跟y
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-100, -40)
                    self.speedy = random.randrange(2, 10)
                    self.speedx = random.randrange(-3, 3)

        class Bullet(pygame.sprite.Sprite):
            def __init__(self, x, y):  # 因為子彈會在飛船上方，所以也要傳入飛船的位置
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(bullet_img, (20, 20))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()  # rect拿來定位這張圖片,簡單來說就是把一張圖片框起來,框起來就可以設定屬性(top、bottom、left、right、(x,y)等等)
                self.rect.centerx = x
                self.rect.bottom = y
                self.speedy = -10  # 子彈往上射

            def update(self):
                self.rect.y += self.speedy
                if self.rect.bottom < 0:  # 如果子彈已經出了畫面，就可以刪掉
                    self.kill()

        class Power(pygame.sprite.Sprite):
            def __init__(self, center):
                pygame.sprite.Sprite.__init__(self)
                self.type = random.choice(['shield', 'lightning'])  # 現在是哪種寶物
                self.image = pygame.transform.scale(power_imgs[self.type], (30, 40))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()  # rect拿來定位這張圖片,簡單來說就是把一張圖片框起來,框起來就可以設定屬性(top、bottom、left、right、(x,y)等等)
                self.rect.center = center
                self.speedy = 3

            def update(self):
                self.rect.y += self.speedy
                if self.rect.top > HEIGHT:  # 如果寶物大於視窗高度，就可以刪掉
                    self.kill()

        # 遊戲迴圈:取得玩家輸入  更新遊戲  畫面顯示
        show_init = True  # 判斷初始化面要不要顯示
        running = True
        while running:  # 判斷遊戲是否要繼續
            if show_init:  # 遊戲一開始就判斷是否要出現遊戲初始畫面
                close = draw_init()
                if close:
                    break
                show_init = False
                all_sprites = pygame.sprite.Group()  # sprites的群組,裡面可以放sprite的物件
                rocks = pygame.sprite.Group()  # 石頭群組
                bullets = pygame.sprite.Group()  # 子彈群組
                powers = pygame.sprite.Group()  # 寶物群組
                player = Player()
                all_sprites.add(player)
                for i in range(8):
                    new_rock()
                score = 0

            clock.tick(FPS)  # 1秒中之內最多更新幾次畫面

            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  # 如果事件類型為按按鍵
                    if event.key == pygame.K_SPACE:  # 如果按的是空白建
                        player.shoot()  # 呼叫射擊函式

            # 更新遊戲
            all_sprites.update()  # 可以執行sprites群組裡面每個物件的update函式
            hits = pygame.sprite.groupcollide(rocks, bullets, True, True)  # 第3格是判斷石頭碰到子彈，石頭要不要刪掉；第4格是判斷子彈碰到石頭，子彈要不要刪掉
            for hit in hits:  # 因為石頭會被子彈打光，因此每打到一個石頭，就會再生成一個新的
                random.choice(expl_sounds).play()
                score += hit.radius  # 每個hit就是碰撞倒的石頭；radius就是石頭的半徑
                if random.random() > 0.98:  # 掉寶率
                    pow = Power(hit.rect.center)
                    all_sprites.add(pow)
                    powers.add(pow)
                new_rock()

            hits = pygame.sprite.spritecollide(player, rocks, True,
                                               pygame.sprite.collide_circle)  # 飛船跟石頭撞到時,要不要把石頭刪掉(原本是不用刪，因為遊戲結束，但後來增加了飛船血條，也就是說被砸到不一定遊戲結束，所以石頭要刪);第四格為用圓形框出飛船和石頭，使碰撞判斷更精準
            # hits = pygame.sprite.spritecollide(player, rocks, False) 此函式會回傳一個列表，列表是所有碰撞到飛船的石頭
            for hit in hits:  # 如果列表有值，就關閉遊戲，代表飛船被砸到，遊戲結束
                new_rock()
                player.health -= hit.radius  # hit是撞到的石頭
                if player.health <= 0:
                    show_init = True  # 當生命值為0，就再把初始畫面顯示出來
                    running = False

            # 判斷寶物跟飛船相撞
            hits = pygame.sprite.spritecollide(player, powers, True)
            for hit in hits:
                if hit.type == 'shield':
                    player.health += 20
                    if player.health > 100:
                        player.health = 100

                elif hit.type == 'lightning':
                    player.lightningup()

            # 畫面顯示
            screen.fill(BLACK)  # R紅色,G綠色,B藍色
            screen.blit(background_img, (0, 0))  # 要把什麼畫上去，要畫在什麼位置
            all_sprites.draw(screen)  # 把all_sprites這個群組裡面的東西全部都畫在screen上
            draw_text_BLACK_score(screen, str(score), 30, WIDTH / 2, 10)  # (寫在什麼平面,要寫的文字(分數),文字大小,x,y)
            draw_health(screen, player.health, 5, 15)
            pygame.display.update()  # 畫面更新(有這行畫面才會變顏色)

        pygame.quit()
        await pause()