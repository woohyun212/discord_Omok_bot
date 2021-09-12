import numpy as np
from PIL import Image, ImageDraw
import os.path
import json


def isSearched(str='_'):
    filenames = os.listdir('game_saving')
    for filename in filenames:
        full_filename = os.path.join('game_saving', filename)
        if str in full_filename:
            return True
    return False


class OmokGame:
    black = '○'  # player1
    white = '●'  # player2

    def isAnotherGameOnGoing(self):
        # P1vsP2 파일은 없는데, P1 or P2 가 검색되는 경우.
        if not isSearched(f'{self.game_name}.npy') \
                and (isSearched(str(self.player1)) or isSearched(str(self.player2))):
            print("진행중인 게임이 있습니다! 먼저 게임을 종료해주세요!")
            return True
        return False

    def __init__(self, player1, player2):
        self.player1, self.player2 = sorted([player1, player2])
        self.game_name = f'{self.player1}vs{self.player2}'
        self.save_file_location = f'game_saving/{self.game_name}.npy'
        self.color = {self.player1: '흑돌', self.player2: '백돌'}

        if isSearched(f'{self.game_name}.npy'):
            print("진행 중인 게임이 존재합니다. 진행중이던 게임을 불러옵니다.")
            self.LoadGameData()

        else:
            print("진행 중인 게임이 없습니다. 초기화 후 새로운 게임을 시작합니다.")
            with open('game_saving/game_data.json', 'r') as json_file:
                self.game_data = json.load(json_file)
            self.turn = self.player1
            self.board = np.array([[int(i) for i in '0' * 19] for _ in range(19)])
            self.gameSave()

    def __str__(self):
        return f'Player1 = {self.player1} [BLACK] \n' \
               f'Player2 = {self.player2} [WHITE]'

    def __del__(self):
        # np.save(f'game_saving/{self.game_name}', self.board)
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
        with open('game_saving/game_data.json', 'w') as json_file:
            self.game_data[self.game_name] = {"turn": self.turn}
            json.dump(self.game_data, json_file, indent='\t')

        np.save(self.save_file_location[:-4], self.board)

    def gameImageSave(self):
        self.getImageFromBoard().save(f'game_saving/{self.game_name}.png', 'png')  # 이미지 저장

    def LoadGameData(self):
        with open('game_saving/game_data.json') as json_file:
            self.game_data = json.load(json_file)
        self.turn = self.game_data[self.game_name]["turn"]
        self.board = np.load(self.save_file_location, allow_pickle=True)
        pass

    def gameNewStart(self):
        pass

    def gameTerminate(self):
        os.remove(self.save_file_location)

        print('세이브 파일 삭제됨')
        pass

    def isMyTurn(self, req_user):
        return self.turn != req_user

    def isAbleSetStone(self, x, y):
        return self.board[x - 1, y - 1] != 0

    def putStone(self, req_user, x, y):
        if req_user == self.player1:
            # print(al_nu[position[:1]], position[1:], player)
            self.board[x - 1, y - 1] = 1
            self.turn = self.player2
        else:
            # print(al_nu[position[:1]], position[1:], player)
            self.board[x - 1, y - 1] = 2
            self.turn = self.player1

        self.gameSave()


if __name__ == '__main__':
    pass
    o = OmokGame(123, 321)
    del o
    o = OmokGame(123, 321)
    o.putStone(123, 2, 3)
    o.gameSave()
    o.getImageFromBoard().show()
    del o
    o = OmokGame(123, 321)
    o.putStone(321, 3, 3)
    o.getImageFromBoard().show()
    del o

# del o
