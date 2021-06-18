import unittest
import pykle_serial as serial


class TestDeserialization(unittest.TestCase):
    def test_a_a(self):
        with self.assertRaises(ValueError, msg="should fail on non-array"):
            serial.deserialize("test")

    def test_a_b(self):
        with self.assertRaises(ValueError, msg="should fail on non array/object data"):
            serial.deserialize(["test"])

    def test_a_c(self):
        msg = "should return empty keyboard on empty array"
        result = serial.deserialize([])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 0, msg

    # metadata
    def test_b_a(self):
        msg = "should parse from first object if it exists"
        result = serial.deserialize([{"name": "test"}])
        self.assertIsInstance(result, serial.Keyboard, msg)
        self.assertEqual(result.meta.name, "test", msg)

    def test_b_b(self):
        with self.assertRaises(ValueError, msg="should throw an exception if found anywhere other than the start"):
            serial.deserialize([[], {"name": "test"}])

    # key positions
    def test_c_a(self):
        msg = "should default to (0,0)"
        result = serial.deserialize([["1"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].x == 0, msg
        assert result.keys[0].y == 0, msg

    def test_c_b(self):
        msg = "should increment x position by the width of the previous key"
        result = serial.deserialize([[{"x": 1}, "1", "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].x == 1, msg
        assert result.keys[1].x == result.keys[0].x + result.keys[0].width, msg
        assert result.keys[1].y == result.keys[0].y, msg

    def test_c_d(self):
        msg = "should increment y position whenever a new row starts, and reset x to zero"
        result = serial.deserialize([[{'y': 1}, "1"], ["2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].y == 1, msg
        assert result.keys[0].x == 0, msg
        assert result.keys[1].y == result.keys[0].y + 1, msg

    def test_c_e(self):
        msg = "should add x and y to current position"
        result = serial.deserialize([["1", {'x': 1}, "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].x == 0, msg
        assert result.keys[1].x == 2, msg

        result = serial.deserialize([["1"], [{'y': 1}, "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].y == 0, msg
        assert result.keys[1].y == 2, msg

    def test_c_f(self):
        msg = "should leave x2,y2 at (0,0) if not specified"
        result = serial.deserialize([[{'x': 1, 'y': 1}, "1"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].x != 0, msg
        assert result.keys[0].y != 0, msg
        assert result.keys[0].x2 == 0, msg
        assert result.keys[0].y2 == 0, msg

        result = serial.deserialize([
            [{'x': 1, 'y': 1, 'x2': 2, 'y2': 2}, "1"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].x != 0, msg
        assert result.keys[0].y != 0, msg
        assert result.keys[0].x2 != 0, msg
        assert result.keys[0].y2 != 0, msg

    def test_c_g(self):
        msg = "should add x and y to center of rotation"
        result = serial.deserialize([[{'r': 10, 'rx': 1, 'ry': 1, 'y': -1.1, 'x': 2}, "E"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].x == 3, msg
        self.assertAlmostEqual(result.keys[0].y, -0.1)

    # key sizes
    def test_d_a(self):
        msg = "should reset width and height to 1"
        result = serial.deserialize([[{'w': 5}, "1", "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].width == 5, msg
        assert result.keys[1].width == 1, msg

        result = serial.deserialize([[{'h': 5}, "1", "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].height == 5, msg
        assert result.keys[1].height == 1, msg

    def test_d_b(self):
        msg = "should default width2/height2 if not specified"
        result = serial.deserialize([
            [{'w': 2, 'h': 2}, "1", {'w': 2, 'h': 2, 'w2': 4, 'h2': 4}, "2"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].width2 == result.keys[0].width, msg
        assert result.keys[0].height2 == result.keys[0].height, msg
        assert result.keys[1].width2 != result.keys[1].width, msg
        assert result.keys[1].height2 != result.keys[1].height, msg

    # other properties
    def test_e_a(self):
        msg = "should reset stepped, homing, and decal flags to false"
        result = serial.deserialize([
            [{'l': True, 'n': True, 'd': True}, "1", "2"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].stepped, msg
        assert result.keys[0].nub, msg
        assert result.keys[0].decal, msg
        self.assertFalse(result.keys[1].stepped, msg)
        self.assertFalse(result.keys[1].nub, msg)
        self.assertFalse(result.keys[1].decal, msg)

    def test_e_b(self):
        msg = "should propagate the ghost flag"
        result = serial.deserialize([["0", {'g': True}, "1", "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 3, msg
        self.assertFalse(result.keys[0].ghost, msg)
        assert result.keys[1].ghost, msg
        assert result.keys[2].ghost, msg

    def test_e_c(self):
        msg = "should propagate the profile flag"
        result = serial.deserialize([["0", {'p': "DSA"}, "1", "2"]])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 3, msg
        assert len(result.keys[0].profile) == 0, msg
        assert result.keys[1].profile == 'DSA', msg
        assert result.keys[2].profile == 'DSA', msg

    def test_e_d(self):
        msg_root = "should propagate switch properties"

        result = serial.deserialize([["1", {'sm': "cherry"}, "2", "3"]])
        self.assertIsInstance(result, serial.Keyboard, msg_root + " :sm")
        assert len(result.keys) == 3, msg_root + " :sm"
        assert result.keys[0].sm == "", msg_root + " :sm_0"
        assert result.keys[1].sm == "cherry", msg_root + " :sm_1"
        assert result.keys[2].sm == "cherry", msg_root + " :sm_2"

        result = serial.deserialize([["1", {'sb': "cherry"}, "2", "3"]])
        self.assertIsInstance(result, serial.Keyboard, msg_root + " :sb")
        assert len(result.keys) == 3, msg_root + " :sb"
        assert result.keys[0].sb == "", msg_root + " :sb_0"
        assert result.keys[1].sb == "cherry", msg_root + " :sb_1"
        assert result.keys[2].sb == "cherry", msg_root + " :sb_2"

        result = serial.deserialize([
            ["1", {'st': "MX1A-11Nx"}, "2", "3"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg_root + " :st")
        assert len(result.keys) == 3, msg_root + " :st"
        assert result.keys[0].st == "", msg_root + " :st_0"
        assert result.keys[1].st == "MX1A-11Nx", msg_root + " :st_1"
        assert result.keys[2].st == "MX1A-11Nx", msg_root + " :st_2"

    # text color
    def test_f_a(self):
        msg = "should apply colors to all subsequent keys"
        result = serial.deserialize([
            [{'c': "#ff0000", 't': "#00ff00"}, "1", "2"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].color == "#ff0000", msg
        assert result.keys[1].color == "#ff0000", msg
        assert result.keys[0].default.textColor == "#00ff00", msg
        assert result.keys[1].default.textColor == "#00ff00", msg

    def test_f_b(self):
        msg = "should apply `t` to all legends"
        result = serial.deserialize([
            [{'a': 0, 't': "#444444"}, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].default.textColor == "#444444"
        for i in range(serial.UB_LABEL_MAP):
            self.assertIsNone(result.keys[0].textColor[i], msg + " :" + str(i))

    def test_f_c(self):
        msg = "should handle generic case"
        labels = "#111111\n#222222\n#333333\n#444444\n" + \
            "#555555\n#666666\n#777777\n#888888\n" + \
            "#999999\n#aaaaaa\n#bbbbbb\n#cccccc"
        result = serial.deserialize([
            [{'a': 0, 't': labels}, labels]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].default.textColor == "#111111", msg
        for i in range(serial.UB_LABEL_MAP):
            assert (result.keys[0].textColor[i] or result.keys[0].default.textColor) == result.keys[0].labels[i], msg + " :i=" + str(i)

    def test_f_d(self):
        msg = "should handle blanks"
        labels = "#111111\nXX\n#333333\n#444444\n" + \
            "XX\n#666666\nXX\n#888888\n" + \
            "#999999\n#aaaaaa\n#bbbbbb\n#cccccc"
        result = serial.deserialize([
            [{'a': 0, 't': labels.replace('XX', '')}, labels]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 1, msg
        assert result.keys[0].default.textColor == "#111111"
        for i in range(serial.UB_LABEL_MAP):
            # if blank, should be same as color[0] / default
            color = result.keys[0].textColor[i] or result.keys[0].default.textColor
            if result.keys[0].labels[i] == "XX":
                assert color == "#111111", msg + ' :i=' + str(i)
            else:
                assert color == result.keys[0].labels[i], msg + ' :i=' + str(i)

    def test_f_e(self):
        msg = "should not reset default color if blank"
        result = serial.deserialize([
            [{'t': "#ff0000"}, "1", {'t': "\n#00ff00"}, "2"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].default.textColor == "#ff0000", msg + " [0]"
        assert result.keys[1].default.textColor == "#ff0000", msg + " [1]"

    def test_f_f(self):
        msg = "should delete values equal to the default"
        result = serial.deserialize([
            [
                {'t': "#ff0000"},
                "1",
                {'t': "\n#ff0000"},
                "\n2",
                {'t': "\n#00ff00"},
                "\n3"
            ]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 3, msg
        assert result.keys[1].labels[6] == "2"
        self.assertIsNone(result.keys[1].textColor[6])
        assert result.keys[2].labels[6] == "3"
        assert result.keys[2].textColor[6] == "#00ff00"

    # rotation
    def test_g_a(self):
        msg = "should not be allowed on anything but the first key in a row"
        try:
            _ = serial.deserialize([[{'r': 45}, "1", "2"]])
            _ = serial.deserialize([[{'rx': 45}, "1", "2"]])
            _ = serial.deserialize([[{'ry': 45}, "1", "2"]])
        except:  # noqa
            self.fail(msg)

        with self.assertRaises(ValueError, msg=msg):
            _ = serial.deserialize([["1", {'r': 45}, "2"]])
        with self.assertRaises(ValueError, msg=msg):
            _ = serial.deserialize([["1", {'rx': 45}, "2"]])
        with self.assertRaises(ValueError, msg=msg):
            _ = serial.deserialize([["1", {'ry': 45}, "2"]])

    # legends
    def test_h_a(self):
        msg_root = "should align legend positions correctly"

        # Some history, to make sense of this:
        # 1. Originally, you could only have top & botton legends, and they were
        #    left-aligned. (top:0 & bottom:1)
        # 2. Next, we added right-aligned labels (top:2 & bottom:3).
        # 3. Next, we added front text (left:4, right:5).
        # 4. Next, we added the alignment flags that allowed you to move the
        #    labels (0-5) to the centered positions (via checkboxes).
        # 5. Nobody understood the checkboxes.  They were removed in favor of
        #    twelve separate label editors, allowing text to be placed anywhere.
        #    This introduced labels 6 through 11.
        # 6. The internal rendering is now Top->Bottom, Left->Right, but to keep
        #    the file-format unchanged, the serialization code now translates
        #    the array from the old layout to the new internal one.

        n = None
        expected = [
            #  top row        middle row      bottom row         front
            ["0","8","2",    "6","9","7",    "1","10","3",    "4","11","5"], # a=0                  # noqa
            [ n ,"0", n ,     n ,"6", n ,     n , "1", n ,    "4","11","5"], # a=1 (center horz)    # noqa
            [ n , n , n ,    "0","8","2",     n ,  n , n ,    "4","11","5"], # a=2 (center vert)    # noqa
            [ n , n , n ,     n ,"0", n ,     n ,  n , n ,    "4","11","5"], # a=3 (center both)    # noqa

            ["0","8","2",    "6","9","7",    "1","10","3",     n , "4", n ], # a=4 (center front)       # noqa
            [ n ,"0", n ,     n ,"6", n ,     n , "1", n ,     n , "4", n ], # a=5 (center front+horz)  # noqa
            [ n , n , n ,    "0","8","2",     n ,  n , n ,     n , "4", n ], # a=6 (center front+vert)  # noqa
            [ n , n , n ,     n ,"0", n ,     n ,  n , n ,     n , "4", n ], # a=7 (center front+both)  # noqa
        ]
        del n
        ub_expected_col = 8
        for a in range(ub_expected_col):
            msg = msg_root + " a=" + str(a)
            result = serial.deserialize([
                [{'a': a}, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11"]
            ])
            self.assertIsNotNone(expected[a], msg)
            self.assertIsInstance(result, serial.Keyboard, msg)
            assert len(result.keys) == 1, msg
            assert len(result.keys[0].labels) == len(expected[a]), msg
            assert set(result.keys[0].labels) == set(expected[a]), msg

    # font sizes
    def test_i_a(self):
        msg_root = "should handle `f` at all alignments"
        ub = 7
        for a in range(ub):
            msg = msg_root + " a=" + str(a)
            result = serial.deserialize([
                [{'f': 1, 'a': a}, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11"]
            ])
            self.assertIsInstance(result, serial.Keyboard, msg)
            assert len(result.keys) == 1, msg
            assert result.keys[0].default.textSize == 1, msg
            self.assertFalse(any(result.keys[0].textSize), msg)

    def test_i_b(self):
        msg_root = "should handle `f2` at all alignments"
        ub = 7
        for a in range(ub):
            msg = msg_root + " a=" + str(a)
            result = serial.deserialize([
                [{'f': 1, 'f2': 2, 'a': a}, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11"]
            ])
            self.assertIsInstance(result, serial.Keyboard, msg)
            assert len(result.keys) == 1, msg
            # All labels should be 2, except the first one ('0')
            for i in range(serial.UB_LABEL_MAP):
                msg = msg_root + " a=" + str(a) + "[" + str(i) + "]"
                if result.keys[0].labels[i]:
                    if result.keys[0].labels[i] == "0":
                        self.assertIsNone(result.keys[0].textSize[i], msg)
                    else:
                        assert result.keys[0].textSize[i] == 2
                else:
                    # no text at [i]; textSize should be undefined
                    self.assertIsNone(result.keys[0].textSize[i], msg)

    def test_i_c(self):
        msg_root = "should handle `fa` at all alignments"
        ub = 7
        for a in range(ub):
            msg = msg_root + " a=" + str(a)
            result = serial.deserialize([
                [
                    {'f': 1, 'fa': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 'a': a},
                    "2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13"
                ]
            ])
            self.assertIsInstance(result, serial.Keyboard, msg)
            assert len(result.keys) == 1, msg
            for i in range(serial.UB_LABEL_MAP):
                msg = msg_root + " a=" + str(a) + "[" + str(i) + "]"
                if result.keys[0].labels[i]:
                    assert result.keys[0].textSize[i] == int(result.keys[0].labels[i])

    def test_i_d(self):
        msg_root = "should handle blanks in `fa`"
        ub = 7
        for a in range(ub):
            msg = msg_root + " a=" + str(a)
            result = serial.deserialize([
                [
                    {'f': 1, 'fa': [None, 2, None, 4, None, 6, None, 8, 9, 10, None, 12], 'a': a},
                    "x\n2\nx\n4\nx\n6\nx\n8\n9\n10\nx\n12"
                ]
            ])
            self.assertIsInstance(result, serial.Keyboard, msg)
            assert len(result.keys) == 1, msg
            for i in range(serial.UB_LABEL_MAP):
                msg = msg_root + " a=" + str(a) + "[" + str(i) + "]"
                if result.keys[0].labels[i] == "x":
                    self.assertIsNone(result.keys[0].textSize[i], msg)

    def test_i_e(self):
        msg = "should not reset default size if blank"
        result = serial.deserialize([
            [{'f': 1}, "1", {'fa': [None, 2]}, "2"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 2, msg
        assert result.keys[0].default.textSize == 1, msg + "[0]"
        assert result.keys[1].default.textSize == 1, msg + "[1]"

    def test_i_f(self):
        msg = "should delete values equal to the default"
        result = serial.deserialize([
            [{'f': 1}, "1", {'fa': "\n1"}, "\n2", {'fa': "\n2"}, "\n3"]
        ])
        self.assertIsInstance(result, serial.Keyboard, msg)
        assert len(result.keys) == 3, msg
        assert result.keys[1].labels[6] == "2", msg
        self.assertIsNone(result.keys[1].textSize[6], msg)
        assert result.keys[2].labels[6] == "3", msg
        assert result.keys[2].textSize[6] == 2, msg

    # strings
    def test_j_a(self):
        msg = "should be lenient about quotes"
        try:
            result1 = serial.parse('''[
                { name: "Sample", author: "Your Name" },
                ["Q", "W", "E", "R", "T", "Y"]
            ]''')
            result2 = serial.parse('''[
                { "name": "Sample", "author": "Your Name" },
                ["Q", "W", "E", "R", "T", "Y"]
            ]''')
            result3 = serial.deserialize([
                {'name': "Sample", 'author': "Your Name"},
                ["Q", "W", "E", "R", "T", "Y"]
            ])
        except:  # noqa
            self.fail(msg)
        
        def deep_equal(left: object, right: object) -> bool:
            if type(left) != type(right):
                return False
            if left is None:
                return right is None
            if isinstance(left, (int, str, float, bool)):
                return left == right
            if isinstance(left, list):
                if len(left) != len(right):
                    return False
                for a, b in zip(left, right):
                    if not deep_equal(a, b):
                        return False
            else:  # class object
                ks = set(vars(left).keys())
                if ks != set(vars(right).keys()):
                    return False
                for k in ks:
                    lv = getattr(left, k)
                    rv = getattr(right, k)
                    if not deep_equal(lv, rv):
                        return False
            return True
        
        assert deep_equal(result1, result2), msg + " 1<>2"
        assert deep_equal(result1, result3), msg + " 1<>3"
