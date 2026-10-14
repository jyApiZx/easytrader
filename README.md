# easytrader

# 通达信/同花顺纯协议接口

**产品介绍见 [thsapi.com](https://thsapi.com/)。提供通达信/同花顺纯协议接口，直连券商，无需启动客户端，支持大部分券商。接入请联系 Telegram：`JyApi888`。**

完整函数表和各语言示例见 [stockapi](https://github.com/jyApiZx/stockapi)。

按 easytrader 的 `use` / `buy` / `sell` 写交易代码。`use("api")`、`use("ths")`、`use("miniqmt")` 都登录 `Api.dll`，向券商下单和查询。

不需要打开同花顺客户端，也不需要安装 miniQMT。支持大部分券商的账户，用 DLL 提供的地址和账号登录即可。

## Api.dll

面向 A 股的交易和行情库。

| 能力 | 说明 |
| --- | --- |
| 券商交易 | 登录、资金、持仓、当日委托、当日成交、买入、卖出、撤单、一键打新 |
| A 股行情 | K 线、分时、实时报价 |
| L2 | 十档、逐笔成交、逐笔委托 |

DLL 与函数说明见 [stockapi](https://github.com/jyApiZx/stockapi)。

进程位数须与 `Api.dll` 一致。查询结果为 GBK 文本，行以换行分隔，列以制表符分隔。

## 交易

```python
import easytrader

user = easytrader.use("api")
user.prepare({
    "ip": "YOUR_BROKER_IP",
    "port": 0,
    "account": "YOUR_ACCOUNT",
    "password": "YOUR_PASSWORD",
})

user.balance()
user.position()
user.today_entrusts()
user.today_trades()

user.buy("000001", 10.0, 100)
user.sell("000001", 10.5, 100)
user.cancel_entrust("委托编号", exchange_id="1")  # 1 上海，0 深圳

user.exit()
```

`prepare` 也可以传入同样字段的 JSON 文件路径。

## 说明

调用风格来自 easytrader。下单和查询由 `Api.dll` 完成。雪球、聚宽、米筐的跟单不在本仓库的支持范围内。许可证见 [LICENSE](LICENSE)。
