import pygame
from settings import * 
from tile import Tile
from player import Player
from debug import debug 
from support import *
from random import choice 
from weapons import Weapon

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None


    # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
                'boundary': import_csv_layout('/home/arthurbrinkmann/dev/personalprojects/ZeldaLikeGame/graphics/map_FloorBlocks.csv'),
                'grass' : import_csv_layout('/home/arthurbrinkmann/dev/personalprojects/ZeldaLikeGame/graphics/map_Grass.csv'),
                'object': import_csv_layout ('/home/arthurbrinkmann/dev/personalprojects/ZeldaLikeGame/graphics/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('/home/arthurbrinkmann/dev/personalprojects/ZeldaLikeGame/graphics/Grass'),
            'objects': import_folder('/home/arthurbrinkmann/dev/personalprojects/ZeldaLikeGame/graphics/objects')
        }


        for style, layout in layouts.items():
            for row_index, row in enumerate (layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacles_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],'grass',random_grass_image)
                        
                        if style == 'object':
                            surf = graphics['objects'][int(col)] # previoussurf = graphics['objects'][int(0-19 OR 0)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites], 'object',surf)



        self.player = Player((2000,1430),[self.visible_sprites],self.obstacles_sprites,self.create_attack,self.destroy_weapon)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None    

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor 
        self.floor_surf = pygame.image.load('/home/arthurbrinkmann/dev/personalprojects/ZeldaLikeGame/graphics/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor 
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)