# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## composition.py
# ## 
# ##############################################################################
# =============================================================================>
# imports
import random

import numpy

def _make_target_edge(edge, target_edge = (True, True), target_position = (True, True)):
    _target = [(0, 0), (0, 0)]

    if not target_edge[0]:
        _target[0] = (0, 0)
    else:
        _a_a, _a_b = 0, 0
        if target_position[0]:
            _a_a = edge[0][0]
        if target_position[1]:
            _a_b = edge[0][1]
        _target[0] = (_a_a, _a_b)
    
    if not target_edge[1]:
        _target[1] = (0, 0)
    else:
        _a_a, _a_b = 0, 0
        if target_position[0]:
            _a_a = edge[1][0]
        if target_position[1]:
            _a_b = edge[1][1]
        _target[1] = (_a_a, _a_b)
    
    return _target

def edge_search(edge_list, edge, target_edge = (True, True), target_position = (True, True)):
    """
    """
    # targetの無視する項を全て0に変更
    _target_a = _make_target_edge(edge, target_edge = target_edge, target_position = target_position)

    for i in range(len(edge_list)):
        _target_b = _make_target_edge(edge_list[i], target_edge = target_edge, target_position = target_position)
        if (_target_a[0][0] == _target_b[0][0]) and (_target_a[1][0] == _target_b[1][0]): 
            if (_target_a[0][1] == _target_b[0][1]) and (_target_a[1][1] == _target_b[1][1]):
                return i
    
    return None

def get_euc(a, b):
    return numpy.sqrt(numpy.sum(numpy.square(numpy.array(a) - numpy.array(b))))

def get_nearest_edge(edge_list, edge):
    _dist = [get_euc(edge[0], i[0]) + get_euc(edge[1], i[1]) for i in edge_list]
    return edge_list[_dist.index(min(_dist))]

def get_insert_position(edge_list, point, target):
    i = len(edge_list) - 1

    if len(edge_list) <= 0:
        return 0
    elif len(edge_list) == 1:
        if edge_list[0][0][target] > point[target]:
            return 0
        else:
            return 1
    else:
        i -= 1
        while (i >= 0):
            if not edge_list[i][0][target] > point[target]: # 辺の位置を通り過ぎた
                break
            i -= 1
        return i + 1

def line_fit_h(random_point_x, pos_h, edge_list_h):
    _pos_h_a = pos_h - 1
    _pos_h_b = pos_h

    while _pos_h_a > 0:
        # 線分が届くまで減らす
        if ((edge_list_h[_pos_h_a][1][0] >= random_point_x) and (edge_list_h[_pos_h_a][0][0] <= random_point_x)):
            break
        _pos_h_a -= 1
    
    while _pos_h_b < (len(edge_list_h) - 1):
        # 線分が届くまで増やす
        if ((edge_list_h[_pos_h_b][1][0] >= random_point_x) and (edge_list_h[_pos_h_b][0][0] <= random_point_x)):
            break
        _pos_h_b += 1
    
    return _pos_h_a, _pos_h_b

def line_fit_v(random_point_y, pos_v, edge_list_v):
    _pos_v_a = pos_v - 1
    _pos_v_b = pos_v

    while _pos_v_a > 0:
        # 線分が届くまで減らす
        if ((edge_list_v[_pos_v_a][1][1] >= random_point_y) and (edge_list_v[_pos_v_a][0][1] <= random_point_y)):
            break
        _pos_v_a -= 1
    
    while _pos_v_b < (len(edge_list_v) - 1):
        # 線分が届くまで増やす
        if ((edge_list_v[_pos_v_b][1][1] >= random_point_y) and (edge_list_v[_pos_v_b][0][1] <= random_point_y)):
            break
        _pos_v_b += 1
    
    return _pos_v_a, _pos_v_b

