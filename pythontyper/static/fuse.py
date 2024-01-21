import json
import re
import ast
import astunparse

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def read_pyi(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data




class CategoryVisitor(ast.NodeVisitor):
    def __init__(self):
        self.category = "local"
        # self.function_stack = []
        self.return_type = None
        self.json_format = {}
        
    def get_json_format(self):
        return self.json_format

    # def split(self, input_string):
    #     input_string = input_string.replace(" ", "")
    #     pairs = input_string.split(",")
    #     result_map = {}
    #     for pair in pairs:
    #         key, value = pair.split(":")
    #         result_map[key] = value
    #     return result_map


    def visit_FunctionDef(self, node):
        # print(astunparse.unparse(node.returns).strip())
        return_type = {}
        return_type["category"]  = "return"
        return_type["name"] = ""
        return_type["type"] = astunparse.unparse(node.returns).strip()
        return_type["source"] = "pytype"

        arg_types = []
        for arg in node.args.args:
            kv_map = {}
            kv_map["category"] = "arg"
            kv_map["name"] = arg.arg
            kv_map["type"] = astunparse.unparse(arg.annotation).strip()
            kv_map["source"] = "pytype"
            arg_types.append(kv_map)

        # arg_types = {()"name": arg.arg, "type": astunparse.unparse(arg.annotation).strip() ) for arg in node.args.args}

        # self.function_stack.append(node.name)
        
        # Retrieve the class name or use "global" if not within a class
        class_name = "global"
        for ancestor in ast.walk(node):
            if isinstance(ancestor, ast.ClassDef):
                class_name = ancestor.name
                break
        
        function_key = f"{node.name}@{class_name}"
        # print(function_key)
        arg_types.append(return_type)
        self.json_format[function_key] = arg_types
        self.generic_visit(node)
        # self.function_stack.pop()
    
    # def visit_arg(self, node):
    #     variable_name = node.arg
    #     type_annotation = astunparse.unparse(node.annotation).strip()
    #     json_record = {
    #         "category": "arg",
    #         "name": variable_name,
    #         "type": [type_annotation]
    #     }
    #     class_name = "global"
    #     for ancestor in ast.walk(node):
    #         if isinstance(ancestor, ast.ClassDef):
    #             class_name = ancestor.name
    #             break
        
    #     function_key = f"{node.name}@{class_name}"
    #     print(function_key)
    #     self.json_records.append(json_record)

    def visit_AnnAssign(self, node):
        variable_name = node.target.id
        type_annotation = astunparse.unparse(node.annotation).strip()
        # category = self.get_category()
        # print(variable_name, category, type_annotation)
        json_record = {
            "category": "global",
            "name": variable_name,
            "type": [type_annotation]
        }
        self.json_format["global@global"] = json_record

    # def get_category(self):
    #     if len(self.function_stack) > 0:
    #         return "arg"
    #     elif self.return_type is not None:
    #         return "return"
    #     else:
    #         return self.category


def extract_type_annotations(pyi_content):
    json_records = []

    tree = ast.parse(pyi_content)
    # for node in ast.walk(tree):
    #     if isinstance(node, ast.AnnAssign):
    #         variable_name = node.target.id
    #         type_annotation = ast.unparse(node.annotation).strip()
            
    visitor = CategoryVisitor()
    visitor.visit(tree)

    return visitor.get_json_format()

def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict:
            merged_dict[key].append(value)
        else:
            merged_dict[key] = [value]
    return merged_dict

def fuse():
    file_name = "./._repo_INFERREDTYPES.json"
    json_data = read_json_file(file_name)
    print(json_data)
    cnt = 0
    new_json_data = {}
    for key, value in json_data.items():
        # print(key)
        pyi_path = "./.pytype/pyi/"+key.replace(".py", ".pyi")[2:]
        try:
            pyi_content = read_pyi(pyi_path)
            annotations = extract_type_annotations(pyi_content)
            print(annotations)
            new_val = merge_dicts(value, annotations)
            # print(new_val)
            new_json_data[key] = new_val
            cnt += 1
        except:
            new_json_data[key] = value
        # if cnt > 0 : break

    output_file = "./fused_types.json"
    with open(output_file, "w") as file:
        json.dump(new_json_data, file, indent=4)
        