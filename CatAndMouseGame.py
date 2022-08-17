import base64
import py3rijndael
import gzip
import msgpack
import main


def getAssetBundle(assetbundle):
    data = base64.b64decode(assetbundle)
    key = b'nn33CYId2J1ggv0bYDMbYuZ60m4GZt5P'  # By default is NA
    iv = data[:32]
    array = data[32:]

    if main.fate_region == "JP":
        key = b'W0Juh4cFJSYPkebJB9WpswNF51oa6Gm7'

    cipher = py3rijndael.RijndaelCbc(
        key,
        iv,
        py3rijndael.paddings.Pkcs7Padding(16),
        32
    )

    data = cipher.decrypt(array)
    gzip_data = gzip.decompress(data)
    data_unpacked = msgpack.unpackb(gzip_data)

    return data_unpacked
