import os
import random 
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect)-> tuple[bool,bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横方向,縦方向）
    画面内ならTrue 画面外ならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False #横方向のはみだしチェック
    if obj_rct.top <0 or HEIGHT < obj_rct.bottom:
        tate = False
    return  yoko, tate        


def gameover(screen: pg.Surface) -> None:
    """
    gameover の Docstring
    引数：スクリーン
    戻り値：なし
    ゲームオーバー時に黒い画面が表示され、白い文字でGameOverが表示される。
    文字の左右にはこうかとんの画像が表示される。5秒後に閉じられる。
    """
    black_img = pg.Surface((WIDTH,HEIGHT))
    black_img.set_alpha(255)
    screen.blit(black_img,(0,0))
    gameover_font = pg.font.Font(None,50)
    txt = gameover_font.render("GameOver",True,(255,255,255))
    screen.blit(txt,[450,300]) 
    gameover_img = pg.image.load("fig/8.png")
    screen.blit(gameover_img,[400,275])
    screen.blit(gameover_img,[650,275])
    

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    init_bb_imgs の Docstring
    :引数なし
    :return: bb_imgsに爆弾のSurface
    :rtype: tuple[list[Surface], list[int]]
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs        


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs,bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]  # 空のSurface
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標     
    bb_img.set_colorkey((0, 0, 0))  # 黒色を透過色に設定
    
    
    vx, vy = +5, +5  # 爆弾の横速度，縦速度
    clock = pg.time.Clock()
    tmr = 0
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
    
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            pg.display.update()
            time.sleep(5)
            return


        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        idx = min(tmr//500,9) #500カウントごとに加速度上昇。上限9
        center = bb_rct.center #座標固定
        bb_img = bb_imgs[idx] #何番目の加速か
        bb_rct = bb_img.get_rect() #rect
        bb_rct.center = center #座標を戻す
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        

        if tmr%500 == 0: #500秒ごとに実行。ifなしだと毎カウントごとに加速してしまう
            vx *= bb_accs[idx] #加速適用
            vy *= bb_accs[idx]
        
        yoko,tate = check_bound(bb_rct)
        
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()