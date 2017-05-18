import os
import re
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes, register_local_role

# menusel role

_amp_re = re.compile(r'(?<!&)&(?![&\s])')

def menusel_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    if True or typ == 'menuselection':
        text = text.replace('-->', u'\u2023')
    spans = _amp_re.split(text)

    node = nodes.emphasis(rawtext=rawtext)
    for i, span in enumerate(spans):
        span = span.replace('&&', '&')
        if i == 0:
            if len(span) > 0:
                textnode = nodes.Text(span)
                node += textnode
            continue
        accel_node = nodes.inline()
        letter_node = nodes.Text(span[0])
        accel_node += letter_node
        accel_node['classes'].append('accelerator')
        node += accel_node
        textnode = nodes.Text(span[1:])
        node += textnode

    node['classes'].append(typ)
    return [node], []

register_local_role('menusel', menusel_role)

# samp role

_litvar_re = re.compile('{([^}]+)}')

def emph_literal_role(typ, rawtext, text, lineno, inliner,
                      options={}, content=[]):
    """replacement for sphinx's ``:samp:`` role handler.
    this is a bit stricter in it's parsing, and allows escaping of literal
    ``{`` and ``}`` characters.
    """
    def make_error(pos, value):
        value = "%s at char %d of %s" % (value, pos, rawtext)
        msg = inliner.reporter.error(value, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    text = utils.unescape(text)
    retnode = nodes.compound(role=typ.lower(), classes=[typ])
#    retnode = nodes.literal(role=typ.lower(), classes=[typ])
    buffer = u"" # contains text being accumulated for next node
    in_escape = False # True if next char is part of escape sequence
    in_var = False # True if parsing variable section instead of plain text
    var_start = None # marks start of var section if in_var is True
    i = 0
    for c in text:
        i += 1
        if in_escape:
            # parse escape sequence
            if c in ru("{}\\"):
                buffer += c
                in_escape = False
            else:
                return make_error(i-2, "unknown samp-escape '\\\\%s'" % (c,))
        elif c == r"\\":
            # begin escape sequence
            in_escape = True
            i += 1 # account for extra escape char in rawtext
        elif in_var:
            # parsing variable section
            if c == u"{":
                return make_error(i, "unescaped '{'")
            elif c == u"}":
                # finalize variable section, return to plaintext
                if not buffer:
                    return make_error(i-1, "empty variable section")
#                retnode += nodes.emphasis(buffer, buffer)
                retnode += nodes.emphasis(buffer, "<%s>"%buffer, classes=['emphasis'])
                buffer = u""
                in_var = False
            else:
                buffer += c
        else:
            # parsing plaintext section
            if c == u"{":
                # finalize plaintext section, start variable section
                if buffer:
                    retnode += nodes.literal(buffer, buffer)
                buffer = u""
                in_var = True
                var_start = i
            elif c == u"}":
                return make_error(i, "unescaped '}'")
            else:
                buffer += c
    if in_escape:
        return make_error(i, "unterminated samp-escape sequence")
    elif in_var:
        return make_error(var_start, "unterminated variable section")
    elif buffer:
        retnode += nodes.literal(buffer, buffer)
    return [retnode], []

register_local_role('samp', emph_literal_role)

class AnswerDirective(rst.Directive):
    """ Directive to insert conditional content """
    has_content = True
    option_spec = {
        'force'  : directives.unchanged,
        'height' : directives.unchanged,
        'text'   : directives.unchanged,
        'points' : directives.unchanged,
        'class'  : directives.class_option,
    }

    def run(self):
        ans_class = 'answer'

        # ANSWER MODE
        if 'ANS' in os.environ or self.options.get('force', None):
            set_classes(self.options)
            self.assert_has_content()
            container = nodes.Element()
            self.add_name(container)
            self.state.nested_parse( self.content, self.content_offset, container)
            childs = [] + container.children
            for node in childs:
                try:
                    node['classes'].append(ans_class)
                except TypeError:
                    pass
                childs.extend(node.children)
            score = nodes.line(text="Max points: %s"%self.options.get('points', 1))
            return [nodes.line(), score, nodes.line()] + container.children
        # EMPTY ANSWER
        ns = [nodes.line(), nodes.line(text=self.options.get('text', 'Solution:'))]
        ns.extend(nodes.paragraph() for x in xrange( int(self.options.get('height', 20)) ))
        return ns

class ChoiceDirective(rst.Directive):
    has_content = True
    option_spec = {
        'force'   : directives.unchanged,
        'correct' : directives.unchanged,
        'class'   : directives.class_option,
    }
    def run(self):

        self.assert_has_content()
        set_classes(self.options)

        container = nodes.Element()
        self.add_name(container)
        self.state.nested_parse( self.content, self.content_offset, container)

        # ANSWER MODE
        if 'ANS' in os.environ or self.options.get('force', None):
            if 'correct' in self.options:
                pfx = nodes.line(text=u'\u00A0\u25A3\u00A0\u00A0')
            else:
                pfx = nodes.line(text=u'\u00A0\u25A2\u00A0\u00A0')
        else:
            # EMPTY ANSWER
            pfx = nodes.line(text=u'\u00A0\u25A2\u00A0\u00A0')
        container.children[0].insert(0,  pfx)
        return container.children

directives.register_directive('answer', AnswerDirective)
directives.register_directive('choice', ChoiceDirective)

