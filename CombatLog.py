""" Reworked textArea to be a read only combat log from pgu"""
from pgu.gui.const import *  # IGNORE:W0614
from pgu.gui import widget


class CombatLog(widget.Widget):
    """A multi-line text output."""

    def __init__(self, value="", width=120, height=30, size=20, **params):
        params.setdefault("cls", "input")
        params.setdefault("width", width)
        params.setdefault("height", height)

        widget.Widget.__init__(self, **params)
        self.value = value  # The value of the CombatLog
        self.pos = len(str(value))  # The position of the cursor
        self.vscroll = 0  # The number of lines that the TextArea is currently scrolled
        self.font = self.style.font  # The font used for rendering the text
        self.cursor_w = 2  # Cursor width (NOTE: should be in a style)
        w, h = self.font.size("e" * size)
        if not self.style.height:
            self.style.height = h
        if not self.style.width:
            self.style.width = w

    def paint(self, s):
        max_line_w = self.rect.w - 20
        self.doLines(max_line_w)
        cnt = 0
        for line in self.lines:
            line_pos = (0, (cnt - self.vscroll) * self.line_h)
            if (line_pos[1] >= 0) and (line_pos[1] < self.rect.h):
                s.blit(self.font.render(line, 1, self.style.color), line_pos)
            cnt += 1
        self.vpos = cnt

        if self.vscroll < 0:
            self.vscroll = 0
        if self.vpos < self.vscroll:
            self.vscroll = self.vpos
        elif (self.vpos - self.vscroll + 1) * self.line_h > self.rect.h:
            self.vscroll = -(self.rect.h / self.line_h - self.vpos - 1)

    def doLines(self, max_line_w):
        self.line_h = 10
        self.lines = []  # Create an empty starter list to start things out.
        inx = 0
        line_start = 0

        while inx >= 0:
            prev_word_start = inx  # Store the previous whitespace
            spc_inx = self.value.find(" ", inx + 1)
            nl_inx = self.value.find("\n", inx + 1)

            if min(spc_inx, nl_inx) == -1:
                inx = max(spc_inx, nl_inx)
            else:
                inx = min(spc_inx, nl_inx)

            lw, self.line_h = self.font.size(self.value[line_start:inx])

            if lw > max_line_w:
                self.lines.append(self.value[line_start : prev_word_start + 1])
                line_start = prev_word_start + 1

            if inx < 0:
                if line_start < len(self.value):
                    self.lines.append(self.value[line_start : len(self.value)])
                else:
                    self.lines.append("")
            elif self.value[inx] == "\n":
                newline = self.value[line_start : inx + 1]
                newline = newline.replace(
                    "\n", " "
                )  # HACK: We know we have a newline character, which doesn't print nicely, so make it into a space. Comment this out to see what I mean.
                self.lines.append(newline)
                line_start = inx + 1
            else:
                pass

    def _setvalue(self, v):
        self.__dict__["value"] = v
        self.send(CHANGE)

    def event(self, e):
        used = None
        if e.type == FOCUS:
            self.repaint()
        elif e.type == BLUR:
            self.repaint()

        self.pcls = ""
        if self.container.myfocus is self:
            self.pcls = "focus"

        return used

    def __setattr__(self, k, v):
        if k == "value":
            if v == None:
                v = ""
            v = str(v)
            self.pos = len(v)
        _v = self.__dict__.get(k, NOATTR)
        self.__dict__[k] = v
        if k == "value" and _v != NOATTR and _v != v:
            self.send(CHANGE)
            self.repaint()
