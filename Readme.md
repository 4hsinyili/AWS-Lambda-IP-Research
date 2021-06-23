# AWS Lambdas 是否每次開啟都會用不同的 IP

## 結論：
不會，會是固定的幾組 ip 在輪替（數量不明，已知大於 22 ）， 但每隔一段時間測試都會有些微的差異，所以用 AWS Lambda 與 step function 的組合不能保證你不會因為一直使用同樣的 ip 而被 ban，但可以大幅降低這樣的機率。

## 測試目標：測試 AWS Lambda 是不是每次開啟都會用不同的 IP
如果會的話，爬蟲就不用擔心被抓了。

## 測試結果：不會
* 如果一次只開啟一台 Lambda，那麼在短時間內多次開啟，會使用到相同的 IP。
* 如果一次開啟多台 Lambda （例如使用 step function 的 parallel），那每一台 Lambda 有可能相同。
* 如果一天開啟多次多台 Lambda（例如一天開啟五次相同的 stepfunction），每一次都有機會拿到完全不同的 ip 組合

## 測試方式：
在我的 ec2 / django server 上架設了一個 view ，只要透過網址連到這個 view 的請求，其 IP 都會被 print 出來。接著利用 AWS Lambda 撰寫簡單的 request ，再以 stepfunction 同時或接連執行該 Lambda 。最後複製 print 結果並整理。

我在 step function 中使用了三層 parallel ，依序開啟 8, 12, 16 次 Lambda，每層間隔 0.5 秒。執行了兩次這個 function ，兩次相隔約 15 分鐘

第一次我得到了 10 個唯一（unique）的 ip，第二次我得到了 12 個唯一的 ip，兩次加起來我得到 22 個唯一的 ip。

所以第一次，分三層，總計執行 36 臺 Lambda 中，有 10 個唯一的 ip。第二次則是有 12 個唯一的 ip，而這兩組 ip 完全不同。

因為還有其他的東西要寫所以我就沒有繼續測了，如果有人想討論歡迎找我