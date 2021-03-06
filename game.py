import time

from tkinter import X, Y, LEFT, RIGHT, BOTH, RAISED, END, Tk, Menu, filedialog, Text, Canvas
from tkinter.ttk import Frame, Button, Style, Entry
from pynput.keyboard import Key, Listener

BLANK_SPACE = "_"
DUNGEON_WIDTH = 20
DUNGEON_HEIGHT = 15
CELL_WIDTH = 40
CELL_HEIGHT = 40

class Dungeon:

    def __init__( self ):
        self.dungeon = []

        self.fill_dungeon()

    def fill_dungeon( self ):
        for row in range( DUNGEON_HEIGHT ):
            row_list = []
            for cell in range( DUNGEON_WIDTH ):
                row_list.append( BLANK_SPACE )
            self.dungeon.append( row_list )

    def get_grid( self ):
        return self.dungeon

class Game( Frame ):

    def __init__( self ):
        super().__init__()

        self.is_running = True

        self.dungeon = Dungeon()

        self.initialize()


    def _print_dungeon( self ):
        for row in self.dungeon:
            for cell in row:
                print( cell, end="" )
            print()

    def initialize( self ):
        self.style = Style()
        self.style.theme_use( "default" )

        self.master.title( "test" )
        self.pack( fill=BOTH, expand=True )

        self.center_window()

        self.place_UI()

        #self.after( 60, self.tick() )
        self.bind_all( "<Key>", self.on_press )

        self.player_x = 0;
        self.player_y = 0;

    def place_UI( self ):
        # Menu
        menu = Menu( self.master )
        self.master.config( menu=menu )

        file = Menu( menu, tearoff=0 )

        submenu = Menu( file, tearoff=0 )
        submenu.add_command( label="Other test" )
        submenu.add_command( label="Another test" )
        file.add_cascade( label="Test", menu=submenu, underline=0 )

        file.add_command( label="Save" )
        file.add_command( label="Load", command=self.open_file )
        file.add_command( label="Options" )

        file.add_separator()

        file.add_command( label="Exit", command=self.quit )
        menu.add_cascade( label="File", menu=file )

        # Game Frame
        game_frame = Frame( self, relief=RAISED, borderwidth=1 )
        game_frame.pack( fill=BOTH, expand=True )

        self.canvas = Canvas( game_frame, bg="white" )
        self.canvas.pack( fill=BOTH, expand=True )

        # UI
        quit_button = Button( self, text="Quit", command=self.quit )
        quit_button.pack( fill=X, side=RIGHT, padx=5, pady=5 )

        self.text = Text( self, width=2, height=1 )
        self.text.pack( fill=X, side=LEFT, expand=True, padx=5, pady=5 )

        grid = self.dungeon.get_grid()
        for row in range( len( grid ) ):
            for cell in range( len( grid[row] ) ):
                if( grid[row][cell] == BLANK_SPACE ):
                    self.canvas.create_line( cell * CELL_WIDTH, row * CELL_HEIGHT, cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT )
                    self.canvas.create_line( cell * CELL_WIDTH, row * CELL_HEIGHT, cell * CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT )
                    self.canvas.create_line( cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT, cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT )
                    self.canvas.create_line( cell * CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT, cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT )

        self.canvas.create_line( 10, 10, 30, 10, tag="square" )
        self.canvas.create_line( 10, 10, 10, 30, tag="square" )
        self.canvas.create_line( 30, 10, 30, 30, tag="square" )
        self.canvas.create_line( 10, 30, 30, 30, tag="square" )

    # Eventually will allow the player to load a save.
    def open_file( self ):
        file_types = [ ("Text files", "*.txt"), ("All files", "*") ]
        dialog = filedialog.Open( self, filetypes=file_types )
        filename = dialog.show()

        if( filename != "" ):
            with open( filename, "r" ) as file:
                self.text.insert( END, file.read() )

    # Centers the window and sets the resolution.
    def center_window( self ):
        width = 800
        height = 600

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_offset = (screen_width - width) // 2
        y_offset = (screen_height - height) // 2

        self.master.geometry( "%dx%d+%d+%d" % (width, height, x_offset, y_offset) )

    # Will
    def draw_dungeon( self ):
        grid = self.dungeon.get_grid()
        for row in range( len( grid ) ):
            for cell in range( len( grid[row] ) ):
                if( grid[row][cell] != BLANK_SPACE ):
                    self.canvas.create_line( cell * CELL_WIDTH, row * CELL_HEIGHT, cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT )
                    self.canvas.create_line( cell * CELL_WIDTH, row * CELL_HEIGHT, cell * CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT )
                    self.canvas.create_line( cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT, cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT )
                    self.canvas.create_line( cell * CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT, cell * CELL_WIDTH + CELL_WIDTH, row * CELL_HEIGHT + CELL_HEIGHT )

    def start( self ):
        print( "Beginning game..." )

    def stop( self ):
        print( "Done running..." )

    def tick( self ):
        pass

    def render( self ):
        self.update_idletasks()
        self.update()
        #self.draw_dungeon()

    def run( self ):
        while( self.is_running ):
            self.tick()
            self.render()

    def quit( self ):
        self.is_running = False

    def on_press( self, key_object ):
        key = key_object.keysym

        if( key == "Left" ):
            if( self.player_x == 0 ):
                return
            for line in self.canvas.find_withtag( "square" ):
                self.canvas.move( line, -CELL_WIDTH, 0 )
            self.player_x -= 1
            self.text.insert( END, "_" )
            self.text.delete( "0.0", END )
            self.text.insert( END, "Moved left." )
        elif( key == "Right" ):
            if( self.player_x == DUNGEON_WIDTH - 1 ):
                return
            for line in self.canvas.find_withtag( "square" ):
                self.canvas.move( line, CELL_WIDTH, 0 )
            self.player_x += 1
            self.text.insert( END, "_" )
            self.text.delete( "0.0", END )
            self.text.insert( END, "Moved right." )
        elif( key == "Up" ):
            if( self.player_y == 0 ):
                return
            for line in self.canvas.find_withtag( "square" ):
                self.canvas.move( line, 0, -CELL_HEIGHT )
            self.player_y -= 1
            self.text.insert( END, "_" )
            self.text.delete( "0.0", END )
            self.text.insert( END, "Moved up." )
        elif( key == "Down" ):
            if( self.player_y == DUNGEON_HEIGHT - 1 ):
                return
            for line in self.canvas.find_withtag( "square" ):
                self.canvas.move( line, 0, CELL_HEIGHT )
            self.player_y += 1
            self.text.insert( END, "_" )
            self.text.delete( "0.0", END )
            self.text.insert( END, "Moved down." )



def main():
    root = Tk()
    root.resizable( width=False, height=False )
    game = Game()
    game.start()
    game.run()
    game.stop()


if( __name__ == "__main__" ):
    main()
