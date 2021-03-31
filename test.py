from libbmp import BMPFile


if __name__ == "__main__":

    bmp = BMPFile("./test_bmps/test.bmp")

    print("BMP file header:")
    print(bmp.bmp_fheader)

    print("BMP info header:")
    print(bmp.bmp_iheader)

    print("BMP size:", bmp.size)

    print("BMP first pixel:", mp[0][0])

    bmp.save_bmp("./test_bmps/test_svae.bmp")
