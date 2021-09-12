import numpy as np
from PIL import Image, ImageDraw
import os.path


class OngoingException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CannotSetStoneException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def isSearched(str='_'):
    filenames = os.listdir('game_saving')
    for filename in filenames:
        full_filename = os.path.join('game_saving', filename)
        # print(1, str)
        # print(2, full_filename)
        if str in full_filename:
            return True
    return False


class OmokGame:
    black = '○'  # player1
    white = '●'  # player2

    def __init__(self, player1, player2):
        self.player1, self.player2 = sorted([player1, player2])

        if isSearched(f'{self.player1}vs{self.player2}.npy'):
            print("진행 중인 게임이 존재합니다. 진행중이던 게임을 불러옵니다.")
            self.board = self.getLoadGameData()
            # P1vsP2 파일은 없는데, P1 or P2 가 검색되는 경우.
            self.save_file_location = f'game_saving/{self.player1}vs{self.player2}.npy'

        elif not isSearched(f'{self.player1}vs{self.player2}.npy') \
                and (isSearched(str(self.player1)) or isSearched(str(self.player2))):
            print("진행중인 게임이 있습니다! 먼저 게임을 종료해주세요!")
            raise OngoingException('The game is Ongoing.')

        else:
            print("진행 중인 게임이 없습니다. 초기화 후 새로운 게임을 시작합니다.")
            self.board = np.array([[int(i) for i in '0' * 19] for _ in range(19)])
            self.gameSave()
            self.save_file_location = f'game_saving/{self.player1}vs{self.player2}.npy'

    def __str__(self):
        return f'Player1 = {self.player1} [BLACK] \n' \
               f'Player2 = {self.player2} [WHITE]'

    def __del__(self):
        # np.save(f'game_saving/{self.player1}vs{self.player2}', self.board)
        # self.gameSave()
        pass

    def getStringFromBoard(self):
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

    def getImageFromBoard(self):
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
        # img_board.show()
        return img_board

    def gameSave(self):
        np.save(f'game_saving/{self.player1}vs{self.player2}', self.board)

    def gameImageSave(self):
        self.getImageFromBoard().save(f'game_saving/{self.player1}vs{self.player2}.png', 'png')  # 이미지 저장

    def getLoadGameData(self):
        return np.load(f'game_saving/{self.player1}vs{self.player2}.npy')

    def gameNewStart(self):
        pass

    def gameTerminate(self):
        os.remove(self.save_file_location)
        print('세이브 파일 삭제됨')
        pass

    def putStone(self, req_user, position: str):
        position = position.upper()
        al_nu = dict(zip('ABCDEFGHIJKLMNOPQRS', map(int, '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19'.split())))
        x, y = al_nu[position[:1]], int(position[1:])
        if self.board[x - 1, y - 1] != 0:
            raise CannotSetStoneException("Cannot Set Stone at the position")
        if req_user == self.player1:
            # print(al_nu[position[:1]], position[1:], player)
            self.board[x - 1, y - 1] = 1
        else:
            # print(al_nu[position[:1]], position[1:], player)
            self.board[x - 1, y - 1] = 2


if __name__ == '__main__':
    pass
    o = OmokGame(12345, 54321)
    del o
    o = OmokGame(12345, 54321)
    o.putStone(123, 'A1')
    o.putStone(321, 'B4')
    o.getImageFromBoard().show()
    del o
    o = OmokGame(12345, 54321)
    o.gameTerminate()

# del o
