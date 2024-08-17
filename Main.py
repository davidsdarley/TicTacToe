import random
import pygame


easy = pygame.image.load("tictac easy.png")
hard = pygame.image.load("tictac hard.png")
ex = pygame.image.load("tictac X.png")
o = pygame.image.load("tictac O.png")
you = pygame.image.load("tictac you.png")
me = pygame.image.load("tictac me.png")

class Grid:
    def __init__(self, game, deltax = 200, deltay = 200, color = 'white', map = "tictactoe"):
        self.deltax = deltax
        self.deltay =deltay

        #probably unecessary
    #    self.xmin = 0 #absolute farthest you can go to the left
    #    self.ymin = 0 #absolute farthest you can go up
        self.cells= [] #to be a list of the cells in the grid
        self.xrange = None
        self.yrange = None
    #Im acatually going to use this one
        self.color = color
        self.map = map
        self.open = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

        self.game = game
        """
        PLANNING
        in order to make this one work, all I need to do is create a 3x3 grid. That can be hardcoded in to do that
        1) make row 1, create 3 cells and save them in the Grid index
        2) repeat two more times
        Done. Simple
        """
        if map == 'tictactoe':
            row = 0
            y = 70+ self.deltay/2
            while row < 3:
                self. cells.append([])
                column = 0
                x = 350 + self.deltax/2
                while column < 3:
                    self.cells[row].append(Cell((x,y),(row, column), self, dim = (deltax, deltay)))
                    column +=1      #increment the column and x value
                    x+= self.deltax
                row += 1
                y+= deltay #increment the row and the y value
    def __del__(self):
        for cell in self.cells:
            del cell

    def update(self): #this might prove to be unnecessary in this game
        for row in self.cells:
            for cell in row:
                cell.update()

    def blit(self):
        for row in self.cells:
            for cell in row:
                cell.blit()
    def click(self, point):
        for row in self.cells:
            for cell in row:
                if cell.clicked(point):

                    return True
        return False
class Cell:
    def __init__(self, point, index, grid, dim=(50, 50), ter = None):
        self.point = point
        self.x = point[0]
        self.y = point[1]

        self.center = point #these two values are unchanging references, unaltered by camera movements
        self.dim = dim

        self.width = float(dim[0])
        self.height = float(dim[1])
        self.ter = ter
        self.index = index
        self.grid = grid


        self.game = grid.game
    def __del__(self):
        del self
    def update(self): #there might legit not be anything I need to update in this project. Wild.
        pass
    def blit(self):
        '''In this version, there are only a few things that need to happent to blit it
        1) draw the tic tac toe board lines
        2) if filled, show the appropritate x or o
        3) if not filled, continue to exist

        one last thing this needs to do:
        in pregame stuff, it needs to show words. put on different costumes will be necessary
        '''
        if self.ter in ['start', 'You', 'stop', 'new']:
            return
        elif self.ter == 'diff-e':
            self.game.centerSurf(easy, self.point)
            return
        elif self.ter == 'diff-h':
            self.game.centerSurf(hard, self.point)
            return
        elif self.ter == 'you':
            self.game.centerSurf(you, self.point)
            return
        elif self.ter =='me':
            self.game.centerSurf(me, self.point)
            return



        color = (228,207,164)
        X = (27, 92, 255)
        O = (234, 27, 27)
        if self.ter == 'X':
            color = X
        if self.ter =='O':
            color = O

        pygame.draw.rect(self.game.screen,color, pygame.Rect(self.x-self.width/2, self.y-self.height/2,self.width, self.height))
                #commad to draw     draw on ^      color r g b                upper left corner    upper right corner     how wide    how tall
        if self.ter == 'X':
            self.game.centerSurf( ex ,self.point)
        elif self.ter == 'O':
            self.game.centerSurf( o ,self.point)
        #draw a box
        rgb = (150,150,150)
            #left side
        pygame.draw.line(self.game.screen,rgb,(self.x - self.width / 2, self.y - self.height / 2),(self.x - self.width / 2, self.y + self.height / 2))
            #right side
        pygame.draw.line(self.game.screen,rgb,(self.x + self.width / 2, self.y - self.height / 2),(self.x + self.width / 2, self.y + self.height / 2))
            #Top
        pygame.draw.line(self.game.screen,rgb,(self.x - self.width / 2, self.y - self.height / 2),(self.x + self.width / 2, self.y - self.height / 2))
            #Bottom
        pygame.draw.line(self.game.screen,rgb,(self.x - self.width / 2, self.y + self.height / 2),(self.x + self.width / 2, self.y + self.height / 2))


    def clicked(self,point):
        '''base case: the x and y values both are within the cell. Return True
        else: return false'''
        x = point[0]
        y = point[1]
        #check whether or not it has been clicked
        if not self.game.turn and self.game.state:
            return False
        if x> self.x-self.width/2 and x<= self.x+self.width/2:
            if y> self.y-self.height/2 and y<= self.y+self.height/2:
                #the response
                '''this little bit is for the pregame thing, for changing the settings'''
                if self.ter == 'start':
                    self.game.start()
                    return False
                elif self.ter ==  'stop':
                    self.game.running = False
                    return False
                elif self.ter == 'diff-e':
                    self.game.easy = False
                    self.ter = 'diff-h'
                    return False
                elif self.ter == 'diff-h':
                    self.game.easy = True
                    self.ter = 'diff-e'
                    return False
                elif self.ter == 'you':
                    self.game.turn = False
                    self.ter = 'me'
                    return False
                elif self.ter == 'me':
                    self.game.turn = True
                    self.ter = 'you'
                    return False
                elif self.ter == None:
                    self.ter = 'X'
                    self.grid.open.remove(self.index)
                    self.game.turn = False
                elif self.ter == 'new':
                    self.game.welcome()

                elif self.ter == 'O':
                    return False




                return True
        return False

