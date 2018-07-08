from meta import MetaDict




class HeadersParserExceptions(Exception):
    pass


class HeaderTypeError(HeadersParserExceptions):
    pass


class HDToolsMix:
    def pops(self, *keys):
        return {key: self.pop(key) for key in keys}

    def replace(self, header, old, new):
        self[header] = self[header].replace(old, new)


class HDParser(dict, HDToolsMix, metaclass=MetaDict):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        for k, v in self.items():
            print(k.rjust(30) + ':', v)
        return '-'*77

    def parser(cls, *args):
        filename, = args
        with open(filename) as file:
            data_dict = {}
            for line in file:
                key, *values = cls.valid_header(line).split(':')
                data_dict[key] = ':'.join(values).strip()
            return data_dict

    def main(cls, *args):
        filename, = args
        if isinstance(filename, dict):
            return filename
        elif filename:
            return cls.parser(filename)
    
    def valid_header(cls, line):
        if line.startswith(':'):
            raise HeaderTypeError('{}'.format(line))
        return line




if __name__ == '__main__':
    i = HDParser('_gh.txt')
    print(i)

    i2 = HDParser({'test_header': 'test_value'})
    print(i2)

    
    i3 = HDParser(None)
    print(i3)


    
