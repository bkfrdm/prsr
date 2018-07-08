TRACE = False


class MetaDict(type):
    def __new__(meta, classname, supers, classdict):
        for attr, val in classdict.items():
            if not attr.startswith('__') and callable(val):
                classdict[attr] = classmethod(val)

                if TRACE: print(attr.rjust(20), '==>', val)
                
        return type.__new__(meta, classname, supers, classdict)
                
    def __call__(cls, *args):
        data = cls.main(*args)
        if not data: return
        
        new_cls = type(
            cls.__name__,
            cls.__bases__,
            {k: v for k, v in cls.__dict__.items() if not k == '__init__'})
        
        instance = new_cls(data)
        instance = cls.rebind_init_values(instance, *args)
        
        return instance

    def rebind_init_values(cls, instance, *args):
        for n, v in zip(cls.__init__.__code__.co_names, args):
            # __dict__ descriptor is broken -> TypeError
            setattr(instance, n, v)

        return instance
