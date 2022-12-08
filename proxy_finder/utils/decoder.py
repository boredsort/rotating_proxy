from pathlib import Path, PosixPath

import js2py


class UtfJS:

    """ A decoder class made specifically for https://www.freeproxylists.net/ as the IPs are encrypted
    utf.js is required to use this class, this file can be found on the site.
    """

    js = None
    UTF = None

    def __init__(self):

        file_name = PosixPath('utf.js')
        path = Path.joinpath(Path.cwd(), PosixPath('proxy_finder/utils'), file_name)

        try:
            with path.open("r") as jsfile:
                self.js = jsfile.read()

            self.UTF = js2py.eval_js(self.js)
        except FileNotFoundError as e:
            # will be updated when the logger is built
            print(e.strerror + e.filename )
        except:
            raise Exception("Failed to create UTF JS object")


    def encode(self, txt:str) -> str:
        return self.UTF.URLencode(txt)

    def decode(self, txt:str) -> str:
        return self.UTF.URLdecode(txt)

