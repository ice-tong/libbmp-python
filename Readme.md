# libbmp-python

A basic bmp library implemented in pure python, for study purpose only.

# how to use

```python
from libbmp import BMPFile
from libbmp import load_bmp

bmp: "BMPFile" = load_bmp("./test_bmps/test.bmp")
print("BMP size:", bmp.size)
print("BMP first pixel:", bmp[0][0])
bmp.save_bmp("./test_bmps/test_svae.bmp")
```

# TODO

- [ ] 16 bit color data
- [ ] Pseudo color support
