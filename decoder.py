import js2py


# def decoder(value):
# js = None

# with open("utf.js", "r") as jsfile:
#     js = jsfile.read()


# enc = "%3c%61%20%68%72%65%66%3d%22%68%74%74%70%73%3a%2f%2f%77%77%77%2e%66%72%65%65%70%72%6f%78%79%6c%69%73%74%73%2e%6e%65%74%2f%31%34%32%2e%31%31%2e%32%32%32%2e%32%32%2e%68%74%6d%6c%22%3e%31%34%32%2e%31%31%2e%32%32%32%2e%32%32%3c%2f%61%3e"
# utf = js2py.eval_js(js)

# txt = utf.URLdecode(enc)
# print(txt)


class UtfJS:

    js = None
    UTF = None

    def __init__(self):

        try:
            with open("utf.js", "r") as jsfile:
                js = jsfile.read()

            UTF = js2py.eval_js(self.js)
        except:
            raise Exception("Failed to create UTF JS object")


    def encode(self, txt):
        return self.UTF.URLencode(txt)

    def decode(self, txt):
        return self.UTF.URLdecode(txt)

