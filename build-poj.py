import os
# import fontforge
from fontTools import ufoLib
from fontTools.pens.recordingPen import RecordingPointPen
from fontTools.pens.roundingPen import RoundingPointPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPointPen
from fontTools.misc import transform
from fontTools.ufoLib import glifLib

class GlyphObject:
    def __init__(self, width=None, unicodes=None, anchors=None):
        self.width = width
        self.unicodes = unicodes
        self.anchors = anchors

ITA = 'Italic'
ROM = 'Roman'
INS = 'Instances'
MAS = 'Master'
CAP = 'Caption'
SMT = 'SmText'
TXT = 'Text'
SUB = 'Subhead'
DIS = 'Display'
EL = 'ExtraLight'
LT = 'Light'
RG = 'Regular'
SB = 'Semibold'
BO = 'Bold'
BK = 'Black'
UC = 'UC'
LC = 'LC'
SC = 'SC'

MasterLabelMap = {
    'caption': CAP,
    'text': TXT,
    'display': DIS,
    'master_0': EL,
    'master_1': RG,
    'master_2': BK
}

Sizes = [ CAP , SMT, TXT, SUB, DIS ]
Weights = [ EL , LT, RG, SB, BO, BK ]
Cases = [ UC, LC, SC ]

VLineAnchorPad = 10

OAccentList = [
    '',
    'acute',
    'grave',
    'circumflex',
    'macron',
    'breve',
    'verticalline',
    'caron'
]

AddedGlyphList = [
    ('verticallinecmb', GlyphObject(unicodes=0x030D), 'uni030D'),
    ('verticallinecmb.cap', None, 'uni030D.cap'),
    ('dotabovertcmb', GlyphObject(unicodes=0x0358), 'uni0358'),
    ('dotabovertcmb.cap', None, 'uni0358.cap'),
    ('overticalline', None, 'uni006F030D'),
    ('Overticalline', None, 'uni004F030D'),
    ('Overticalline.sc', None, 'uni004F030D.sc'),
    ('odotabovert', None, 'uni006F0358'),
    ('Odotabovert', None, 'uni004F0358'),
    ('Odotabovert.sc', None, 'uni004F0358.sc'),
    ('Odotabovertacute', None, 'uni00D30358'),
    ('odotabovertacute', None, 'uni00F30358'),
    ('Odotabovertacute.sc', None, 'uni00D30358.sc'),
    ('Odotabovertgrave', None, 'uni00D20358'),
    ('odotabovertgrave', None, 'uni00F20358'),
    ('Odotabovertgrave.sc', None, 'uni00D20358.sc'),
    ('Odotabovertcircumflex', None, 'uni00D40358'),
    ('odotabovertcircumflex', None, 'uni00F40358'),
    ('Odotabovertcircumflex.sc', None, 'uni00D40358.sc'),
    ('Odotabovertmacron', None, 'uni014C0358'),
    ('odotabovertmacron', None, 'uni014D0358'),
    ('Odotabovertmacron.sc', None, 'uni014C0358.sc'),
    ('Odotabovertbreve', None, 'uni014E0358'),
    ('odotabovertbreve', None, 'uni014F0358'),
    ('Odotabovertbreve.sc', None, 'uni014E0358.sc'),
    ('Odotabovertverticalline', None, 'uni004F030D0358'),
    ('odotabovertverticalline', None, 'uni006F030D0358'),
    ('Odotabovertverticalline.sc', None, 'uni004F030D0358.sc'),
    ('Odotabovertcaron', None, 'uni01D10358'),
    ('odotabovertcaron', None, 'uni01D20358'),
    ('Odotabovertcaron.sc', None, 'uni01D10358.sc'),
    ('N.sups.sc', None, 'N.sups.sc'),
]

