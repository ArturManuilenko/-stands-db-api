from reportlab.platypus.flowables import Flowable

class vtext(Flowable):
    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text.split('\n')

    def draw(self):
        canvas = self.canv
        canvas.rotate(90)
        fs = canvas._fontsize
        canvas.translate(1, -fs/1.2)  # canvas._leading?
        #canvas.drawString(0, 0, self.text)
        textobject = canvas.beginText()
        #textobject.setTextOrigin(inch, 2.5*inch)
        #textobject.setFont("Helvetica-Oblique", 14)
        #textobject.setFillGray(0.4)
        for txt in self.text:
            textobject.textLine(txt)
        canvas.drawText(textobject)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        ah = 0;
        for l in self.text:
            w = canv.stringWidth(l, fn, fs)
            if w > ah: ah = w
        return canv._leading * len(self.text), 1 + ah