#this class exists to help me communicate between files. I don't technically need it but it's easier to stay organized when I have multiple files



"""possible screens"""
welcome = pygame.image.load("TicTacToe_startscreen copy.png")
white = pygame.image.load("TicTacToe_whitescreen.png")
win = pygame.image.load("TicTacToe_win.png")
lose =pygame.image.load("TicTacToe_lose.png")
tie = pygame.image.load("TicTacToe_tie.png")
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1296, 750))
        self.background = welcome
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = None
        self.state = False
        self.easy = True
        self.turn = True
        self.count = 0

    def update(self):
        if self.grid != None:
            self.grid.update()
    def blit(self):
        screen.blit(self.background, (0, 0))
        self.grid.blit()
        pygame.display.update()

    def wait(self,t = 1):
        self.blit()
        pygame.time.wait(round(t*1000))
    def click(self, point):
        click = self.grid.click(point)
        if self.state:

            if self.gameover():
                return
        if not self.turn and self.state:
            self.ai()

    def welcome(self):
        pass
        if self.grid != None:
            del self.grid
        self.grid = Grid(self, map = None)
        self.background = welcome
        start = Cell((1296/2, 632),None, self.grid, (300,70), ter = 'start')
        difficulty = Cell((1296/2,360),None, self.grid, (280,60), ter = "diff-e")
        first = Cell((1296/2,550), None, self.grid, (200,60), ter = 'you')

        self.grid.cells.append([])
        self.grid.cells[0].append(start)
        self.grid.cells[0].append(difficulty)
        self.grid.cells[0].append(first)

    def rp(self, point):
        return round(point[0]), round(point[1])

    def centerSurf(self, surf, point):
        self.screen.blit(surf, self.rp((point[0] - surf.get_width() / 2, point[1] - surf.get_height() / 2)))
    def start(self):
        del self.grid
        self.grid = Grid(self)
        self.background = white
        self.state = True
    def newgame(self):
        del self.grid
        self.grid = Grid(self, map = None)
        start = Cell((535, 555),None, self.grid, (70,50), 'new')
        stop = Cell((750, 555),None, self.grid, (70,50),'stop')
        self.grid.cells.append([])
        self.grid.cells[0].append(start)
        self.grid.cells[0].append(stop)

    def win(self):
        self.wait(2)
        self.state = False
        self.turn = True
        self.count = 0
        self.background = win
        self.newgame()


        #show YouWin! screen and offer to play again
    def lose(self):
        self.wait(2)
        #show YouLose! screen and offer to play again
        self.state = False
        self.turn = True
        self.count = 0
        self.background = lose
        self.newgame()
    def tie(self):
        self.wait(2)
        self.state = False
        self.turn = True
        self.count = 0
        self.background = tie
        self.newgame()

    def gameover(self):
        '''to check if either side won, we will iter through the grid checking the three spaces
        1) choose a row to row.check
            a) if the cell.ter == team continue. Else return False
            b) if all three are, return True.
        2) if True, Yay! you won. Else pass in next row
        3) if all rows are false, move on to columns.
        4) if all columns are false, move on to the two diagonals
        5) if all diagonals are false, return False

        '''

    #check if you won
        c = 'X'
        if self.checkrows(c):
            self.win()
            return True
        if self.checkcols(c):
            self.win()
            return True
        if self.checkdi(c):
            self.win()
            return True
        c= 'O'
        if self.checkrows(c):
            self.lose()
            return True
        if self.checkcols(c):
            self.lose()
            return True
        if self.checkdi(c):
            self.lose()
            return True
        #check if there are no spaces left
        if len(self.grid.open) == 0:
            self.tie()
            return True
    def checkrows(self, team, quota = 3):
        if self.check(self.grid.cells[0], team, quota):
            return True
        if self.check(self.grid.cells[1], team, quota):
            return True
        if self.check(self.grid.cells[2], team, quota):
            return True
        return False
    def checkcols(self, team, quota = 3):
        c = 0
        while c < 3:
            if self.check([self.grid.cells[0][c],self.grid.cells[1][c],self.grid.cells[2][c]],team, quota):
                return True
            c+=1
        return False
    def checkdi(self,team, quota = 3):
        if self.check([self.grid.cells[0][0], self.grid.cells[1][1], self.grid.cells[2][2]], team, quota):
            return True
        if self.check([self.grid.cells[0][2], self.grid.cells[1][1], self.grid.cells[2][0]], team, quota):
            return True
        return False
    def check(self,lst, team, quota = 3):
        count = 0
        for cell in lst:
            if cell.ter == team:
                count += 1
            elif cell.ter != None:
                return False
        if count == quota:
            return True

        return False
    def easyai(self):
        '''this ai simply chooses a random available space to go
                    from the availale spaces
                        space.ter = O
                        remove space from self.grid.open'''
        max = len(self.grid.open) - 1
        i = random.randint(0, max)
        cell = self.grid.open[i]
        row = cell[0]
        col = cell[1]

        self.grid.cells[row][col].ter = 'O'
        self.grid.open.remove(cell)
        self.turn = True
        self.gameover()
    def hardai(self, team):
        # rows

        for row in self.grid.cells:
            if self.check(row, team, 2):
                for cell in row:
                    if cell.ter == None:
                        self.grid.open.remove(cell.index)
                        cell.ter = 'O'
                        self.turn = True
                        self.gameover()
                        return True
        # columns

        c = 0
        while c < 3:
            if self.check([self.grid.cells[0][c], self.grid.cells[1][c], self.grid.cells[2][c]], team, 2):
                i = 0
                while i < 3:
                    cell = self.grid.cells[i][c]
                    if cell.ter == None:
                        self.grid.open.remove(cell.index)
                        cell.ter = 'O'
                        self.turn = True
                        self.gameover()
                        return True
                    i += 1
            c+=1
        # diagonals

        if self.check([self.grid.cells[0][0], self.grid.cells[1][1], self.grid.cells[2][2]], team, 2):
            c = 0
            while c < 3:
                cell = self.grid.cells[c][c]
                if cell.ter == None:
                    self.grid.open.remove(cell.index)
                    cell.ter = 'O'
                    self.turn = True
                    self.gameover()
                    return True
                c += 1
        if self.check([self.grid.cells[0][2], self.grid.cells[1][1], self.grid.cells[2][0]], team, 2):
            c = 0
            while c < 3:
                cell = self.grid.cells[c][2 - c]
                if cell.ter == None:
                    self.grid.open.remove(cell.index)
                    cell.ter = 'O'
                    self.turn = True
                    self.gameover()
                    return True
                c += 1
        return False

    def ai(self):
        self.wait(.5)
        #easy ai
        if self.easy:
            self.easyai()
        #hard ai
        else:
            """Hard ai first looks to win. Then looks to block, then defaults to easy
            1)check all rows for your win
                a)look at a row. if it has 2 in it, and third is available, take it"""
            #win

            if self.hardai('O'):
                return
            #don't lose
            elif self.hardai('X'):

                return
            #random
            else:
                self.easyai()

game = Game()
game.welcome()
screen = game.screen





if __name__ == '__main__':
    while game.running == True:
        screen.fill((0, 0, 0))
        mouseUp = (None, None)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the game when X is clicked
                game.running = False
            if event.type == pygame.MOUSEBUTTONUP:  # click, return mouse position
                mouseUp = pygame.mouse.get_pos()
                game.click(mouseUp)

        # static things
        # update all the things
        game.update()
        # blit all the things
        game.blit()
        # basic systems
        game.clock.tick(60)
