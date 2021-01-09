import os, pathlib, itertools
pem = os.getenv('PEM').split()
pathlib.Path('pem').write_text(' '.join((pem[0], '\n'.join(itertools.islice(pem, 1, len(pem) - 1)), pem[-1])))
key = os.getenv('KEY').split()
pathlib.Path('key').write_text(' '.join((key[0], key[1], '\n'.join(itertools.islice(key, 2, len(key) - 2)), key[-2], key[-1])))
