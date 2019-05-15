import numpy as np
from PIL import Image



lvl = np.load('visualizevae_v4.npy')
lvl =  lvl.reshape([-1,24,32,5])

# E, C, B, R, L

brick = Image.open('brick.png')
gold = Image.open('gold.png')
guard = Image.open('guard.png')
ladder = Image.open('ladder.png')
rope = Image.open('rope.png')
ground = Image.open('ground.png')
bkg = Image.open('bkg.png')

brick = np.asarray(brick)
gold = np.asarray(gold)
guard = np.asarray(guard)
ladder = np.asarray(ladder)
rope = np.asarray(rope)
ground = np.asarray(ground)
bkg = np.asarray(bkg)
print(guard.shape)

for k in range(lvl.shape[0]):
    print("Generating Level : ", k)
    level_comp = np.zeros(((22*44) + 20, 32*40,4))
    for i in range(22):
        for j in range(32):
            if lvl[k,i,j,4]:
                level_comp[(i*44):(i*44)+44, (j*40):(j*40)+40] = guard
            elif lvl[k,i,j,3]:
                level_comp[(i*44):(i*44)+44, (j*40):(j*40)+40] = gold
            elif lvl[k,i,j,0]:
                level_comp[(i*44):(i*44)+44, (j*40):(j*40)+40] = brick
            elif lvl[k,i,j,1]:
                level_comp[(i*44):(i*44)+44, (j*40):(j*40)+40] = rope
            elif lvl[k,i,j,2]:
                level_comp[(i*44):(i*44)+44, (j*40):(j*40)+40] = ladder
            else:
                level_comp[(i*44):(i*44)+44, (j*40):(j*40)+40] = bkg
    for j in range(32):
        level_comp[(22*44):(22*44)+20, (j*40):(j*40)+40] = ground

    f = Image.fromarray(np.uint8(level_comp))
    f.save('./ae' + str(k) + '.png')
