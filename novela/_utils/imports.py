# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-22
"""
``novela._utils.imports`` provides classes that fake a uninstalled module
"""
import importlib
import sys


class LazyModule(object):
    r"""Lazy loading modules

    Arguments:
        module_name (str): The path of import.
        global_dict (dict): Override the global dictionary when the module is loaded.

    Examples:
		>>> torch = LazyModule("torch", globals())
		>>> print(torch)
		<cotk._utils.imports.LazyModule object at 0x000001BE147682E8>
		>>> torch.Tensor = LazyObject("torch.Tensor")
		>>> print(torch.Tensor)
		<cotk._utils.imports.LazyObject object at 0x000001BE1339CE80>
		>>> print(torch.LongTensor)
		<class 'torch.LongTensor'>
		>>> print(torch.Tensor)
		<class 'torch.Tensor'>
		>>> print(torch)
		<module 'torch'>
    """
    def __init__(self, module_name, global_dict):
        super().__init__()
        self._module_name = module_name
        self._global_dict = global_dict

    def _try_load(self):
        if super().__getattribute__("_module_name") in sys.modules:
            return sys.modules[super().__getattribute__("_module_name")]
        else:
            return None

    def _load(self):
        module = importlib.import_module(super().__getattribute__("_module_name"))
        global_dict = super().__getattribute__("_global_dict")
        global_dict[super().__getattribute__("_module_name")] = module
        return module

    def __getattribute__(self, key):
        """属性拦截器"""
        # 首先从当前已经导入的模块中加载
        loaded = super().__getattribute__("_try_load")()
        if loaded is not None:
            return getattr(loaded, key)

        # 如果当前已经加载的模块中不存在
        try:
            return super().__getattribute__(key)
        except AttributeError:
            pass

        if key == "__bases__":
            return tuple()
        else:
            return getattr(super().__getattribute__("_load")(), key)


class LazyObject(object):
    r"""
    Lazy loading objects.

    Arguments:
        object_name (str): The path of import.
    """
    def __init__(self, object_name):
        super().__init__()
        self._object_name = object_name
        self._module_name = object_name.split(".")[0]

    def _try_load_module(self):
        if super().__getattribute__("_module_name") in sys.modules:
            return sys.modules[super().__getattribute__("_module_name")]
        else:
            return None

    def _load_object(self):
        mod = importlib.import_module(super().__getattribute__("_module_name"))
        arr = super().__getattribute__("_object_name").split(".")
        obj = getattr(mod, arr[1])
        for i in range(2, len(arr)):
            try:
                obj = getattr(obj, arr[i])
            except AttributeError:
                raise AttributeError("No attribute {} in {}.".format(arr[i], ".".join(arr[:i])))
        return obj

    def _try_getattribute(self, key):
        loaded = super().__getattribute__("_try_load_module")()
        if loaded is not None:
            return getattr(super().__getattribute__("_load_object")(), key)

        try:
            return super().__getattribute__(key)
        except AttributeError:
            pass
        return None

    def __getattribute__(self, key):
        loaded = super().__getattribute__("_try_load_module")()
        if loaded is not None:
            return getattr(super().__getattribute__("_load_object")(), key)

        try:
            return super().__getattribute__(key)
        except AttributeError:
            pass

        if key == "__bases__":
            return tuple()
        else:
            return getattr(super().__getattribute__("_load_object")(), key)

    def __call__(self, *args, **kwargs):
        return self._load_object()(*args, **kwargs)

    @staticmethod
    def peek(obj, key):
        if isinstance(obj, LazyObject):
            loaded = obj._try_load_module()
            if loaded is not None:
                return getattr(obj, key)
            else:
                return obj._try_getattribute(key)
        else:
            return None