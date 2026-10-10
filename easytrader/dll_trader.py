# coding=utf-8
import json
import os
from ctypes import WinDLL, c_int, c_short, c_float, c_char_p, create_string_buffer


def gbk(text):
    if text is None:
        text = ""
    if isinstance(text, bytes):
        return text
    return str(text).encode("gbk", errors="replace")


def decode(buf):
    return buf.raw.split(b"\x00", 1)[0].decode("gbk", errors="replace")


def parse_tsv(text):
    text = (text or "").strip()
    if not text or "\t" not in text:
        return []
    lines = [line for line in text.split("\n") if line]
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cols = line.split("\t")
        rows.append({header[i] if i < len(header) else str(i): cols[i] if i < len(cols) else "" for i in range(max(len(header), len(cols)))})
    return rows


class ApiTrader(object):
    """Trade through Api.dll. Does not drive a broker desktop client."""

    def __init__(self):
        self.dll = WinDLL(os.environ.get("STOCKAPI_DLL", "Api.dll"))
        self.client_id = -1
        self._bind()
        self.dll.Init()

    def _bind(self):
        d = self.dll
        self.logon = d.Logon
        self.logon.argtypes = [c_char_p, c_short, c_char_p, c_short, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.logon.restype = c_int
        self.logoff = d.Logoff
        self.logoff.argtypes = [c_int]
        self.query = d.QueryData
        self.query.argtypes = [c_int, c_int, c_char_p, c_char_p]
        self.query.restype = c_int
        self.send = d.SendOrder
        self.send.argtypes = [c_int, c_int, c_int, c_char_p, c_char_p, c_float, c_int, c_char_p, c_char_p]
        self.cancel = d.CancelOrder
        self.cancel.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p]
        self.ipo = d.OneClickIpo
        self.ipo.argtypes = [c_int, c_int, c_char_p, c_char_p]
        self.ipo.restype = c_int

    def _bufs(self):
        return create_string_buffer(1024 * 1024), create_string_buffer(256)

    def prepare(self, config_path=None, **kwargs):
        conf = {}
        if isinstance(config_path, dict):
            conf.update(config_path)
        elif config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as handle:
                conf.update(json.load(handle))
        conf.update(kwargs)
        ip = conf.get("ip", conf.get("broker_ip", "YOUR_BROKER_IP"))
        port = int(conf.get("port", 0))
        account = conf.get("account", conf.get("user", "YOUR_ACCOUNT"))
        password = conf.get("password", "YOUR_PASSWORD")
        account_type = conf.get("account_type", 0)
        err = create_string_buffer(256)
        config = '{"account_type":%s}' % account_type
        self.client_id = self.logon(gbk(ip), port, gbk(config), 0, gbk(account), gbk(account), gbk(password), gbk(""), err)
        if self.client_id < 0:
            raise RuntimeError(decode(err) or "Logon failed")
        return self.client_id

    def login(self, user, password, exe_path=None, comm_password=None, **kwargs):
        kwargs.setdefault("account", user)
        kwargs.setdefault("password", password)
        return self.prepare(**kwargs)

    def exit(self):
        if self.client_id >= 0:
            self.logoff(self.client_id)
            self.client_id = -1
        self.dll.UnInit()

    def _query(self, category):
        result, err = self._bufs()
        code = self.query(self.client_id, int(category), result, err)
        if code != 0:
            raise RuntimeError(decode(err) or "QueryData failed")
        return parse_tsv(decode(result))

    def balance(self):
        return self._query(0)

    def position(self):
        return self._query(1)

    def today_entrusts(self):
        return self._query(2)

    def today_trades(self):
        return self._query(3)

    def cancel_entrusts(self):
        return self._query(4)

    def _order(self, security, price, amount, category):
        result, err = self._bufs()
        self.send(self.client_id, int(category), 0, gbk(""), gbk(security), float(price), int(amount), result, err)
        text = decode(err)
        if text:
            raise RuntimeError(text)
        return decode(result)

    def buy(self, security, price, amount, **kwargs):
        return self._order(security, price, amount, 0)

    def sell(self, security, price, amount, **kwargs):
        return self._order(security, price, amount, 1)

    def cancel_entrust(self, entrust_no, exchange_id="1"):
        result, err = self._bufs()
        self.cancel(self.client_id, gbk(exchange_id), gbk(entrust_no), result, err)
        text = decode(err)
        if text:
            raise RuntimeError(text)
        return decode(result)

    def auto_ipo(self):
        result, err = self._bufs()
        code = self.ipo(self.client_id, 0, result, err)
        if code < 0:
            raise RuntimeError(decode(err) or "OneClickIpo failed")
        return decode(result)
