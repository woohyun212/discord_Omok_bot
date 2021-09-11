import numpy as np
from PIL import Image, ImageDraw, ImageFilter


class OthelloGame:
    white = '○'
    black = '●'
    board = np.array([[int(i) for i in '0' * 19] for j in range(19)])

    def __init__(self, player1, player2):
        self.player1, self.player2 = player1, player2

    def __str__(self):
        return f'Player1 = {self.player1} [BLACK] \n' \
               f'Player2 = {self.player2} [WHITE]'

    def __del__(self):
        print(f"{self.player1}와 {self.player2}의 게임이 종료되었어요!")

    def getTextBoard(self):
        board_str = list(map(int, self.board.flat))
        for index in enumerate(board_str):
            if board_str[index[0]] == 1:
                board_str[index[0]] = self.black
            elif board_str[index[0]] == 2:
                board_str[index[0]] = self.white
            elif board_str[index[0]] == 0:
                board_str[index[0]] = ' '
        board = np.array(board_str).reshape(19, 19)
        set_style = '\033[04m'
        line_head = '0 │' + '│'.join('ABCDEFGHIJKLMNOPQRS') + '│\n'
        line_body = [f'{rank[0] + 1:<2}│{"│".join(rank[1])}│\n' for rank in enumerate(board)]
        end_style = '\033[00m'
        board = set_style + line_head + ''.join(line_body) + end_style
        return board

    def getImageBoard(self):
        pixel_pos = {1: 52, 2: 102, 3: 151, 4: 200, 5: 249, 6: 298, 7: 347, 8: 396, 9: 445, 10: 500, 11: 554, 12: 603,
                     13: 652, 14: 701, 15: 750, 16: 799, 17: 848, 18: 898, 19: 947}
        img_board = Image.open('omokBoard.png')
        stone_size = 40
        for enu_x in enumerate(self.board):
            # print(enu_x[0], end=' ')
            for enu_y in enumerate(enu_x[1]):
                # print(enu_y[1], end=' ')
                if enu_y[1] != 0:
                    x_pos, y_pos = pixel_pos[enu_x[0] + 1], pixel_pos[enu_y[0] + 1]
                    x_pos -= stone_size / 2
                    y_pos -= stone_size / 2
                    if enu_y[1] == 1:
                        ImageDraw.Draw(img_board).ellipse((x_pos, y_pos, x_pos + stone_size, y_pos + stone_size),
                                                          fill='black',
                                                          outline='black')
                    else:
                        ImageDraw.Draw(img_board).ellipse((x_pos, y_pos, x_pos + stone_size, y_pos + stone_size),
                                                          fill='white',
                                                          outline='black')
            # print()
        img_board.show()
        return img_board

    def gameStart(self):
        pass

    def putStone(self, player, x, y):
        if player == self.player1:
            self.board[x - 1, y - 1] = 1
        else:
            self.board[x - 1, y - 1] = 2


if __name__ == '__main__':
    pass
    o = OthelloGame(1, 2)
    o.gameStart()
    o.putStone(1, 11, 11)
    o.putStone(1, 12, 12)
    o.putStone(1, 13, 13)
    o.putStone(1, 14, 14)
    o.putStone(2, 15, 15)
    print(o.getImageBoard())
    del o