class BasicRandomImage:
    """BasicRandomImage
    """

    def __init__(self, width = 1.0, height = 1.0, seed = None):
        if seed == None:
            self.seed = random.random()
        else:
            self.seed = seed
        self.w = width
        self.h = height
        self.random_value_count = 1
    
    def __str__(self):
        return "BasicRandomImage {} x {}, seed:{}".format(self.w, self.h, self.seed)
    
    # =========================================================================>
    # GET
    def get_random_value(self, custom_seed = None):
        if custom_seed is None:
            random.seed(self.seed * self.random_value_count)
        else:
            random.seed(custom_seed * self.random_value_count)
        
        self.random_value_count += 1
        return random.random()
    
    @property
    def seed(self):
        return self.__seed
    
    @property
    def w(self):
        return self.__w
    
    @property
    def width(self):
        return self.__w

    @property
    def h(self):
        return self.__h
    
    @property
    def height(self):
        return self.__h
    
    # =========================================================================>
    # SET
    @seed.setter
    def seed(self, seed):
        if seed is None:
            raise TypeError('invalid seed')
        self.__seed = seed
    
    @w.setter
    def w(self, width):
        if width is None or width <= 0:
            raise TypeError('invalid width')
        self.__w = width
    
    @h.setter
    def h(self, height):
        if height is None or height <= 0:
            raise TypeError('invalid height')
        self.__h = height
    
    @width.setter
    def width(self, width):
        self.w = width
    
    @height.setter
    def height(self, height):
        self.h = height