def buildOList():
    oList = []

    for accent in OAccentList:
        oList.append({
            'UC': (f'O{accent}', f'Odotabovert{accent}'),
            'LC': (f'o{accent}', f'odotabovert{accent}'),
            'SC': (f'O{accent}.sc', f'Odotabovert{accent}.sc'),
        })
    
    return oList

OList = buildOList()

offset = transform.Offset


# /Odotabovertcircumflex/H /odotabovertcircumflex/h /Odotabovertcircumflex.sc/H.sc
# /Odotabovertcircumflex/N.sups /odotabovertcircumflex/n.sups /Odotabovertcircumflex.sc/N.sups.sc

ODotOffsets = {
    ROM: {
        CAP: {
            EL: { UC: (offset(694, -84), 768), LC: (offset(564, -94), 608), SC: (offset(629, -198), 695) },
            LT: { UC: (offset(694, -81), 768), LC: (offset(559, -91), 608), SC: (offset(635, -198), 695) },
            RG: { UC: (offset(688, -78), 768), LC: (offset(570, -88), 640), SC: (offset(636, -184), 708) },
            SB: { UC: (offset(692, -75), 779), LC: (offset(592, -85), 686), SC: (offset(660, -182), 753) },
            BO: { UC: (offset(723, -72), 833), LC: (offset(623, -82), 742), SC: (offset(676, -180), 760) },
            BK: { UC: (offset(736, -70), 828), LC: (offset(650, -80), 768), SC: (offset(726, -180), 811) },
        },
        SMT: {
            EL: { UC: (offset(682, -84), 727), LC: (offset(522, -94), 561), SC: (offset(607, -198), 671) },
            LT: { UC: (offset(668, -81), 744), LC: (offset(537, -91), 597), SC: (offset(620, -198), 681) },
            RG: { UC: (offset(670, -78), 750), LC: (offset(560, -88), 628), SC: (offset(636, -184), 708) },
            SB: { UC: (offset(692, -75), 779), LC: (offset(592, -85), 686), SC: (offset(660, -182), 753) },
            BO: { UC: (offset(705, -72), 795), LC: (offset(599, -82), 716), SC: (offset(664, -180), 760) },
            BK: { UC: (offset(702, -70), 802), LC: (offset(614, -80), 734), SC: (offset(684, -180), 811) },
        },
        TXT: {
            EL: { UC: (offset(660, -84), 706), LC: (offset(506, -94), 538), SC: (offset(613, -198), 659) },
            LT: { UC: (offset(662, -81), 720), LC: (offset(524, -91), 578), SC: (offset(624, -198), 659) },
            RG: { UC: (offset(664, -78), 732), LC: (offset(540, -88), 618), SC: (offset(636, -184), 708) },
            SB: { UC: (offset(664, -75), 742), LC: (offset(560, -85), 630), SC: (offset(636, -182), 712) },
            BO: { UC: (offset(666, -72), 752), LC: (offset(570, -82), 650), SC: (offset(636, -180), 718) },
            BK: { UC: (offset(666, -70), 758), LC: (offset(588, -80), 700), SC: (offset(636, -180), 728) },
        },
        SUB: {
            EL: { UC: (offset(620, -84), 689), LC: (offset(482, -94), 521), SC: (offset(573, -198), 640) },
            LT: { UC: (offset(622, -81), 688), LC: (offset(524, -91), 578), SC: (offset(580, -198), 640) },
            RG: { UC: (offset(640, -78), 718), LC: (offset(540, -88), 618), SC: (offset(602, -184), 692) },
            SB: { UC: (offset(644, -75), 724), LC: (offset(546, -85), 630), SC: (offset(606, -182), 702) },
            BO: { UC: (offset(652, -72), 740), LC: (offset(564, -82), 650), SC: (offset(620, -180), 714) },
            BK: { UC: (offset(666, -70), 758), LC: (offset(582, -80), 684), SC: (offset(636, -180), 728) },
        },
        DIS: {
            EL: { UC: (offset(584, -84), 648), LC: (offset(472, -94), 512), SC: (offset(549, -198), 597) },
            LT: { UC: (offset(586, -81), 645), LC: (offset(478, -91), 534), SC: (offset(549, -198), 597) },
            RG: { UC: (offset(590, -78), 650), LC: (offset(514, -88), 578), SC: (offset(552, -184), 604) },
            SB: { UC: (offset(606, -75), 682), LC: (offset(532, -85), 622), SC: (offset(572, -182), 636) },
            BO: { UC: (offset(624, -72), 708), LC: (offset(534, -82), 628), SC: (offset(594, -180), 682) },
            BK: { UC: (offset(632, -70), 720), LC: (offset(556, -80), 656), SC: (offset(594, -180), 692) },
        }
    },

    # /Odotabovertcircumflex/h /Odotabovertcircumflex/question /odotabovertcircumflex/n.sups /odotabovertcircumflex/question /Overticalline/overticalline
    ITA: {
        CAP: {
            EL: { UC: (offset(588, -84), 680), LC: (offset(472, -180), 536) },
            LT: { UC: (offset(582, -81), 683), LC: (offset(487, -177), 547) },
            RG: { UC: (offset(608, -78), 688), LC: (offset(518, -171), 586) },
            SB: { UC: (offset(636, -75), 761), LC: (offset(566, -167), 684) },
            BO: { UC: (offset(658, -72), 797), LC: (offset(595, -163), 742) },
            BK: { UC: (offset(676, -70), 828), LC: (offset(628, -160), 768) },
        },
        SMT: {
            EL: { UC: (offset(554, -84), 663), LC: (offset(451, -180), 531) },
            LT: { UC: (offset(572, -81), 665), LC: (offset(474, -177), 583) },
            RG: { UC: (offset(605, -78), 726), LC: (offset(500, -171), 597) },
            SB: { UC: (offset(613, -75), 740), LC: (offset(532, -167), 647) },
            BO: { UC: (offset(633, -72), 765), LC: (offset(560, -163), 692) },
            BK: { UC: (offset(651, -70), 795), LC: (offset(600, -160), 734) },
        },
        TXT: {
            EL: { UC: (offset(547, -84), 702), LC: (offset(439, -180), 520) },
            LT: { UC: (offset(562, -81), 656), LC: (offset(452, -177), 538) },
            RG: { UC: (offset(562, -78), 704), LC: (offset(458, -171), 553) },
            SB: { UC: (offset(569, -75), 707), LC: (offset(492, -167), 574) },
            BO: { UC: (offset(582, -72), 721), LC: (offset(498, -163), 610) },
            BK: { UC: (offset(610, -70), 744), LC: (offset(566, -160), 717) },
        },
        SUB: {
            EL: { UC: (offset(545, -84), 669), LC: (offset(440, -180), 531) },
            LT: { UC: (offset(551, -81), 688), LC: (offset(452, -177), 551) },
            RG: { UC: (offset(551, -78), 688), LC: (offset(466, -171), 576) },
            SB: { UC: (offset(569, -75), 703), LC: (offset(492, -167), 608) },
            BO: { UC: (offset(583, -72), 713), LC: (offset(510, -163), 626) },
            BK: { UC: (offset(597, -70), 728), LC: (offset(534, -160), 666) },
        },
        DIS: {
            EL: { UC: (offset(521, -84), 636), LC: (offset(419, -180), 491) },
            LT: { UC: (offset(531, -81), 653), LC: (offset(434, -177), 534) },
            RG: { UC: (offset(541, -78), 670), LC: (offset(434, -171), 530) },
            SB: { UC: (offset(551, -75), 687), LC: (offset(463, -167), 598) },
            BO: { UC: (offset(561, -72), 703), LC: (offset(482, -163), 612) },
            BK: { UC: (offset(572, -70), 720), LC: (offset(493, -160), 632) },
        }
    }
}

