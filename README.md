# easytrader

按原来的 `use` 写交易。`use("ths")` 仍是同花顺客户端，`use("miniqmt")` 仍是 miniQMT。雪球和其他券商客户端的入口没有改。

客户端下单慢，界面操作也容易漏单、错单。要纯协议直接连券商，用 `use("thsapi")`，加载 `thsapi.dll`。不用把同花顺或通达信客户端开着。下单、撤单和查询走 DLL。

交易包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.2/thsapi_1.0.2_x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.2/thsapi_1.0.2_x32.zip)。调用说明见 [stockapi](https://github.com/jyApiZx/stockapi)。

## 纯协议

```python
import easytrader

user = easytrader.use("thsapi")
user.prepare({
    "ip": "trade.10jqka.com.cn",
    "port": 8002,
    "account": "YOUR_ACCOUNT",
    "password": "YOUR_PASSWORD",
})
user.balance()
```

先用同花顺模拟账户把查询、下单和撤单测好。程序位数要和 `thsapi.dll` 一致。
