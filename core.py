import yaml, os, re
import importlib.util

yaml.warnings({'YAMLLoadWarning': False})


class ObjFile:
    def __init__(self, path, prev_path=None):
        self.prev_path = prev_path

        abs_file = os.path.abspath(os.path.join(prev_path, path) if prev_path else path)
        self.path = os.path.dirname(abs_file)

        data = yaml.load(open(abs_file, "r"))

        if "namespace" in data:
            self.namespace = data["namespace"]
        else:
            base = base=os.path.basename(path)
            self.namespace = os.path.splitext(base)[0]

        self.metadata = self.ns_dict(data["metadata"]) if "metadata" in data else None

        self.classes = {}
        self.load_imports(data["includes"]) if "includes" in data else None

        self.objects = {}
        self.load_objects(data["objects"]) if "objects" in data else None



    def ns_dict(self, d):
        return {"{}.{}".format(self.namespace, k): v for k, v in d.items()}

    def ns_or_default(self, d, key):
        if not isinstance(key, str):
            raise Exception("Unable to fetch {}".format(key))

        if "." not in key:
            key = "{}.{}".format(self.namespace, key)

        if key in d:
            return d[key]
        else:
            raise Exception("Unable to fetch {}".format(key))

    def get_class(self, key):
        return self.ns_or_default(self.classes, key)

    def get_object(self, key):
        return self.ns_or_default(self.objects, key)

    def get_metadata(self, key):
        return self.ns_or_default(self.metadata, key)

    def load_import_python(self, i, name):
        foo = importlib.import_module(i)
        self.classes = self.classes | self.ns_dict(foo.classes)

    def load_import_yaml(self, i):
        pass

    def load_imports(self, imports):
        for i in imports:
            if os.path.isfile(os.path.join(self.path, "{}.py".format(i))):
                path = os.path.join(self.path, "{}.py".format(i))
                self.load_import_python(i, path)
            else:
                if os.path.isfile(os.path.join(self.path, "{}.yaml".format(i))):
                    self.load_import_yaml(i)
                elif os.path.isfile(os.path.join(self.path, "{}.yml".format(i))):
                    self.load_import_yaml(i)

    def load_objects(self, objects):
        names = self.ns_dict(objects)

        for k, v in names.items():
            t = v["__type__"]
            del v["__type__"]
            try:
                self.objects[k] = self.get_class(t)(self, **v)
            except Exception as e:
                raise Exception("{} while instantiating {}".format(e, t))