class POJBuilder:
    def __init__(self, slant, size, weight, master=False):
        self.weightKey = weight
        self.master = master

        if slant == ITA:
            if weight == RG:
                weight = 'It'
            else:
                weight = f'{weight}It'

        self.slant = slant
        self.size = size
        self.weight = weight

        if self.master:
            x = '' if size == 'text' else size[0]
            y = weight[-1]
            self.ufoFile = f'{slant}/Masters/{size}/{weight}/SourceSerif_{x}{y}.ufo'
        else:
            self.ufoFile = f'{slant}/Instances/{size}/{weight}/font.ufo'
        self.ufo = ufoLib.UFOWriter(self.ufoFile)
        self.glyphSet = self.ufo.getGlyphSet()

    def build(self):
        self.addGlyphs()
        self.build_verticalline()
        self.build_dotabovert()
        self.build_overticalline()
        self.build_odots()
        if self.slant == ROM:
            self.build_N_sups_sc()
        self.save_lib_plist()
    
    def save_lib_plist(self):
        lib_plist = self.ufo.readLib()
        for g in AddedGlyphList:
            if g[0] not in lib_plist['public.glyphOrder']:
                lib_plist['public.glyphOrder'].append(g[0])
            if g[0] not in lib_plist['public.postscriptNames']:
                lib_plist['public.postscriptNames'][g[0]] = g[2]
        self.ufo.writeLib(lib_plist)

    def addGlyphs(self):
        for g in AddedGlyphList:
            if self.slant == ITA and g[0].endswith('.sc'):
                continue
            self.glyphSet.writeGlyph(g[0], g[1])
        self.glyphSet.writeContents()

    def getTransformDraw(self, src, transformation, glyphObject=None):
        def transformDraw(pointPen):
            roundingPen = RoundingPointPen(pointPen)
            transformPen = TransformPointPen(roundingPen, transformation)
            self.glyphSet.readGlyph(src, glyphObject, transformPen)
        return transformDraw

    def getBounds(self, glyph):
        bPen = BoundsPen(self.glyphSet)
        bPen.addComponent(glyph, transform.Identity)
        return bPen.bounds

    def getxOffset(self, glyph):
        x1, _, x2, _ = self.getBounds(glyph)
        return round((x2 - x1) / 2 + x1)
    
    def xMax(self, glyph):
        _, _, x, _ = self.getBounds(glyph)
        return x

    def yMax(self, glyph):
        _, _, _, y = self.getBounds(glyph)
        return y

    def getVlineOffsetItalic(self, refGlyph, vlineGlyph):
        obj = self.getGlyphObj(refGlyph)
        x_1 = obj.anchors[0]['x']
        y_1 = obj.anchors[0]['y']
        x_2 = obj.anchors[1]['x']
        y_2 = obj.anchors[1]['y']
        m = (y_2 - y_1) / (x_2 - x_1)
        _, y_low, _, _ = self.getBounds(refGlyph)        
        xCenter = (y_low - y_1) / m + x_1
        pen = RecordingPointPen()
        self.glyphSet.readGlyph(vlineGlyph, None, pen)
        x_3 = pen.value[1][1][0][0]
        x_4 = pen.value[2][1][0][0]
        y_3 = pen.value[1][1][0][1]
        dx = - (x_3 + x_4/2 - x_3/2 - xCenter)
        dy = y_low - y_3
        return offset(dx, dy)

    def getVlineOffset(self):
        if self.slant == ITA:
            return self.getVlineOffsetItalic('caroncmb', 'verticallinemod')

        x1, y1, x2, _ = self.getBounds('verticallinemod')
        dx = -round((x2 - x1) / 2 + x1)
        _, y2, _, _ = self.getBounds('caroncmb')
        dy = y2 - y1
        return offset(dx, dy)
    
    def getVlineCapOffset(self):
        if self.slant == ITA:
            return self.getVlineOffsetItalic('caroncmb.cap', 'verticallinecmb.cap')

        _, y1, _, _ = self.getBounds('verticallinecmb.cap')
        _, y2, _, _ = self.getBounds('caroncmb.cap')
        return offset(0, y2 - y1)
    
    def getGlyphObj(self, glyph):
        obj = GlyphObject()
        self.glyphSet.readGlyph(glyph, obj)
        return obj

    def updateGlyph(self, glyph, glyphObject):
        self.glyphSet.writeGlyph(glyph, glyphObject, self.glyphSet[glyph].drawPoints)

    def copyAnchorsPadYTop(self, src, dst, vpad=VLineAnchorPad):
        srcObj = GlyphObject()
        dstObj = GlyphObject()

        self.glyphSet.readGlyph(src, srcObj)
        self.glyphSet.readGlyph(dst, dstObj)

        dstObj.anchors = srcObj.anchors

        ymax = self.yMax(dst)
        if dstObj.anchors[1]['y'] < ymax + vpad:
            dstObj.anchors[1]['y'] = ymax + vpad
        self.updateGlyph(dst, dstObj)

    def build_verticalline(self):
        vline = self.getGlyphObj('verticallinecmb')
        vlineCap = self.getGlyphObj('verticallinecmb.cap')

        tDraw = self.getTransformDraw('verticallinemod', self.getVlineOffset())
        self.glyphSet.writeGlyph('verticallinecmb', vline, tDraw)

        tDraw = self.getTransformDraw('verticallinecmb', transform.Scale(1, 0.8))
        self.glyphSet.writeGlyph('verticallinecmb.cap', vlineCap, tDraw)

        tDraw = self.getTransformDraw('verticallinecmb.cap', self.getVlineCapOffset())
        self.glyphSet.writeGlyph('verticallinecmb.cap', vlineCap, tDraw)

        self.copyAnchorsPadYTop('caroncmb', 'verticallinecmb')
        self.copyAnchorsPadYTop('caroncmb.cap', 'verticallinecmb.cap')

    def copyReference(self, src, dst):
        dstObj = self.getGlyphObj(dst)
        pen = RecordingPointPen()
        pen.addComponent(src, transform.Identity)
        self.glyphSet.writeGlyph(dst, dstObj, pen.replay)

    def build_dotabovert(self):
        self.copyReference('dotaccentcmb', 'dotabovertcmb')
        self.copyReference('dotaccentcmb.cap', 'dotabovertcmb.cap')

    def getAccentTransform(self, src, accent):
        pen = RecordingPointPen()
        self.glyphSet.readGlyph(src, None, pen)
        transformation = next(x for x in pen.value if x[1][0] == accent)[1][1]
        return transformation
    
    def getGlyphWidth(self, glyphname):
        obj = self.getGlyphObj(glyphname)
        return obj.width

    def buildAccentGlyph(self, dst, base, mark, width, accentTransform):
        dstObj = self.getGlyphObj(dst)
        dstObj.width = width
        dstPen = RecordingPointPen()
        dstPen.addComponent(base, transform.Identity)
        dstPen.addComponent(mark, accentTransform)
        self.glyphSet.writeGlyph(dst, dstObj, dstPen.replay)

    def buildAccentedGlyphFromRef(self, dst, base, mark, ref, refMark):
        self.buildAccentGlyph(dst, base, mark, self.getGlyphWidth(ref), self.getAccentTransform(ref, refMark))

    def build_overticalline(self):
        self.buildAccentedGlyphFromRef('overticalline', 'o', 'verticallinecmb', 'ocaron', 'caroncmb')
        self.buildAccentedGlyphFromRef('Overticalline', 'O', 'verticallinecmb.cap', 'Ocaron', 'caroncmb.cap')
        if self.slant == ROM:
            self.buildAccentedGlyphFromRef('Overticalline.sc', 'O.sc', 'verticallinecmb.cap', 'Ocaron.sc', 'caroncmb.cap')

    def setWidth(self, glyph, width):
        glyphObj = self.getGlyphObj(glyph)
        glyphObj.width = width
        self.updateGlyph(glyph, glyphObj)

    def build_odots(self):
        slant = self.slant
        size = self.size
        wt = self.weightKey

        if self.master:
            size = MasterLabelMap[size]
            wt = MasterLabelMap[wt]

        for oset in OList:
            for case in Cases:
                if self.slant == ITA and case == SC:
                    continue

                transform, width = ODotOffsets[slant][size][wt][case]
                src = oset[case][0]
                dst = oset[case][1]
                mark = 'dotabovertcmb' if case == LC else 'dotabovertcmb.cap'
                self.buildAccentGlyph(dst, src, mark, 0, transform)
                if width is not None:
                    self.setWidth(dst, width)
                else:
                    self.setWidth(dst, self.getGlyphWidth(src))

    def copyOutline(self, src, dst):
        srcObj = self.getGlyphObj(src)
        dstObj = self.getGlyphObj(dst)
        dstObj.width = srcObj.width
        self.glyphSet.writeGlyph(dst, dstObj, self.glyphSet[src].drawPoints)

    def getVMap(self, font, scale):
        vals = font.private['OtherBlues'] + font.private['BlueValues']
        valIter = iter(vals)
        vMap = []
        for beg, end in zip(valIter, valIter):
            if beg < 0:
                tmp = beg
                beg = end
                end = tmp
            vMap.append((int(beg), int(end - beg), round(beg * scale)))
        return vMap

    # This method should be deleted if fontforge gets fixed...
    def tmp_N_sups_sc_copy(self):
        size = self.size
        weight = self.weight

        if self.master:
            size = size.capitalize()
            if weight == 'master_0':
                weight = 'ExtraLight'
            elif weight == 'master_1':
                weight = 'Regular'
            elif weight == 'master_2':
                weight = 'Black'

        if size == 'Text':
            size = ''
        filename = f'N.sups_SourceSerif4{size}-{weight}.glif'
        path = os.path.join(self.ufoFile, '../../../../../N.sups.sc', filename)
        data = ''
        with open(path) as f:
            data = f.read()
        pen = RecordingPointPen()
        srcObj = GlyphObject()
        glifLib.readGlyphFromString(data, srcObj, pen)
        dstObj = self.getGlyphObj('N.sups.sc')
        dstObj.width = srcObj.width
        self.glyphSet.writeGlyph('N.sups.sc', dstObj, pen.replay)

    def build_N_sups_sc(self):
        self.tmp_N_sups_sc_copy()
        # self.copyOutline('N.sups', 'N.sups.sc')
        
        # Fontforge is currently broken, so we can't use the automated
        # glyph change function. For now .glif files must be manually copied

        # font = fontforge.open(self.ufoFile)
        # vMap = self.getVMap(font, 0.82)
        # N_sups_sc = font['N.sups.sc'].genericGlyphChange(
        #     stemScale=1,
        #     hCounterScale=0.82,
        #     vMapping=vMap
        #     )
        # N_sups_sc_glif = os.path.join(self.ufoFile, 'glyphs', self.glyphSet.contents['N.sups.sc'])        
        # N_sups_sc.export(N_sups_sc_glif)

def buildInstances():
    for size in Sizes:
        for weight in Weights:
            builder = POJBuilder(ROM, size, weight)
            builder.build()

    for size in Sizes:
        for weight in Weights:
            builder = POJBuilder(ITA, size, weight)
            builder.build()

def buildMasters():
    for size in [ 'caption', 'text', 'display' ]:
        for weight in [ 'master_0', 'master_1', 'master_2' ]:
            builder = POJBuilder(ROM, size, weight, master=True)
            builder.build()

buildInstances()
buildMasters()