class CompositionRandomImage(BasicRandomImage):
    """CompositionRandomImage
    """

    def __init__(self, n_line = 10, seed = None):
        super().__init__(1.0, 1.0, seed)
        self._edge_list_h = []
        self._edge_list_v = []
        self.init_image()
        self.generate_image(n_line)

    def __str__(self):
        return "CompositionRandomImage {} x {}, seed:{}".format(self.w, self.h, self.seed)

    # =========================================================================>
    # OTHER
    def init_image(self):
        self._edge_list_h = [
            [(0,      0), (self.w,      0)], # top
            [(0, self.h), (self.w, self.h)]  # bottom
        ]

        self._edge_list_v = [
            [(0,      0), (0,      self.h)], # left
            [(self.w, 0), (self.w, self.h)]  # right
        ]
        self.random_value_count = 1
    
    def generate_image(self, n_line, n_toend_line = None, max_rect_size = (1.0, 1.0), min_rect_size = (0.0, 0.0)):
        """_summary_

        Args:
            n_line (_type_): _description_
            n_toend_line (int, optional): set number of lines to end of window. Defaults to None.
            max_rect_size (tuple, optional): set maximum rectangle size. Defaults to (1.0, 1.0).
            min_rect_size (tuple, optional): set minimum rectangle size. Defaults to (0.0, 0.0).

        Returns:
            (list)
        """

        is_vertical = True # 縦線モード
        
        for i in range(n_line):
            random_point_x = self.get_random_value()
            random_point_y = self.get_random_value()

            _pos_h = get_insert_position(
                self._edge_list_h, 
                (random_point_x, random_point_y),
                target = 1
            )
            _pos_v = get_insert_position(
                self._edge_list_v, 
                (random_point_x, random_point_y),
                target = 0
            )

            if is_vertical:
                _pos_h_a, _pos_h_b = line_fit_h(random_point_x, _pos_h, self._edge_list_h)

                new_pos = [
                    (random_point_x, self._edge_list_h[_pos_h_a][0][1]), 
                    (random_point_x, self._edge_list_h[_pos_h_b][0][1])
                ]

                self._edge_list_v = self._edge_list_v[:_pos_v] + [new_pos] + self._edge_list_v[_pos_v:]
            else:
                _pos_v_a, _pos_v_b = line_fit_v(random_point_y, _pos_v, self._edge_list_v)

                new_pos = [
                    (self._edge_list_v[_pos_v_a][0][0], random_point_y), 
                    (self._edge_list_v[_pos_v_b][0][0], random_point_y)
                ]

                self._edge_list_h = self._edge_list_h[:_pos_h] + [new_pos] + self._edge_list_h[_pos_h:]
            
            is_vertical = not is_vertical
        
        # 線を分割
        _tmp_h = []
        _tmp_v = []

        for i in range(len(self._edge_list_h)):
            _tmp_h_a = self._edge_list_h[i]
            for j in self._edge_list_v[1:]:
                if (_tmp_h_a[0][0] <= j[0][0]) and (j[0][0] <= _tmp_h_a[1][0]): # 範囲内
                    if (_tmp_h_a[0][1] <= j[1][1]) and (j[0][1] <= _tmp_h_a[0][1]): # 範囲内
                        if not ((_tmp_h_a[0][0] == j[0][0]) and (_tmp_h_a[0][1] == _tmp_h_a[1][1])): # 点でない
                            if not (i == (len(self._edge_list_h) - 1) or i == 0):
                                _tmp_h.append([_tmp_h_a[0], (j[0][0], _tmp_h_a[1][1])])
                            _tmp_h.append([_tmp_h_a[0], (j[0][0], _tmp_h_a[1][1])])
                        _tmp_h_a = [(j[0][0], _tmp_h_a[0][1]), _tmp_h_a[1]]
        
        for i in range(len(self._edge_list_v)):
            _tmp_v_a = self._edge_list_v[i]
            for j in self._edge_list_h[1:]:
                if (_tmp_v_a[0][1] <= j[0][1]) and (j[0][1] <= _tmp_v_a[1][1]): # 範囲内
                    if (_tmp_v_a[0][0] <= j[1][0]) and (j[0][0] <= _tmp_v_a[0][0]): # 範囲内
                        if not ((_tmp_v_a[0][0] == _tmp_v_a[1][0]) and (_tmp_v_a[0][1] == j[0][1])): # 点でない
                            if not (i == (len(self._edge_list_v) - 1) or i == 0):
                                _tmp_v.append([_tmp_v_a[0], (_tmp_v_a[1][0], j[0][1])])
                            _tmp_v.append([_tmp_v_a[0], (_tmp_v_a[1][0], j[0][1])])
                        _tmp_v_a = [(_tmp_v_a[0][0], j[0][1]), _tmp_v_a[1]]
        
        self._edge_list_h = _tmp_h
        self._edge_list_v = _tmp_v

    # =========================================================================>
    # GET
    def get_edges(self):
        """get_intersections
        Description:
            return edges
        Return:
            List
        """
        return self._edge_list_v + self._edge_list_h
    
    def get_intersections(self):
        """get_intersections
        Description:
            change format from edge_list to point of intersections
        Return:
            List
        """
        # 交点のみのデータに変換
        edge_list = self.get_edges()
        node_list = []

        for i in edge_list:
            node_list.append(i[0])
            node_list.append(i[1])

        node_list = list(set(node_list))

        return node_list
    
    def get_rectangles(self):
        """get_intersections
        Description:
            change format from edge_list to rectangles
        Return:
            List
        """
        rect_nodes = []
        tmp_nodes_tl = []
        tmp_nodes_br = []
        _tmp_v_alone = []
        _tmp_h_alone = []
        _tmp_v = self._edge_list_v.copy()
        _tmp_h = self._edge_list_h.copy()
        
        # top and left, bottom and rightの組み合わせを作る
        while not len(_tmp_v) < 1: # 左上の組
            _left = _tmp_v.pop(0)
            _another_left_index = edge_search(_tmp_v, _left)
            if not _another_left_index is None:
                _tmp_v_alone.append(_tmp_v.pop(_another_left_index))
            
            _top_index = edge_search(_tmp_h, _left, target_edge = (True, False), target_position = (True, True))
            if _top_index is None:
                # right max or middle path
                _tmp_v_alone.append(_left)
            else:
                _h = _tmp_h.pop(_top_index)
                tmp_nodes_tl.append(
                    [
                        _left[1], 
                        _h[1],
                        _left[0] # 角
                    ]
                )
        
        while not len(_tmp_h) < 1: # 右下の組
            _bottom = _tmp_h.pop(0)
            _another_bottom_index = edge_search(_tmp_h, _bottom)
            if not _another_bottom_index is None:
                _tmp_h_alone.append(_tmp_h.pop(_another_bottom_index))
            
            _right_index = edge_search(_tmp_v_alone, _bottom, target_edge = (False, True), target_position = (True, True))
            if _right_index is None:
                # right max or middle path
                _tmp_h_alone.append(_bottom)
            else:
                _r = _tmp_v_alone.pop(_right_index)
                tmp_nodes_br.append(
                    [
                        _bottom[0], 
                        _r[0],
                        _bottom[1] # 角
                    ]
                )
        
        # 左上と右下をくっつける
        _leave_tl = []
        is_pass = 0
        while not len(tmp_nodes_tl) < 1:
            for i in range(len(tmp_nodes_br)):
                if tmp_nodes_br[i][0] == tmp_nodes_tl[0][0]:
                    if tmp_nodes_br[i][1] == tmp_nodes_tl[0][1]:
                        # 閉じて四角形になったら追加
                        rect_nodes.append(
                            [tmp_nodes_tl[0][2], tmp_nodes_br[i][2]]
                        )

                        tmp_nodes_br.pop(i)
                        tmp_nodes_tl.pop(0)
                        is_pass = 0
                        break
                    else: # 右上の不一致
                        # 足りない方向に少し伸ばしてキューの一番後ろに追加
                        if not tmp_nodes_br[i][1][0] == tmp_nodes_tl[0][1][0]:
                            # tlの後ろにhを追加
                            _new = tmp_nodes_tl[0]
                            _add = edge_search(
                                _tmp_h_alone, (_new[1], (0, 0)), 
                                target_edge = (True, False), target_position = (True, True)
                            )
                            if not _add is None:
                                _new[1] = _tmp_h_alone[_add][1]
                                tmp_nodes_tl.append(_new)
                                tmp_nodes_br.append(tmp_nodes_br[i])
                                _tmp_h_alone.pop(_add)
                            else:
                                print("err")
                        if not tmp_nodes_br[i][1][1] == tmp_nodes_tl[0][1][1]:
                            # brの前にvを追加
                            _new = tmp_nodes_br[i]
                            _add = edge_search(
                                _tmp_v_alone, ((0, 0), _new[1]), 
                                target_edge = (False, True), target_position = (True, True)
                            )
                            if not _add is None:
                                _new[1] = _tmp_v_alone[_add][0]
                                tmp_nodes_br.append(_new)
                                tmp_nodes_tl.append(tmp_nodes_tl[0])
                                _tmp_v_alone.pop(_add)
                            else:
                                print("err")
                        
                        tmp_nodes_br.pop(i)
                        tmp_nodes_tl.pop(0)
                        break
                else:
                    if tmp_nodes_br[i][1] == tmp_nodes_tl[0][1]: # 左下の不一致
                        # 足りない方向に少し伸ばしてキューの一番後ろに追加
                        if not tmp_nodes_br[i][0][0] == tmp_nodes_tl[0][0][0]:
                            # brの後ろにhを追加
                            _new = tmp_nodes_br[i]
                            _add = edge_search(
                                _tmp_h_alone, ((0, 0), _new[0]), 
                                target_edge = (False, True), target_position = (True, True)
                            )
                            if not _add is None:
                                _new[0] = _tmp_h_alone[_add][0]
                                tmp_nodes_br.append(_new)
                                tmp_nodes_tl.append(tmp_nodes_tl[0])
                                _tmp_h_alone.pop(_add)
                            else:
                                print("err3")
                        if not tmp_nodes_br[i][0][1] == tmp_nodes_tl[0][0][1]:
                            # tlの前にvを追加
                            _new = tmp_nodes_tl[0]
                            _add = edge_search(
                                _tmp_v_alone, (_new[0], (0, 0)), 
                                target_edge = (True, False), target_position = (True, True)
                            )
                            if not _add is None:
                                _new[0] = _tmp_v_alone[_add][1]
                                tmp_nodes_tl.append(_new)
                                tmp_nodes_br.append(tmp_nodes_br[i])
                                _tmp_v_alone.pop(_add)
                            else:
                                print("err4")
                        
                        tmp_nodes_br.pop(i)
                        tmp_nodes_tl.pop(0)
                        break
                    else: # 少しも一致していない場合は次に渡す
                        pass
            if is_pass < 5:
                is_pass += 1
            else:
                _leave_tl.append(tmp_nodes_tl[0])
                tmp_nodes_tl.pop(0)
        
        tmp_nodes_tl = _leave_tl
        # 余りを近い順に結合
        for i in tmp_nodes_tl:
            rect_nodes.append([i[2], get_nearest_edge(tmp_nodes_br, i)[2]])
        
        # (x, y, width, height)に変更
        return rect_nodes # ((lt x, lt y), (rb x, rb y))

    # =========================================================================>
    # SET

if __name__ == "__main__":
    pass
    