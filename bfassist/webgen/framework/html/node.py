#############################################################################
#
#
#   HTML Node webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML node module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        css <- (html.)node

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from typing import Union

from bfassist.webgen.framework.css import CSS_Style


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class HTML_Node:
    """ Representation of a classic HTML tag-pair including its innerHTML.

        :param nodeType:    Type of the node.
        :param properties:  Properties as a dictionary if given.
        :param innerHTML:   Content as tuple if any.

        // The following parameters are all redundant contents of the properties dictionary.
        // They are just here for easier modification.

        :param Id:         Identifier if any.
        :param Class:      Classifier if any.

            note::  Author(s): Mitch """

    def __init__(self, nodeType: str, properties: dict = None, innerHTML: Union[tuple, str] = (), Id: str = None,
                 Class: str = None):
        self.nodeType = nodeType

        if properties is None:
            self.properties = {}
        else:
            self.properties = properties

        if innerHTML == ():
            self.innerHTML = innerHTML
        elif self.isValidInnerHTML(innerHTML):
            self.innerHTML = innerHTML
        else:
            raise TypeError("All elements of parameter innerHTML have to be nodes or text!")

        self.Id = Id
        self.Class = Class

    def __getattr__(self, item: str):
        """ This way we will make child nodes available via their node type.

            :param item:    A potential child node type.

            :return:        Always the last child node of given type.

                note::  Author(s): Mitch """

        if item == "_innerHTML":  # This is a call from a contentless node
            return ()

        if self.nodeTypeInChildren(item):
            for node in reversed(self.innerHTML):
                if isinstance(node, HTML_Node) and node.nodeType == item:
                    return node
        else:
            raise AttributeError("No such attribute or child node. " + item + " " + str(self.innerHTML))

    def __iadd__(self, other):
        """ Makes appendages available via the plus-equals-operator.

            :param other:   A single HTML node or a tuple of HTML nodes to be added as children.

            :return:        Returns itself at the end.

                note::  Author(s): Mitch """

        if isinstance(other, HTML_Node):
            self.appendChildNode(other)
        elif isinstance(other, tuple) and self.allNodesAreNodes(other):
            self.appendChildrenNodes(other)
        return self

    def __getitem__(self, item):
        """ Magic function that gives more direct access to properties of this node.

            :param item:    A potential property of this node to get its value.

            :return:        The value of the property if it exists.

                note::  Author(s): Mitch """

        return self.properties[item]

    def __setitem__(self, key, value):
        """ Magic function that gives more direct access to properties of this node.

            :param key:     The property name.
            :param value:   The value to set for this property.

                note::  Author(s): Mitch """

        self.properties[key] = value

    def nodeTypeInChildren(self, nodeType: str):
        """ Simple helper function to determine, if a node type is contained in this node's inner HTML.

            :param nodeType:    The node type to look for.

            :return:            True if it is contained, otherwise False.

                note::  Author(s): Mitch """

        return any([True if isinstance(node, HTML_Node) and node.nodeType == nodeType
                    else False
                    for node in self.innerHTML])

    def getChildrenOfType(self, nodeType: str):
        """ Simple helper function to fetch all Children of a node type.

            :param nodeType:    The node type to fetch.

            :return:            A tuple containing the children.

                note::  Author(s): Mitch """

        nodes = ()
        for node in self.innerHTML:
            if isinstance(node, HTML_Node) and node.nodeType == nodeType:
                nodes += (node, )
        return nodes

    @staticmethod
    def nodeIdInNodes(nodeId: str, nodes: tuple):
        """ Simple helper function to determine, if a node in nodes has nodeId as id.

            :param nodeId:  The Id to look for.
            :param nodes:   The tuple of nodes to inspect.

                note::  Author(s): Mitch """

        return any([True if isinstance(node, HTML_Node) and node.Id == nodeId else False for node in nodes])

    @staticmethod
    def allNodesAreContentless(nodes: tuple):
        """ Simple helper function to determine, if all nodes in a tuple are contentless.

            :param nodes:   A tuple of nodes.

            :return:        True if all nodes are contentless, otherwise False.

                note::  Author(s): Mitch """

        return all([True if isinstance(node, HTML_Node_Contentless) else False for node in nodes])

    @staticmethod
    def allNodesAreNodes(nodes: tuple):
        """ Simple helper function to determine, if all nodes in a tuple are actually nodes.

            :param nodes:   A tuple of nodes.

            :return:        True if all objects in nodes are actually nodes.

                note::  Author(s): Mitch """

        return all([True if isinstance(node, HTML_Node) else False for node in nodes])

    @staticmethod
    def isValidInnerHTML(innerHTML: tuple):
        """ Simple helper function to determine, if an inner HTML is valid inner HTML.

            :param innerHTML:   A tuple of inner HTML.

            :return:            True if the inner HTML is valid, otherwise False.

                note::  Author(s): Mitch """

        return all([True if
                    (isinstance(node, HTML_Node) or isinstance(node, HTML_Node_Contentless) or isinstance(node, str))
                    else False
                    for node in innerHTML])

    @property
    def innerHTML(self):
        """ Gets the inner HTML of this node.

            :return:    Inner HTML.

                note::  Author(s): Mitch """
        return self._innerHTML

    @innerHTML.setter
    def innerHTML(self, innerHTML: str):
        """ Sets the inner HTML of this node.

            :param innerHTML:   Inner HTML to be set as string or node.

                note::  Author(s): Mitch """

        if isinstance(innerHTML, str):
            self._innerHTML = (innerHTML,)
        elif isinstance(innerHTML, tuple):
            self._innerHTML = innerHTML

    @innerHTML.deleter
    def innerHTML(self):
        """ Deletes the inner HTML of this node.

            :param innerHTML:   Inner HTML to be deleted.

                note::  Author(s): Mitch """

        del self._innerHTML

    @property
    def Id(self):
        """ Gets the id of this node.

            :return: Node id.

                note::  Author(s): Mitch """
        return self._Id

    @Id.setter
    def Id(self, Id: str):
        """ Sets the id of this node.

            :param Id: Id to be set.

                note::  Author(s): Mitch """
        self._Id = Id
        self.properties['id'] = Id

    @property
    def Class(self):
        """ Gets the class of this node.

            :return: Node class.

                note::  Author(s): Mitch """
        return self._Class

    @Class.setter
    def Class(self, Class: str):
        """ Sets the class of this node.

            :param Class:   Class to be set.

                note::  Author(s): Mitch """
        self._Class = Class
        self.properties['class'] = Class

    def appendChildNode(self, child: HTML_Node):
        """ Appends a new node as child.

            :param child:   The child node to be appended.

            :return:        Returns self after appendix.

                note::  Author(s): Mitch """
        self.innerHTML += (child,)
        return self

    def appendChildrenNodes(self, children: tuple):
        """ Appends a list of nodes as children.

            :param children:    The children to be appended.

                note::  Author(s): Mitch """
        for child in children:
            self.appendChildNode(child)

    def addProperty(self, key: str, value: str):
        """ Add a property to the properties dictionary.

            :param key:     The property key.
            :param value:   The property value.

                note::  Author(s): Mitch """
        self.properties[key] = value

    def propertiesToString(self):
        """ Builds the property string as it will be used in HTML to define this node's properties.

            :return:    Properties as string.

                note::  Author(s): Mitch """

        properties = ""
        for prop in self.properties:
            if isinstance(prop, str) and (self.properties[prop] != "" or prop == 'onclick' or prop == 'disabled') \
                    and self.properties[prop] is not None:
                properties += " " + prop + "=\"" + self.properties[prop] + "\""
        return properties

    def openTagToString(self):
        """ Builds the HTML opening tag for this node.

            :return:    Opening tag as string.

                note::  Author(s): Mitch """

        return "<" + self.nodeType + self.propertiesToString() + ">\n"

    def innerHTMLtoString(self):
        """ Builds the HTML for the inner HTML of this node.

            :return:    Inner HTML as string.

                note::  Author(s): Mitch """

        content = ""
        for node in self.innerHTML:
            if isinstance(node, str):
                content += "\t" + node + "\n"
            elif isinstance(node, HTML_Node_Contentless):
                content += "\t" + node.toString()
            else:
                content += "\t" + node.toString().replace('\n', '\n\t')[:-1]
        return content.replace("\n", "\n")

    def endTagToString(self):
        """ Builds the HTML closing tag for this node.

            :return:    Closing tag as string.

                note::  Author(s): Mitch """

        return "</" + self.nodeType + ">\n"

    def toString(self):
        """ Converts this HTML node to a string.

            :return:    Node as string.

                note::  Author(s): Mitch """

        return self.openTagToString() + self.innerHTMLtoString() + self.endTagToString()

    def styleThisType(self, rules: set):
        """ Creates a CSS Style for all nodes of this type.

            :param rules:   The CSS rules to apply.

            :return:        The finished CSS Style instance.

                note::  Author(s): Mitch """
        return CSS_Style(self.nodeType, rules)

    def styleThisClass(self, rules: set):
        """ Creates a CSS Style for all nodes of this type and class.

            :param rules:   The CSS rules to apply.

            :return:        The finished CSS Style instance.

                note::  Author(s): Mitch """

        if self.Class is not None:
            return CSS_Style(self.nodeType + "." + self.Class, rules)
        else:
            raise ValueError("This node doesn't have any class value assigned.")

    def styleThisNode(self, rules: set):
        """ Creates a CSS Style for this particular node.

                :param rules:   The CSS rules to apply.

                :return:        The finished CSS Style instance.

                    note::  Author(s): Mitch """

        if self.Id is not None:
            return CSS_Style(self.nodeType + "#" + self.Id, rules)
        else:
            raise ValueError("This node doesn't have an identifier assigned.")

    def styleThisNodesSubType(self, subtype: str, rules: set):
        """ Creates a CSS style for a subtype of this particular node.

            :param subtype: Subtype the CSS rules should apply to.
            :param rules:   The CSS rules to apply.

            :return:        The finished CSS style instance.

                note::  Author(s): Mitch """

        if self.Id is None:
            raise ValueError("This node doesn't have an identifier assigned.")
        else:
            if not self.nodeTypeInChildren(subtype):
                raise ValueError("The specified subtype does not exist.")
            else:
                return CSS_Style(self.nodeType + "#" + self.Id + " " + subtype, rules)

    def styleThisNodesSubNode(self, subtype: str, nodeId: str, rules: set):
        """ Creates a CSS style for a sub-node of this particular node.

            :param subtype: Subtype the CSS rules should apply to.
            :param nodeId:  Id of the sub-node.
            :param rules:   The CSS rules to apply.

            :return:        The finished CSS style instance.

                note::  Author(s): Mitch """

        if self.Id is None:
            raise ValueError("This node doesn't have an identifier assigned.")
        else:
            if not self.nodeTypeInChildren(subtype):
                raise ValueError("The specified subtype does not exist.")
            else:
                if not self.nodeIdInNodes(nodeId, self.getChildrenOfType(subtype)):
                    raise ValueError("The sub id does not exist for the specified subtype.")
                else:
                    return CSS_Style(self.nodeType + "#" + self.Id + " " + subtype + '#' + nodeId, rules)

    def getNodeById(self, Id: str):
        """ Searches the inner HTML for the first node with the given Id.

            :param Id:  The identifier to search for.

            :return:    The identified node or None.

                note::  Author(s): Mitch """

        for node in self.innerHTML:
            if isinstance(node, HTML_Node):
                if node.Id == Id:
                    return node
                elif node.getNodeById(Id) is not None:
                    return node.getNodeById(Id)
        return None


class HTML_Node_Contentless(HTML_Node):
    """ Representation of a HTML single tag with no innerHTML.

        :param nodeType:       Type of the node.
        :param properties:  Properties as a dictionary.

            note::  Author(s): Mitch """

    def __init__(self, nodeType: str, properties: dict = None):
        if properties is None:
            super().__init__(nodeType, dict())
        else:
            super().__init__(nodeType, properties)
        del self.innerHTML

    def toString(self):
        """ Converts this HTML node to a string.

            :return:    Node as string.

                note::  Author(s): Mitch """

        return self.openTagToString()
