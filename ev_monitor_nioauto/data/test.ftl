直接输出字符串：${msg}<br>
截取字符串：${msg?substring(1,4)}<br>
首字母小写：${msg?uncap_first}<br>
首字母大写：${msg?cap_first}<br>
字母转大写：${msg?upper_case}<br>
字母转小写：${msg?lower_case}<br>
字符长度：${msg?length}<br>
是否以H开头：${msg?starts_with("H")?string}<br>
是否以c结尾：${msg?ends_with("c")?string}<br>
获取e的索引：${msg?index_of("e")}<br>
替换字符串：${msg?replace("Hello", "你好")}<br>
输出布尔型：${flag?string("true表示你答对了！","false表示你答错了！")}<br>
输出日期：${createDate?datetime("yyyyMMdd HHmmss")?date}<br>
输出时间：${createDate?datetime("yyyyMMdd HHmmss")?time}<br>
输出日期时间：${createDate?datetime("yyyyMMdd HHmmss")?datetime}<br>
输出格式化的日期时间：${createDate?datetime("yyyyMMdd HHmmss")?string("yyyy年MM月dd日 HH时mm分ss秒")}<br>
数字直接输出：${salary}<br>
数字转为字符串输出：${avg?c}<br>
数字转为货币类型输出：${salary?string.currency}<br>
数字转为百分比类型输出：${avg?string.percent}<br>
浮点数字保留后两位小数：${avg?string["0.##"]}<br>
不存在的字符串显示空：${noExist!}<br>
不存在的字符串显示默认字符串：${noExist!"我是不存在时候的默认值"}<br>
<hr>
<#list stars as star>
    索引：${star?index} - 名字：${star} <br>
</#list>
明星数组长度：${stars?size} <br>
第一个元素：${stars?first} <br>
最后一个元素：${stars?last} <br>
<hr>
<#list cities as city>
    ${city} <br>
</#list>
城市数组长度：${cities?size} <br>
倒序输出：
<#list cities?reverse as city>
    ${city}
</#list>
<br>
升序输出：
<#list cities?sort as city>
    ${city}
</#list>
<br>
降序输出：
<#list cities?sort?reverse as city>
    ${city}
</#list>
<br>
<hr>
逻辑判断：
得分：${score}，
<#if score < 60>
    你个渣渣！
    <#elseif score == 60>
        分不在高，及格就行～
    <#elseif score gt 60 && score lt 80>
        哎呦不错哦！
    <#else>
        你好棒棒哦～
</#if>