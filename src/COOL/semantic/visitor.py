from COOL.error import Error
from COOL.nodes.basic_classes import BasicBool, BasicInt, BasicIO, BasicObject, BasicString

class Visitor:

    def __init__(self):
        self.types:dict = {'Object':BasicObject(),'IO':BasicIO()}
        #TODO implement the basic types
        self.basic_types: dict = {
            'Object': BasicObject(), 'IO': BasicIO(), 'Int': BasicInt(), 'String': BasicString(), 'Bool': BasicBool()}

        self.tree = {}# Is the tree of heritance, In each "key" there is a class and its "value" is the class from which it inherits.
        self.errors = []

    def _check_cycle(self, class_:str, node):
        temp_class = class_
        lineage = set()
        lineage.add(class_)
        while temp_class in self.tree.keys():
            if self.types[temp_class].inherits in lineage:
                self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Class {class_}, or an ancestor of {class_}, is involved in an inheritance cycle.'))
                return 
            lineage.add(self.types[temp_class].inherits)
            temp_class = self.tree[temp_class]

    def inheritable_class(self, class_str:str):
        return class_str in self.types.keys()

    def _search_lineage(self,class_:str):
        temp_class = class_
        lineage = []

        while temp_class in self.tree.keys():
            if temp_class in lineage: 
                if temp_class == class_:
                    lineage.pop()
                    return lineage
            inherits_ = self.types[temp_class].inherits
            if inherits_:
                lineage.append(inherits_)
                temp_class = self.tree[temp_class]

            else: break
        return lineage
    
    def _search_attribute_name_in_lineage(self, lineage:list, attrib):
        attrb_equals=[]
        for i in lineage:
            if not i:
                break
            if not self.inheritable_class(i):
                break
            for comprobate_attr in self.types.get(i).attributes:
                if attrib.id == comprobate_attr.id and type(attrib):
                    attrb_equals.append(comprobate_attr)
        return attrb_equals

    def _search_method_name_in_lineage(self, lineage:list, method):
        meths_equals=[]
        for i in lineage:
            if not i:
                break
            if not self.inheritable_class(i):
                break
            for comprobate_meth in self.types.get(i).methods:
                if method.id == comprobate_meth.id:                  
                    meths_equals.append(comprobate_meth)
        return meths_equals
    
    def visit_program(self, node):
        for i in node.classes:
            if  i.type in self.basic_types.keys():
                self.errors.append(Error.error(i.line,i.column,'SemanticError',f'Redefinition of basic class {i.type}.' ))
            elif i.type in self.types.keys():
            #TODO search this error
                self.errors.append(Error.error(i.line,i.column,"TypeError",f'Repeated class name {i.type}'))
            self.types[i.type] = i

        for cls in node.classes:
            if cls.inherits:
                if not cls.inherits in self.types.keys():
                    if cls.inherits in self.basic_types:
                        self.errors.append(Error.error(cls.line, cls.column, 'SemanticError',
                            f'Class {cls.type} cannot inherit class {cls.inherits}. '))
                    else :
                        self.errors.append(Error.error(cls.line, cls.column, 'TypeError',
                            f'Class {cls.type} inherits from an undefined class {cls.inherits}.'))
                self.tree[cls.type] = cls.inherits
                self._check_cycle(cls.type,cls)

    def _analize_methods(self, features):
        meth_node = set()
        for meth in features:
            if meth.id in meth_node:
                self.errors.append(Error.error(meth.line,meth.column,'SemanticError',f'Method {meth.id} is multiply defined.'))

            if meth.type not in self.types.keys() and not (meth.type in self.basic_types.keys()):
                self.errors.append(Error.error(meth.line,meth.column,'TypeError',f'Undefined return type {meth.type} in method test.'))

            meth_formals_name = set()
            for formal in meth.formals:
                
                if formal.type not in self.types.keys() and not (formal.type in self.basic_types.keys()):
                    self.errors.append(Error.error(meth.line,meth.column,'TypeError',f'Class {formal.type} of formal parameter {formal.id} is undefined.'))
                
                if formal.id in meth_formals_name:
                    self.errors.append(Error.error(meth.line,meth.column,'SemanticError',f'Formal parameter {formal.id} is multiply defined.'))
                meth_formals_name.add(formal.id)
            meth_node.add(meth.id)
        
    def _analize_attributes(self, features):
        attrib_node = set()
        for attrb in features:
            if attrb.id in attrib_node:
                self.errors.append(Error.error(attrb.line,attrb.column,'SemanticError',f'Attribute {attrb.id} is multiply defined in class.'))

            if attrb.type not in self.types.keys() and not (attrb.type in self.basic_types.keys()):
                self.errors.append(Error.error(attrb.line,attrb.column,'TypeError',f'Class {attrb.type} of attribute {attrb.id} is undefined.'))

            if attrb.__dict__.get('expr'):
                if attrb.expr.__dict__.get('type'):
                    expr_type = attrb.expr.type 
                    if not (attrb.type == expr_type):
                        lineage_expr_type = self._search_lineage(expr_type)
                        if not (attrb.type in lineage_expr_type):
                            self.errors.append(Error.error(attrb.line,attrb.column,'TypeError',f'Inferred type {expr_type} of initialization of attribute {attrb.id} does not conform to declared type {attrb.type}.'))

            attrib_node.add(attrb.id)

    def visit_class(self, node):
        # TODO veryfy if the type and the count of the formal parameters in a heritance method is the same as the original method to subscribe
        
        self._analize_attributes(node.attributes)
        self._analize_methods(node.methods)

        lineage = self._search_lineage(node.type)

        for attrb in node.attributes:
            equals_attrbs = self._search_attribute_name_in_lineage(lineage,attrb)
            if len(equals_attrbs) > 0:
                #TODO analize if the types are different
                self.errors.append(Error.error(attrb.line,attrb.column,'SemanticError',f'Attribute {attrb.id} is an attribute of an inherited class.'))


        for meth in node.methods:
            equals_methods = self._search_method_name_in_lineage(lineage, meth)
            if len(equals_methods) > 0:
                equal_meth = equals_methods[0]
                
                if len(meth.formals) != len(equal_meth.formals):
                    self.errors.append(Error.error(meth.line,meth.column,'SemanticError',f'Incompatible number of formal parameters in redefined method {meth.id}.'))
                    break
                for j in range(len(meth.formals)):
                    if meth.formals[j].type != equal_meth.formals[j].type:
                        self.errors.append(Error.error(meth.line,meth.column,'SemanticError',f'In redefined method {meth.id}, parameter type {meth.formals[j].type} is different from original type {equal_meth.formals[j].type}.'))
                
                if meth.type != equal_meth.type:
                    self.errors.append(Error.error(meth.line,meth.column,'SemanticError',f'In redefined method {meth.id}, return type {meth.type} is different from original return type {equal_meth.type}.'))
            
        
        node.methods_dict = {}
        node.attributes_dict = {}
        node.features_dict = {}

        for anc_class in lineage.reverse():
            anc_class = self.types[anc_class]
            for attrb in anc_class.attributes:
                node.attributes_dict[attrb.id] = attrb
            for meth in anc_class.methods:
                node.methods_dict[meth.id] = meth
            for feat in anc_class.features:
                node.features_dict[feat.id] = feat

        node.methods_dict.update({i.id:i for i in node.methods})
        node.attributes_dict.update({i.id:i for i in node.attributes})
        node.features_dict.update({i.id: i for i in node.features})



    def visit_method(self, node):
        pass
    # TODO check if every expr in the method is conform with its type and every formal (variable declaration) is correct

    # def visit_variable(self, node):
    #     pass

    def visit_attribute(self, node):
        pass

        # if node.expr:
        #     if not node.expr.type == node.type:
        #         #TODO search this error
        #         self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible type of attribute in {node.id} in {node.type}'))
                    
        # #TODO when an attribute does have the same static and dynamic type(or not inheritance)
        #TypeError: Inferred type F of initialization of attribute test does not conform to declared type B. 
    # def visit_expression(self, node):
    #     pass


    def visit_attribute_declaration(self, node):
        pass


    def visit_attribute_inicialization(self, node):
        pass