from urllib.parse import urlparse
import pandas as pd
import urllib
import hashlib
import mmh3
import mmh as mmhash
import base64
import base58
import zlib
import json
import re
from urllib.parse import quote_plus, unquote_plus
import codecs

from lzstring import LZString
import html
import brotli
import lzma
import brotli


# DELIMITERS = re.compile('[&|\,]')
DELIMITERS = re.compile(r'[&|,=]')

EXTENSION_RE = re.compile('\.[A-Za-z]{2,4}$')
ENCODING_LAYERS = 3
ENCODINGS_NO_ROT = ['base64', 'base32', 'base16',
    'base58', 'zlib', 'gzip', 'urlencode',
    'entity', 'zlib64', 'brotli_base64', 'json',
    'deflate_base64', 'deflateraw_base64', 'gzip_base64',
    'hex' ]
LIKELY_ENCODINGS = ['base16', 'base32', 'base58', 'base64',
                    'urlencode',  'entity', 'zlib64']
HASHES = [  'md5', 'sha1', 'sha256', 'sha224', 'sha384',
          'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',   'mmh3_32', 'mmh3_64_1', 'mmh3_64_2', 'mmh3_128',  ]


class Hasher():
    def __init__(self):
        # Define Supported hashes
        hashes = dict()
        # hashes['md2'] = lambda x: self._get_md2_hash(x)
        hashes['md5'] = lambda x: hashlib.md5(x).hexdigest()
        hashes['sha1'] = lambda x: hashlib.sha1(x).hexdigest()
        hashes['sha256'] = lambda x: hashlib.sha256(x).hexdigest()
        hashes['sha224'] = lambda x: hashlib.sha224(x).hexdigest()
        hashes['sha384'] = lambda x: hashlib.sha384(x).hexdigest()
        hashes['sha512'] = lambda x: hashlib.sha512(x).hexdigest()
        hashes['sha3_224'] = lambda x: hashlib.sha3_224(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
        hashes['sha3_256'] = lambda x: hashlib.sha3_256(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
        hashes['sha3_384'] = lambda x: hashlib.sha3_384(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
        hashes['sha3_512'] = lambda x: hashlib.sha3_512(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
        hashes['mmh3_32'] = lambda x: str(mmh3.hash(x))
        hashes['mmh3_64_1'] = lambda x: str(mmh3.hash64(x)[0])
        hashes['mmh3_64_2'] = lambda x: str(mmh3.hash64(x)[1])
        hashes['mmh3_128'] = lambda x: str(mmh3.hash128(x))
       # hashes['blake2b'] = lambda x: pyblake2.blake2b(x).hexdigest()
       # hashes['blake2s'] = lambda x: pyblake2.blake2s(x).hexdigest()
        hashes['crc32'] = lambda x: str(zlib.crc32(x) & 0xFFFFFFFF)
        hashes['adler32'] = lambda x: str(zlib.adler32(x))

        self._hashes = hashes
        self.hashes_and_checksums = list(self._hashes.keys())
        self.supported_hashes = HASHES

    def _get_hashlib_hash(self, name, string):
        """Use for hashlib hashes that don't have a shortcut"""
        hasher = hashlib.new(name)
        hasher.update(string)
        return hasher.hexdigest()

    def _get_md2_hash(self, string):
        """Compute md2 hash"""
        md2 = MD2.new()
        md2.update(string)
        return md2.hexdigest()

    def get_hash(self, hash_name, string):
        """Compute the desired hash"""
        return self._hashes[hash_name](string)


class Encoder():
    def __init__(self):
        # Define supported encodings
        encodings = dict()
        encodings['base16'] = lambda x: base64.b16encode(x)
        encodings['base32'] = lambda x: base64.b32encode(x)
        encodings['base58'] = lambda x: base58.b58encode(x)
        encodings['base64'] = lambda x: base64.b64encode(x)
        encodings['urlencode'] = lambda x: quote_plus(x)
        encodings['deflate'] = lambda x: self._compress_with_zlib('deflate', x)
        encodings['zlib'] = lambda x: self._compress_with_zlib('zlib', x)
        encodings['gzip'] = lambda x: self._compress_with_zlib('gzip', x)
        encodings['json'] = lambda x: json.dumps(x)
        encodings['binary'] = lambda x: ''.join(format(ord(c), '08b') for c in x)
        encodings['entity'] = lambda x: html.escape(x)
        encodings['rot13'] = lambda x: codecs.encode(x, 'rot_13')
        
        for i in range(1, 26):
            if i == 13:
                continue  # handled separately with codecs
            encodings[f'rot{i}'] = lambda x, i=i: rot_n(x, i)
 
        encodings['deflate_base64'] = lambda x: base64.b64encode(zlib.compress(x))
        encodings['deflateraw_base64'] = lambda x: base64.b64encode(zlib.compress(x, -zlib.MAX_WBITS))
        encodings['gzip_base64'] = lambda x: base64.b64encode(zlib.compress(x, zlib.MAX_WBITS | 16))
        encodings['brotli_base64'] = lambda x: base64.b64encode(brotli.compress(x))
        encodings['deflate_hex'] = lambda x: zlib.compress(x).hex()
        encodings['gzip_hex'] = lambda x: zlib.compress(x, zlib.MAX_WBITS | 16).hex()
        
        
        try:
            lz = LZString()
            encodings['lz64'] = lambda x: base64.b64encode(lz.compress(x.decode('utf-8')).encode('utf-8'))
        except:
            pass
        
        try:
            lz = LZString()
            encodings['lz64de'] = lambda x: base64.b64encode(LZString().compress(x.decode('utf-8')).encode('utf-8')).decode('utf-8')
        except:
            pass
        
        encodings['zlib64'] = lambda x: base64.b64encode(zlib.compress(x.encode('utf-8') if isinstance(x, str) else x)).decode('utf-8')
        
        try:
            import lzw
            encodings['lzw'] = lambda x: json.dumps(lzw.encode(x.decode('utf-8')))
        except:
            pass
        try:
            lz = LZString()
            encodings['lz_string'] = lambda x: lz.compressToEncodedURIComponent(x.decode('utf-8'))
        except:
            pass
        self._encodings = encodings
        self.supported_encodings = list(self._encodings.keys())

    def _compress_with_zlib(self, compression_type, string, level=6):
        """Compress in one of the zlib supported formats: zlib, gzip, or deflate.
        For a description see: http://stackoverflow.com/a/22311297/6073564
        """
        if compression_type == 'deflate':
            compressor = zlib.compressobj(level, zlib.DEFLATED,
                                          -zlib.MAX_WBITS)
        elif compression_type == 'zlib':
            compressor = zlib.compressobj(level, zlib.DEFLATED,
                                          zlib.MAX_WBITS)
        elif compression_type == 'gzip':
            compressor = zlib.compressobj(level, zlib.DEFLATED,
                                          zlib.MAX_WBITS | 16)
        else:
            raise ValueError("Unsupported zlib compression format %s." %
                             compression_type)
        return compressor.compress(string) + compressor.flush()

    def encode(self, encoding, string):
        """Encode `string` in desired `encoding`"""
        return self._encodings[encoding](string)


class DecodeException(Exception):
    def __init__(self, message, error):
        super(DecodeException, self).__init__(message)
        self.error = error


def rot_n(text, n):
    def rotate_char(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + n) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + n) % 26 + ord('A'))
        return c
    return ''.join(rotate_char(c) for c in text)

class Decoder():
    def __init__(self):
        # Define supported encodings
        decodings = dict()
        decodings['base16'] = lambda x: base64.b16decode(x)
        decodings['base32'] = lambda x: base64.b32decode(x)
        decodings['base58'] = lambda x: base58.b58decode(x)
        decodings['base64'] = lambda x: base64.b64decode(x)
        decodings['urlencode'] = lambda x: unquote_plus(x)
        decodings['deflate'] = lambda x: self._decompress_with_zlib('deflate',
                                                                    x)
        decodings['zlib'] = lambda x: self._decompress_with_zlib('zlib', x)
        decodings['gzip'] = lambda x: self._decompress_with_zlib('gzip', x)
        decodings['json'] = lambda x: json.loads(x)
        decodings['binary'] = lambda x: ''.join(chr(int(x[i:i+8], 2)) for i in range(0, len(x), 8))
        decodings['entity'] = lambda x: html.unescape(x)
        
        decodings['rot13'] = lambda x: codecs.decode(x, 'rot_13')
        
        for i in range(1, 26):
            if i == 13:
                continue  # handled separately with codecs
            decodings[f'rot{i}'] = lambda x, i=i: rot_n(x, i)
            
        try:
            lz = LZString()
            decodings['lz64'] = lambda x: lz.decompress(base64.b64decode(x).decode('utf-8'))
        except:
            pass
        
        decodings['zlib64'] = lambda x: zlib.decompress(base64.b64decode(x)).decode('utf-8', errors='ignore')
        
        try:
            lz = LZString()
            decodings['lz64de'] = lambda x: LZString().decompress(base64.b64decode(x).decode('utf-8'))
        except:
            pass

        try:
            lz = LZString()
            decodings['lz_string'] = lambda x: lz.decompressFromEncodedURIComponent(x)
        except:
            pass

        try:
            
            import lzw
            decodings['lzw'] = lambda x: ''.join(lzw.decode(json.loads(x)))
        except:
            pass

        try:
            decodings['brotli_base64'] = lambda x: brotli.decompress(base64.b64decode(x)).decode('utf-8', errors='ignore')
        except:
            pass

        decodings['deflate_base64'] = lambda x: zlib.decompress(base64.b64decode(x), -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
        decodings['deflateraw_base64'] = lambda x: zlib.decompress(base64.b64decode(x), -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
        decodings['gzip_base64'] = lambda x: zlib.decompress(base64.b64decode(x), zlib.MAX_WBITS | 16).decode('utf-8', errors='ignore')
        decodings['deflate_hex'] = lambda x: zlib.decompress(bytes.fromhex(x)).decode('utf-8', errors='ignore')
        decodings['gzip_hex'] = lambda x: zlib.decompress(bytes.fromhex(x), zlib.MAX_WBITS | 16).decode('utf-8', errors='ignore')
 
        self._decodings = decodings
        self.supported_encodings = list(self._decodings.keys())

    def _decompress_with_zlib(self, compression_type, string, level=9):
        """Compress in one of the zlib supported formats: zlib, gzip, or deflate.
        For a description see: http://stackoverflow.com/a/22311297/6073564
        """
        if compression_type == 'deflate':
            return zlib.decompress(string, -zlib.MAX_WBITS)
        elif compression_type == 'zlib':
            return zlib.decompress(string, zlib.MAX_WBITS)
        elif compression_type == 'gzip':
            return zlib.decompress(string, zlib.MAX_WBITS | 16)
        else:
            raise ValueError("Unsupported zlib compression format %s." %
                             compression_type)

    def decode_error(self):
        """Catch-all error for all supported decoders"""

    def decode(self, encoding, string):
        """Decode `string` encoded by `encoding`"""
        try:
            return self._decodings[encoding](string)
        except Exception as e:
            raise DecodeException(
                'Error while trying to decode %s' % encoding,
                e
            )


class LeakDetector():
    def __init__(self, search_strings, precompute_hashes=True, hash_set=None,
                 hash_layers=2, precompute_encodings=True, encoding_set=None,
                 encoding_layers=2, debugging=False):
        """LeakDetector searches URL, POST bodies, and cookies for leaks.

        The detector is constructed with a set of search strings (given by
        the `search_strings` parameters. It has several methods to check for
        leaks containing these strings in URLs, POST bodies, and cookie header
        strings.

        Parameters
        ==========
        search_strings : list
            LeakDetector will search for leaks containing any item in this list
        precompute_hashes : bool
            Set to `True` to include precomputed hashes in the candidate set.
        hash_set : list
            List of hash functions to use when building the set of candidate
            strings.
        hash_layers : int
            The detector will find instances of `search_string` iteratively
            hashed up to `hash_layers` times by any combination of supported
            hashes.
        precompute_encodings : bool
            Set to `True` to include precomputed encodings in the candidate set
        encoding_set : list
            List of encodings to use when building the set of candidate
            strings.
        encoding_layers : int
            The detector will find instances of `search_string` iteratively
            encoded up to `encoding_layers` times by any combination of
            supported encodings.
        debugging : bool
            Set to `True` to enable a verbose output.
        """
        self.search_strings = search_strings
        self._min_length = min([len(x) for x in search_strings])
        self._hasher = Hasher()
        self._hash_set = hash_set
        self._hash_layers = hash_layers
        self._encoder = Encoder()
        self._encoding_set = encoding_set
        self._encoding_layers = encoding_layers
        self._decoder = Decoder()
        self._precompute_pool = dict()
        # If hash/encoding sets aren't specified, use all available.
        if self._hash_set is None:
            self._hash_set = self._hasher.supported_hashes
        if self._encoding_set is None:
            self._encoding_set = self._encoder.supported_encodings
        self._build_precompute_pool(precompute_hashes, precompute_encodings)
        self._debugging = debugging

    def _compute_hashes(self, string, layers, prev_hashes=tuple()):
        """Returns all iterative hashes of `string` up to the
        specified number of `layers`"""
        for h in self._hasher.supported_hashes:
            hashed_string = self._hasher.get_hash(h, string.encode('utf-8'))
            if hashed_string == string:  # skip no-ops
                continue
            hash_stack = (h,) + prev_hashes
            self._precompute_pool[hashed_string] = hash_stack
            if layers > 1:
                self._compute_hashes(hashed_string, layers-1, hash_stack)

    def _compute_encodings(self, string, layers, prev_encodings=tuple()):
        for enc in self._encoding_set:
            try:
                input_data = string.encode('utf-8') if enc in ['base16', 'base32', 'base58', 'base64', 'deflate', 'zlib', 'gzip'] else string
                encoded = self._encoder.encode(enc, input_data)
                if isinstance(encoded, bytes):
                    encoded_string = encoded.decode('utf-8', errors='ignore')
                else:
                    encoded_string = str(encoded)
            except Exception:
                continue
            if encoded_string == string:
                continue
            encoding_stack = (enc,) + prev_encodings
            self._precompute_pool[encoded_string] = encoding_stack
            if layers > 1:
                self._compute_encodings(encoded_string, layers - 1, encoding_stack)

    def _build_precompute_pool(self, precompute_hashes, precompute_encodings):
        """Build a pool of hashes for the given search string"""
        seed_strings = list()
        for string in self.search_strings:
            seed_strings.append(string)
            if string.startswith('http'):
                continue
            all_lower = string.lower()
            if all_lower != string:
                seed_strings.append(string.lower())
            all_upper = string.upper()
            if all_upper != string:
                seed_strings.append(string.upper())

        strings = list()
        for string in seed_strings:
            strings.append(string)
            # If the search string appears to be an email address, we also want
            # to include just the username portion of the URL, and the address
            # and username with any '.'s removed from the username (since these
            # are optional in Gmail).
            if '@' in string:
                parts = string.rsplit('@')
                if len(parts) == 2:
                    uname, domain = parts
                    strings.append(uname)
                    strings.append(re.sub('\.', '', uname))
                    strings.append(re.sub('\.', '', uname) + '@' + domain)
                # Domain searches have too many false positives
                # strings.append(parts[1])
                # strings.append(parts[1].rsplit('.', 1)[0])
            # The URL tokenizer strips file extensions. So if our search string
            # has a file extension we should also search for a stripped version
            if re.match(EXTENSION_RE, string):
                strings.append(re.sub(EXTENSION_RE, '', string))
        for string in strings:
            self._precompute_pool[string] = (string,)
        self._min_length = min([len(x) for x in self._precompute_pool.keys()])
        initial_items = list(self._precompute_pool.items())
        if precompute_hashes:
            for string, name in initial_items:
                self._compute_hashes(string, self._hash_layers, name)
        if precompute_encodings:
            for string, name in initial_items:
                self._compute_encodings(string, self._encoding_layers, name)

    def _split_on_delims(self, string, rv_parts, rv_named):
        """Splits a string on several delimiters"""
        if string == '':
            return
        parts = set(re.split(DELIMITERS, string))
        if '' in parts:
            parts.remove('')
        for part in parts:
            if part == '':
                continue
            count = part.count('=')
            if count != 1:
                rv_parts.add(part)
            if count == 0:
                continue
            n, k = part.split('=', 1)
            if len(n) > 0 and len(k) > 0:
                rv_named.add((n, k))
            else:
                rv_parts.add(part)

    def check_if_in_precompute_pool(self, string):
        """Returns a tuple that lists the (possibly layered) hashes or
        encodings that result in input string
        """
        try:
            return self._precompute_pool[str(string)]
        except KeyError:
            return
        except (UnicodeDecodeError, UnicodeEncodeError):
            return

    def check_for_leak(self, string, layers=1, prev_encodings=tuple(),
                       prev=''):
        """Check if given string contains a leak"""
        # Short tokens won't contain email address
        if len(string) < self._min_length:
            return

        # Check if direct hash or plaintext
        rv = self.check_if_in_precompute_pool(string)
        if rv is not None:
            return prev_encodings + rv

        # Try encodings
        for encoding in self._encoding_set:
            # multiple rots are unnecessary
            if encoding.startswith('rot') and prev.startswith('rot'):
                continue
            try:
                decoded = self._decoder.decode(encoding, string)
                if type(decoded) == int:
                    decoded = str(decoded)
            except DecodeException:  # means this isn't the correct decoding
                continue
            if decoded == string:  # don't add no-ops
                continue
            if decoded is None:  # Empty decodings aren't useful
                continue
            encoding_stack = prev_encodings + (encoding,)
            if layers > 1:
                rv = self.check_for_leak(decoded, layers-1,
                                         encoding_stack, encoding)
                if rv is not None:
                    return rv
            else:
                # New: allow substring matches
                for known_string, transform_stack in self._precompute_pool.items():
                    if known_string in str(decoded):
                        return encoding_stack + transform_stack
        return

    def _check_parts_for_leaks(self, tokens, parameters, nlayers):
        """Check token and parameter string parts for leaks"""
        leaks = list()
        for token in tokens:
            leak = self.check_for_leak(token, layers=nlayers)
            if leak is not None:
                leaks.append(leak)
        for name, value in parameters:
            leak = self.check_for_leak(value, layers=nlayers)
            if leak is not None:
                leaks.append(leak)
            leak = self.check_for_leak(name, layers=nlayers)
            if leak is not None:
                leaks.append(leak)
        return leaks

    def _split_url(self, url):
        """Split url path and query string on delimiters"""
        tokens = set()
        parameters = set()
        try:
            purl = urlparse(url)
        except ValueError:
            print(f"Can't parse url: {url}")
            return [], []
        path_parts = purl.path.split('/')
        for part in path_parts:
            if not part.endswith('.com'):
                part = re.sub(EXTENSION_RE, '', part)
            self._split_on_delims(part, tokens, parameters)
        self._split_on_delims(purl.query, tokens, parameters)
        self._split_on_delims(purl.fragment, tokens, parameters)
        return tokens, parameters

    def check_url(self, url, encoding_layers=3, substring_search=True):
        """Check if a given url contains a leak"""
        tokens, parameters = self._split_url(url)
        if self._debugging:
            print("URL tokens:") 
            print(tokens)
            for token in tokens:
                print(token)
            print("\nURL parameters:")
            for key, value in parameters:
                print("Key: %s | Value: %s" % (key, value))
        return self._check_whole_and_parts_for_leaks(
            url, tokens, parameters, encoding_layers, substring_search)

    def _get_header_str(self, header_str, header_name):
        """Returns the header string parsed from `header_str`"""
        for item in json.loads(header_str):
            if item[0] == header_name:
                return item[1]
        return ""

    def _split_cookie(self, cookie_str, from_request=True):
        """Returns all parsed parts of the cookie names and values"""
        tokens = set()
        parameters = set()
        try:
            if from_request:
                cookies = ck.Cookies.from_request(cookie_str)
            else:
                cookies = ck.Cookies.from_response(cookie_str,
                                                   ignore_bad_cookies=True)
        except (ck.InvalidCookieError, UnicodeDecodeError, KeyError):
            return tokens, parameters  # return empty sets

        for cookie in cookies.values():
            self._split_on_delims(cookie.name, tokens, parameters)
            self._split_on_delims(cookie.value, tokens, parameters)
        return tokens, parameters

    def get_location_str(self, header_str):
        return self._get_header_str(header_str, "Location")

    def get_referrer_str(self, header_str):
        return self._get_header_str(header_str, "Referer")

    def get_cookie_str(self, header_str, from_request=True):
        if not header_str:
            return ""
        if from_request:
            header_name = 'Cookie'
        else:
            header_name = 'Set-Cookie'

        return self._get_header_str(header_str, header_name)

    def check_cookies(self, header_str, encoding_layers=3,
                      from_request=True, substring_search=True):
        """Check the cookies portion of the header string for leaks"""
        cookie_str = self.get_cookie_str(header_str, from_request)
        if not cookie_str:
            return list()
        tokens, parameters = self._split_cookie(header_str, from_request=from_request)
        return self._check_whole_and_parts_for_leaks(
            cookie_str, tokens, parameters, encoding_layers, substring_search)

    def check_location_header(self, location_str, encoding_layers=3,
                              substring_search=True):
        """Check the Location HTTP response header for leaks."""
        if location_str == '':
            return list()
        tokens, parameters = self._split_url(location_str)
        return self._check_whole_and_parts_for_leaks(
            location_str, tokens, parameters, encoding_layers,
            substring_search)

    def check_referrer_header(self, header_str, encoding_layers=3,
                              substring_search=True):
        """Check the Referer HTTP request header for leaks."""
        if header_str == '':
            return list()
        referrer_str = self.get_referrer_str(header_str)
        # We use this check instead of ==''
        # since _get_header_str may return None
        if not referrer_str:
            return list()
        tokens, parameters = self._split_url(referrer_str)
        return self._check_whole_and_parts_for_leaks(
            referrer_str, tokens, parameters, encoding_layers,
            substring_search)
    

    def _extract_url_style_payload(self, payload_str, tokens, parameters, seen, depth):
            """
            Extract tokens and named parameters from a URL-style payload.
            Example: en=Scroll_depth&epn.scroll_depth=30&ep.url=https%3A%2F%2Fexample.com
            """
            if depth > 3 or payload_str in seen:
                return
            seen.add(payload_str)

            try:
                pairs = payload_str.split('&')
                for pair in pairs:
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        k = k.strip()
                        v = unquote_plus(v.strip())
                        tokens.add(k)
                        tokens.add(v)
                        parameters.add((k, v))

                        # Recursively extract deeper from values
                        self._split_on_delims(k, tokens, parameters)
                        self._split_on_delims(v, tokens, parameters)

                        # Recurse into value for deeper encoding
                        for enc in LIKELY_ENCODINGS:
                            try:
                                decoded = self._decoder.decode(enc, v)
                                if isinstance(decoded, bytes):
                                    decoded = decoded.decode("utf-8", errors="ignore")
                                decoded = decoded.strip()
                                if decoded and decoded != v:
                                    self._extract_url_style_payload(decoded, tokens, parameters, seen, depth + 1)
                            except Exception:
                                continue
                    else:
                        tokens.add(pair)
            except Exception as e:
                if self._debugging:
                    print(f"Error parsing URL-style payload: {e}")
           
    def _extract_json_array_payload(self, payload_str, tokens, parameters, seen, depth):
        """
        Extract tokens and values from a JSON array-style payload.
        Handles deeply nested arrays.
        """
        if depth > 3 or payload_str in seen:
            return
        seen.add(payload_str)

        try:
            data = json.loads(payload_str)
            if not isinstance(data, list):
                return

            def recurse_array(arr, depth):
                if depth > 3:
                    return
                for item in arr:
                    if isinstance(item, list):
                        recurse_array(item, depth + 1)
                    elif isinstance(item, dict):
                        for k, v in item.items():
                            k = str(k).strip()
                            v = str(v).strip()
                            tokens.add(k)
                            tokens.add(v)
                            parameters.add((k, v))
                            self._split_on_delims(k, tokens, parameters)
                            self._split_on_delims(v, tokens, parameters)
                    elif item is not None:
                        val = str(item).strip()
                        tokens.add(val)
                        self._split_on_delims(val, tokens, parameters)

            recurse_array(data, 0)

        except Exception as e:
            if self._debugging:
                print(f"Error parsing JSON array payload: {e}")
    def _extract_json_object_payload(self, payload_str, tokens, parameters, seen, depth):
        """
        Extract tokens and key-value pairs from a JSON object-style payload.
        Handles deeply nested dictionaries.
        """
        if depth > 3 or payload_str in seen:
            return
        seen.add(payload_str)

        try:
            data = json.loads(payload_str)
            if not isinstance(data, dict):
                return

            def recurse_obj(obj, depth):
                if depth > 3:
                    return
                for k, v in obj.items():
                    k_str = str(k).strip()
                    tokens.add(k_str)

                    if isinstance(v, dict):
                        recurse_obj(v, depth + 1)
                    elif isinstance(v, list):
                        for item in v:
                            if isinstance(item, (dict, list)):
                                recurse_obj(item, depth + 1)
                            else:
                                val = str(item).strip()
                                tokens.add(val)
                                parameters.add((k_str, val))
                                self._split_on_delims(val, tokens, parameters)
                    elif v is not None:
                        val = str(v).strip()
                        tokens.add(val)
                        parameters.add((k_str, val))
                        self._split_on_delims(k_str, tokens, parameters)
                        self._split_on_delims(val, tokens, parameters)

            recurse_obj(data, 0)

        except Exception as e:
            if self._debugging:
                print(f"Error parsing JSON object payload: {e}")
                
    def check_payload(self, payload_str, encoding_layers=3, substring_search=True):
        tokens = set()
        parameters = set()
        seen_payloads = set()
        
        

      #  self._extract_url_style_payload(payload_str, tokens, parameters, seen_payloads, depth=0)
       # self._extract_json_array_payload(payload_str, tokens, parameters, seen_payloads, depth=0)
       # self._extract_json_object_payload(payload_str, tokens, parameters, seen_payloads, depth=0)

        if self._debugging:
            print("Tokens:", tokens)
            print("Parameters:", parameters)

        return self._check_whole_and_parts_for_leaks(
            payload_str, tokens, parameters, encoding_layers, substring_search
        )
           
    def _check_whole_and_parts_for_leaks(self, input_string, tokens,
                                         parameters, encoding_layers,
                                         substring_search):
        """Search an input string and its parts for leaks."""
        results = self._check_parts_for_leaks(tokens, parameters,
                                              encoding_layers)
        if substring_search:
            substr_results = self.substring_search(input_string, max_layers=2)
            # filter repeating results
            return list(set(results + substr_results))
        else:
            return results

    def substring_search(self, input_string, max_layers=None):
        """Do a substring search for all precomputed hashes/encodings

        `max_layers` limits the number of encoding/hashing layers used in the
        substring search (to limit time). The default is no limit (`None`).
        """
        if input_string is None or input_string == '':
            return list()
        try:
            input_string = input_string.encode('utf8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            print(f"ERROR encoding: {repr(input_string)}")
            return list()
        leaks = list()
        for string, transform_stack in self._precompute_pool.items():
            if max_layers and len(transform_stack) > (max_layers + 1):
                continue
            if string.encode('utf-8', errors='ignore') in input_string:
                leaks.append(transform_stack)
        return leaks
    

 


if __name__ == "__main__":
    # Sample value to detect
    secret = "hi_my"

    # Create the leak detector with one known secret string
    detector = LeakDetector(search_strings=[secret], debugging=True)

    # Example URL containing a base64-encoded version of the secret
    import base64
    encoded_secret = base64.b64encode(secret.encode()).decode()
    url = f"https://example.com/profile?token={encoded_secret}&id=123"
    payload= """
    {\"body\":\"eJyVjssKwjAQRf/lrmcRlTZNfiUMJbSRlrS6EAtB+u9OgmjFjV3N484ZjnO1UpUhxB70wNjDmoYww579dAvSRVjHksMigNB1sEpGKbVZmTKvT4SCe9m6zxcvzOKne+YW6YexnVM7XC8BK2/YCMrnm7hkWlX/eaVvr+blpY+HvV7pLVbgH7EE5ic+HlWr\",\"chunk_number\":0,\"encoding\":\"zlib64\",\"request_number\":11,\"token\":\"7KSx1snskTybS6xlHnYNsAfzTHCFoGrMrYtsdcVj/Y3duTy4/64J/4IBCpc1YUAhFbgfC8BZJpZEQ8hD/a/na+/K+BmA8RLjZYPwNB2m\"}
    """
    print("\n=== Checking URL ===")
    leaks = detector.check_url(url)
    leaks_payload = detector.check_payload(payload)
    print("Leaks found in URL:", leaks)
    
    print("Leaks found in Payload:", leaks_payload)