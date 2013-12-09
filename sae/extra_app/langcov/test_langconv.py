#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from langconv import *

class ConvertMapTest(TestCase):
    def test_map(self):
        mapping = {'a': 'b', 'b': 'a', 'abc': 'cba', 'cb': 'bb'}
        cm = ConvertMap('test', mapping)
        self.assertEqual(len(cm), 6) # with switch node: 'ab' and 'c'
        self.failUnless('a' in cm)
        self.failUnless('c' in cm)
        self.failIf('bc' in cm)
        self.assertEqual(cm['a'].data, (True, True, 'b'))
        self.assertEqual(cm['b'].data, (True, False, 'a'))
        self.assertEqual(cm['c'].data, (False, True, ''))
        self.assertEqual(cm['ab'].data, (False, True, ''))
        self.assertEqual(cm['abc'].data, (True, False, 'cba'))
        self.assertEqual(cm['cb'].data, (True, False, 'bb'))

class ConverterModelTest(TestCase):
    def test_1(self):
        registery('rev', {u'a': u'c', u'c': u'a'})
        c = Converter('rev')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'c')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'cb')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'cba')

    def test_2(self):
        registery('2', {u'b': u'a', u'ab': u'ab'})
        c = Converter('2')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'ab')

    def test_3(self):
        registery('3', {u'a': u'b', u'ab': u'ba'})
        c = Converter('3')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'ba')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'ba')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'babc')

    def test_4(self):
        registery('4', {u'ab': u'ba'})
        c = Converter('4')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'ba')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'ba')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'baac')

    def test_5(self):
        registery('5', {u'ab': u'ba'})
        c = Converter('5')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'aba')

    def test_6(self):
        registery('6', {u'abc': u'cba'})
        c = Converter('6')
        c.feed(u'a')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'a')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'cbaabb')

    def test_7(self):
        registery('7', {u'abc': u'cba', u'bc': 'cb'})
        c = Converter('7')
        c.feed(u'a')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'')
        self.assertEqual(c.get_result(), u'cbaa')

    def test_8(self):
        registery('8', {u'abc': u'cba', u'ab': 'ba'})
        c = Converter('8')
        c.feed(u'a')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'cba')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'cbabab')

    def test_9(self):
        registery('9', {u'bx': u'dx', u'c': u'e', u'cy': u'cy'})
        c = Converter('9')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'a')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'a')
        c.feed(u'c')
        self.assertEqual(c.get_result(), u'a')
        c.end()
        self.assertEqual(c.get_result(), u'abe')

    def test_10(self):
        registery('10', {u'a': u'd', u'b': u'e', u'ab': u'cd', u'by': u'yy'})
        c = Converter('10')
        c.feed(u'a')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'b')
        self.assertEqual(c.get_result(), u'')
        c.feed(u'c')
        c.end()
        self.assertEqual(c.get_result(), u'cdc')

class ConverterTest(TestCase):
    def assertConvert(self, name, string, converted):
        c = Converter(name)
        new = c.convert(string)
        assert new == converted, (
                "convert(%s, '%s') should return '%s' but '%s'" % (
                    repr(name), string, converted, new)).encode('utf8')

    def assertST(self, trad, simp):
        self.assertConvert('zh-hans', trad, simp)
        self.assertConvert('zh-hant', simp, trad)

    def test_zh1(self):
        self.assertST(u'乾燥', u'干燥')
        self.assertST(u'乾坤', u'乾坤')
        self.assertST(u'乾隆', u'乾隆')
        self.assertST(u'幹事', u'干事')
        self.assertST(u'牛肉乾', u'牛肉干')
        self.assertST(u'相干', u'相干')

    def test_zh2(self):
        self.assertST(u'印表機', u'打印机')
        self.assertST(u'說明檔案', u'帮助文件')

    def test_zh3(self):
        self.assertST(u'頭髮', u'头发')
        self.assertST(u'頭髮和', u'头发和')
        self.assertST(u'發生', u'发生')
        self.assertST(u'頭髮和發生', u'头发和发生')

    def test_zh4(self):
        self.assertST(u'著名', u'著名')
        self.assertST(u'覆蓋', u'覆盖')
        self.assertST(u'翻來覆去', u'翻来覆去')
        self.assertST(u'獃獃', u'呆呆')
        self.assertST(u'獃住', u'呆住')
        self.assertST(u'壁畫', u'壁画')
        self.assertST(u'畫面', u'画面')
        self.assertST(u'顯著', u'显著')
        self.assertST(u'土著人', u'土著人')
        self.assertST(u'長春鹼', u'长春碱')
        self.assertST(u'嘌呤鹼', u'嘌呤碱')
        self.assertST(u'嘧啶鹼', u'嘧啶碱')

if '__main__' == __name__:
    import unittest
    unittest.main()

