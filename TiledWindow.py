import arcade
import pathlib


class TiledWindow (arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Initial Tiled Map Super Simple Example")
        self.map_location = pathlib.Path.cwd()/'Assets'/'DemoClassMap.json'
        self.current_scene = None
        self.mapscene1 = None
        self.mapscene2 = None
        self.wall_list=None
        self.wall_list2 = None
        self.player: arcade.Sprite = None
        self.simple_physics = None
        self.player_list = None
        self.move_speed = 3
        self.prev_scene: arcade.Scene = None

    def setup(self):
        sample_map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene1 = arcade.Scene.from_tilemap(sample_map)
        self.wall_list = sample_map.sprite_lists["WallLayer"]
        map2 = arcade.tilemap.load_tilemap(pathlib.Path.cwd()/'Assets'/'Map2.json')
        self.mapscene2 = arcade.Scene.from_tilemap(map2)
        self.wall_list2 = map2.sprite_lists['wallLayer']
        self.player = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'orc2.png')
        self.player.center_x = 96
        self.player.center_y = 224
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.current_scene = self.mapscene1

    def on_draw(self):
        arcade.start_render()

        self.current_scene.draw()

        self.player_list.draw()

    def on_update(self, delta_time: float):
        self.simple_physics.update()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y += self.move_speed
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y -= self.move_speed
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x -= self.move_speed
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x += self.move_speed
        if self.player.center_x < -10: # if the player is on map1 and heading off the map
            self.current_scene = self.mapscene2
            self.player.center_x = self.width-self.player.width/2
            self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list2)
        elif self.player.center_x > self.width+10: # if we are on map2 and headed off the scene
            self.current_scene = self.mapscene1
            self.player.center_x = self.player.width/2
            self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y <0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y =0
        if self.player.change_y >0 and (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y =0
        if self.player.change_x <0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x =0
        if self.player.change_x >0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x =0