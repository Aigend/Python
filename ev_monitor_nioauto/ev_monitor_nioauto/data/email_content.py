# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : email_content.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/18 10:19 上午
# @Description :
import json

from config.settings import BASE_DIR

long_text = """
蔚来ES8
蔚来ES8是蔚来量产车，其中“E”代表“电动”，“S”代表“SUV”，“8”代表性能等级。ES8定位于快速增长的7座SUV市场，面向一二线城市的新生代核心家庭。 [35] 
截至2019年12月31日，蔚来ES8累计交付20,480辆。 [36] 
智能电动旗舰SUV ES8焕新登场。全新ES8搭载160千瓦永磁电机和240千瓦感应电机智能四驱系统，提供544马力，725牛·米的强劲动力，兼顾长续航和高性能。搭载100千瓦时液冷恒温电池包后，全新ES8 NEDC续航达580公里，续航能力全面提升。 [24] 
全新ES8外观在传承之余对蔚来家族设计作出了新的诠释，更锐利、更现代。在内饰的设计和材质提升方面，数字座舱全面升级为9.8英寸超窄边数字仪表盘和11.3英寸高清多点触控中控屏。NOMI Mate 2.0配备汽车行业首个AMOLED全圆屏，显示面积和效果大幅提升。此外，全新ES8还配备了智能充电口盖及NFC卡片式车钥匙等高科技配置。 [24] 
2019年12月28日，全新ES8在NIO DAY 2019正式上市。全新ES8补贴前售价为46.8-53.4万元，签名版车型补贴前指售价为55.8-62.4万元。全新ES8首批车辆预计2020年4月开始交付。 [24] 
ES6采用高强度铝加碳纤维的复合架构，拥有4.7秒零到百公里加速性能，510公里超长综合工况续航里程和33.9米制动距离。ES6延续了蔚来产品家族的设计语言，外观时尚运动，内饰精致而有科技感。 [17] 
ES6分为基准版和性能版。基准版补贴前起售价35.8万元，性能版补贴前起售价39.8万元。ES6采取个性化定制、按订单生产的模式销售，用户即刻可通过蔚来App预订ES6。ES6预计2019年6月起逐步交付。 [17] 
截至2019年12月31日，蔚来ES6累计交付11,433辆。 [36] 
蔚来EC6
蔚来第三款量产车——智能电动轿跑SUV EC6全球首秀。EC6采用轿跑式车身设计，整车风阻系数低至0.27Cd。EC6的一体化穹顶式玻璃车顶，总面积达2.1平方米。EC6性能版搭载前160千瓦永磁电机和240千瓦感应电机，百公里加速仅为4.7秒。搭载100千瓦时液冷恒温电池包的EC6 性能版NEDC续航达到615公里。
7月24日，蔚来智能电动轿跑SUV EC6在2020成都车展正式上市，即日起蔚来App和官网开启选配。首批车辆将在9月下旬开启交付。
蔚来EC6搭载70kWh电池包的运动版车型，补贴前售价为36.8万起；性能版车型，补贴前售价为40.8万起；签名版车型，补贴前售价为46.8万起。
蔚来EC6轿跑式车身设计塑造出兼具动感与优雅的车身比例。蓄势待发的流线型设计让EC6的空气动力学表现尤为突出，风阻系数低至0.26Cd。蔚来EC6配备全景天幕式玻璃天窗，拥有超大的透光面积，同时采用双层隔热玻璃，能量透过率仅为15%，并能隔绝99.5%以上紫外线。
蔚来EC6车身尺寸2.9米长轴距，内饰延续“第二起居室”蔚来EVE概念车的设计理念。
蔚来EC6签名版和性能版搭载前160kW高效能永磁电机+后240kW高性能感应电机组成的双电机智能四驱系统峰值功率544马力，最大扭矩725N·m，造就0-100km/h加速最快4.5秒。运动版则搭载前、后160kW双永磁电机组合，0-100km/h加速可达5.4秒。EC6采用高强度铝合金车身，全系标配CDC动态阻尼控制系统，可选主动式空气悬架，智能识别路况，兼具操控性和舒适性。
蔚来EC6性能版和签名版搭载70kWh电池包，综合工况续航里程最高可达440公里；搭载100kWh电池包，综合工况续航里程最高可达615公里。
蔚来EC6拥有智能化愉悦数字座舱，9.8英寸超窄边数字仪表、11.3英寸高清多点触控中控屏、全圆AMOLED屏的NOMI Mate 2.0共同打造智能、高效、安全、愉悦的交互体验。 [37] 
蔚来EVE
2017年，蔚来发布了概念车EVE。 [1]  4月19日，蔚来携11辆车亮相2017上海国际车展，这是蔚来品牌的中国首秀。量产车蔚来ES8首次揭开面纱，旗舰超跑蔚来EP9开启预售。ES8是一款高性能7座纯电动SUV，计划2017年内正式发布，2018正式开始交付。
蔚来EVE是一个无人驾驶的移动生活空间，以“第二起居室”为设计理念，让用户能够充分享受愉悦自由的出行时间。 [38]  通过全景座舱、智能全息屏幕等交互技术，实现了车与环境、人与环境的融合。伴随着EVE，蔚来同时发布了“NOMI”人工智能伴侣系统。 [38] 
蔚来EP9
2016年，蔚来发布全球最快电动汽车之一的EP9，创造了纽博格林北环等国际知名赛道最快圈速纪录以及最快无人驾驶时速世界纪录。 [1]  11月21日，蔚来在伦敦发布了英文品牌“NIO”、全新Logo、全球最快电动汽车EP9。
作为蔚来的首款产品，EP9在设计上突破界限并打破诸多世界记录，成为电动汽车设计的新标杆。 [39] 
蔚来EP9是一款动力达1360匹马力的电动超跑。2016年10月12日，EP9在德国纽博格林北环赛道创造了7分05秒的电动汽车圈速记录 ，11月4日又以1分52秒的成绩刷新了法国Paul Ricard赛道的电动汽车圈速。 [40] 
蔚来EP9搭载了4台高性能电机以及4个独立变速箱，能够输出1,360匹马力的强劲动力，0到200公里加速7.1秒，极速313KPH。EP9采用弹匣式可换电池系统，快充模式下充满电仅需45分钟，续航里程可达427公里。EP9 搭载了 DRS可调扰流控制系统，包括采用了三种可调模式的动态尾翼系统和全尺寸底盘扩散器等空气动力装置，使得EP9在每小时240公里的速度下能够获得高达24,000牛的下压力 。 [41] 
EP9应用前瞻性的整车电控架构及传感器系统布局，可以适用新的无人驾驶技术。同时EP9应用了蔚来“Know-Me”人性化交互设计理念。 [40] 
进入2017年，蔚来EP9继续在世界各大著名赛道上展现实力：
2017年2月23日，无人驾驶版EP9在得克萨斯美洲赛道(Circuit of the Americas)创造了每小时257公里的速度纪录。 [42] 
2017年2月23日，EP9在得克萨斯美洲赛道(Circuit of the Americas)以2分11秒的成绩打破了此前由迈凯轮P1所保持的2分17秒量产车圈速纪录。 [42] 
2017年3月16日，EP9在上海国际赛车场以2分01秒的成绩创造了该赛道量产车圈速纪录。该成绩较此前由奔驰SLS AMG所保持的圈速提升了24秒。
2017年5月12日，EP9在德国纽博格林北环赛道以6分45秒90的成绩创造了该赛道当时的历史圈速纪录。
"""
textlen = len(long_text)
text_list = list([i for i in long_text])
num = 500
if textlen >= num:
    long_text = long_text[:num]
else:
    long_text = long_text + long_text[0] * (num - textlen)

html5 = '''
        <!DOCTYPE html>
<html lang="zh-cn">	
<head>
	<meta charset="uth-8">
	<title>[title]</title>
</head>
<body>
<div>
[title]姓名：[name]日期：[date]车型：[mode_type]

</div>
<a href="https://cdn-app-test.nio.com/account-center/2021/7/5/8764ed97-1930-49f0-a772-9206028c1e0c.jpeg">图片</a>
<a href="https://nio.feishu.cn/docs/doccnKq4vB0QCXr4wbKWz3LYHEf">飞书云文档</a>
<a href="https://confluence.nioint.com/pages/viewpage.action?pageId=74090751">confluence云文档</a>
<img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fm2.auto.itc.cn%2Flogo%2Fmodel%2F5293.jpg&refer=http%3A%2F%2Fm2.auto.itc.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1616643382&t=02342741d3d105721e812dfe4f2a6adb" alt="[mode_type][date]" />
</body>
</html>	
        '''

html5_new = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      body {
        margin: 0;
      }
      a {
        background-color: transparent;
      }
      .main {
        width: 100vw;
        min-height: 100vh;
        box-sizing: border-box;
        overflow-x: hidden;
        overflow-y: auto;
      }
      .header .icon {
        display: inline-block;
        margin: 40px 0 0 50px;
        width: 51px;
        height: 48px;
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADMAAAAzCAMAAAANf8AYAAABklBMVEUAAAD////////////9/f3///////+boaSCiY11fYDv7+/9//////////91foGGjZACERhJVFl6goe/xMWOlZkLGiF3gIOKkZSus7UjMDaqrrJxen+WnJ+boaSus7V+h4t1foGqsLLW2trS1daZoKOUmp35+fmiqatRXWD///+ip6rm5+j///+2vL7n5+f4+Pj////k5OT///+kqqyVnJ86Rkuhpqqeo6Z1foHZ3N3U2NmHj5OIj5OUmp5+hom4vb+gpqmboqWrsLSusrV6g4d1foGjqKs6R0uSmZw7RkzCx8iwtbitsrWqsLOrsbTFysq4v8C1ur3BxsersLLEyMqnra/4+Pj19/dwen3Jzs5yfYDx8fTm5ujj5ub////y8vLZ3Nzz8/OqrrKZoaX7+/vs7Oz////z8/MADxYDEhkKGSAIFx4FFBs/S1A3Q0kzP0URHyZFUFYjMDYaKC4UIin19vbX2tu3vL6NlJd1foFlb3MrOD4mMzkVIyoPHiS/w8W9wcOHj5J9hYlZY2hSXWFIU1iHqF09AAAAaHRSTlMAAwQBFzoKvLW1Px0QCP319PLs4+Dg1czLy8rJxsW/u7u6tLSsq6iVkI2LY1U8KSMTEg36+vby8uvp4uLa0NDMzMrGxMTEvLi2trGvr6+to5+Xk46Gf2dkZGNgW1paTk5JQkJBNzcqFcotOKUAAAIVSURBVEjH5ZRlc9tAEIalOzltDYGGoZA2DG2TMjMzhRlXUswOM/3vjOJEd3sr25rJxzwf951ndHpv57RzgD7fPdT2ubaysvZj20C3oRcWZpoPbZCwk5+CLK8xXpIBQqJkOPfHQs8S4Eni6W1vg3dGISfRTu51rl+bkIf0H06VZsiP2cpV5bsJhaTfivTPhoJYg0iZSIAPNm9Jyp04+OJ+RLT8CnzS6jqTab9O+vRu9cukoujKztLS9kqSlPnipLug2tnBky6Dcc6Mrsf7ancnNTzHY/tBgLvXNnbXwmnT8bwXl2aWF2lypeULKI4dp0FA3AtriN6HOJ91hh14gQOawlwSZP47s3o0+qIRfoJMvTMqQ8cNUScUA4kyZ5SSJxWcOrwCJFLOKCP3PKJ5MCpfYMaZiC6t+HLYywkvxyx3IxaUkL1cN4FgbtTkfq1YnTCw9ZrlUt4gBXGFeStvxZ/5lNhVpBAuUEknCpF0VWkU/+JT0n9QhdKEpL9U2dqiUoekTFFlbXFxjUrT4mSlJFxtj0TaV8m41D1dj6VmxQFnHihW53aPezW7SvTIyAaG+ortiUvq20BJlfuKFFWhINUvVX1DPt17JhL2Tgqsm3LZrEYk1xlaqWsiqWN426pdRVc2xJWqmbqiDdk7uqSTTbyYVRoY3etGSyhUsj8IRS4ijhQkrYvfx1HLNxHg5GuLSJRIBDQ5E0cfkg/aDzYqjAAAAABJRU5ErkJggg==');
      }
      .header .left-hint {
        display: inline-block;
        margin: 40px 0 0 calc(100% - 341px);
        height: 46px;
        font-size: 14px;
        font-family: BlueSkyStandard-Regular, BlueSkyStandard;
        font-weight: 400;
        color: rgba(0, 15, 22, 1);
        line-height: 22px;
        letter-spacing: 3px;
        background-color: #fff;
      }
      .title {
        font-size: 60px;
        font-family: BlueSkyStandard-Light, BlueSkyStandard;
        font-weight: 300;
        color: rgba(0, 15, 22, 1);
        line-height: 80px;
        margin: 145px 50px 57px;
        background-color: #fff;
      }
      .content {
        min-height: calc(100vh - 782px);
        width: 100%;
        background-color: #f0f2f5;
      }
      .content .pic {
        width: 88.3%;
        margin: 0 auto;
      }

      .content .pic img {
        width: 100%;
      }
      .hi-title {
        font-size: 40px;
        font-family: BlueSkyStandard-Light, BlueSkyStandard;
        font-weight: 300;
        color: rgba(0, 15, 22, 1);
        line-height: 56px;
        padding: 60px 40px 20px;
      }
      .hi-content {
        font-size: 22px;
        font-family: BlueSkyStandard-Light, BlueSkyStandard;
        font-weight: 300;
        color: rgba(0, 15, 22, 1);
        line-height: 30px;
        padding: 0 40px 60px;
      }
      .confirm-btn {
        width: 240px;
        height: 44px;
        box-sizing: border-box;
        background: rgba(0, 190, 190, 1);
        margin: 0 40px 40px 40px;
        font-size: 14px;
        font-family: BlueSkyStandard-Regular, BlueSkyStandard;
        font-weight: 400;
        color: rgba(255, 255, 255, 1);
        line-height: 17px;
        letter-spacing: 3px;
      }

      .confirm-btn a {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: rgba(255, 255, 255, 1) !important;
        text-decoration: none;
      }

      .hi-ending {
        margin: 0 40px 59px;
        font-size: 22px;
        font-family: BlueSkyStandard-Light, BlueSkyStandard;
        font-weight: 300;
        color: rgba(0, 15, 22, 1);
        line-height: 32px;
      }

      .hi-note {
        font-size: 22px;
        font-family: BlueSkyStandard-Light, BlueSkyStandard;
        font-weight: 300;
        color: rgba(0, 15, 22, 1);
        line-height: 32px;
        padding: 0 40px 60px;
      }
      .footer {
        width: 100%;
        height: 323px;
        background: rgba(0, 15, 22, 1);
      }
      .footer-top-part {
        padding-top: 35px;
      }
      .footer .icon {
        display: inline-block;
        margin: 5px 0 55px 40px;
        width: 111px;
        height: 39px;
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG8AAAAnCAMAAAA2EOZTAAAAvVBMVEUADxb///+kqavZ29xnb3QCEBd/hopaY2guO0DR09T19fXm5+jBxMYFExufpKf9/f1SXGD39/cmMjgIFh37+/sWIyrd39/FyMqxtbeNk5ZtdXlFT1Q2QUcbKC4RHyUNGyK3u71gaW0qNjz5+fnt7u7h4uNAS1AyPkMiLjTj5OW8wMGKkJRweHxLVVpCTVI5RErz8/Tx8fLIy8yboKOFjI97goZze39IUlfU1tfNz9GprrBXYGVOWV6Ump1qcnbpw9aWAAACv0lEQVRYw8XXaVeyQBiA4ecBMTdEWQQVRFxSMzMr2+v//6w3GB1mw855D5yuT4TprTMwo/DHokTr6Iv+8iE4hgZUzLltImPxaEOFnOc2ClytumI4QAX3GapxO0e1YAIV0LDQIILSDfGCZlz6YOJFHRNKdWfhZY9QJvMVf2GFwJr1er1PG3LO7udMlL5UerCm5ydXmj9oTp/4p4/wVz6w6tl7OAI1TU9cAcB7elA717Z9egm8ADVZIEs/hl5sJwE/xld8L5PQE+3zv+hMb88tH11T+fEOiQHEzEfGm6Lnji/1dn3honOA6GBuaTPT2kXGWu7hoVHca9yjQIOMxwzcfQMY5g3mnhU9bEdFPaN5Wiy2tZHWYuekJr5ozmsh9aDq4Wtc0EvIiG+zWbN90s7+eERq4wBvi9Rc2cMbU917wNQ3EAYJfpJrmaqDYI05T+j181mRe5GVvRk4s7OR6qaHzBY7A9EbUg2h1/ki559UvU9MjYX94DU9onefWwfJfkl7O7FnBOSBmqJHLopYWFMW2YV7MpuE07cmzz+a6/PjE7EHDpkkdyf3yAZgCr0WsMYtlGkGUGIPvAG5i1ZS74PMjzCeA2Bc5zk5qO6BTSajfRB7Kzq1hLPBH1Mxpw4W92BPn8X3yAjPG/x+PpJy6mBxD3qWokcD+ik4srJ8JOfUweIe3Kp73oGsEk8zMx6f1sVhvsHLOTmo7sFQ2YNvFC0nRTl9aonB4p7xLvfydVLeC+QbQTOh1xeDhT1wfGXP4L/zbVb8t4FcN33tFz7orqVekH9B0MUe8ZEvTta7B9TMFXNScAisjyAI2F8WXl37sU83lPTgjn7y2s08+2xfK2ANhZwU3MTwn5z1fuWBwPT5HDGmwX4I5YraNKdaUBMom72kOSlojaB8kc7n8hvTTaAKcZfmuFV8EEJFrg2QrWIo1T/TQTKEl7wTYwAAAABJRU5ErkJggg==');
      }
      .footer .icon-350 {
        display: none;
      }
      .footer .links {
        display: inline-block;
        margin-left: calc(61% - 151px);
        font-size: 14px;
        font-family: BlueSkyStandard-Regular, BlueSkyStandard;
        font-weight: 400;
        color: rgba(255, 255, 255, 1);
        line-height: 24px;
        letter-spacing: 3px;
      }
      .footer .links a, .contact-link {
        color: rgba(255, 255, 255, 1) !important;
        text-decoration: none;
      }
      .contact-link {
        text-decoration: underline;
        font-weight: bold;
      }
      .footer .right {
        width: 75px;
        margin: -18px calc(39% - 86px) 0 auto;
        font-size: 14px;
        font-family: BlueSkyStandard-Light, BlueSkyStandard;
        font-weight: 300;
        color: rgba(255, 255, 255, 1);
        line-height: 18px;
      }
      .footer .note {
        margin: 5px 0 0 40px;
        width: 40%;
        font-size: 14px;
        font-family: BlueSkyStandard-LightItalic, BlueSkyStandard;
        font-weight: normal;
        line-height: 18px;
        color: rgba(255, 255, 255, 1);
      }
      .question {
        margin-bottom: 30px;
      }
      @media (min-width: 843px) {
        .content {
          min-height: calc(100vh - 712px);
        }
      }
      @media (max-width: 410px) and (min-width: 350px) {
        .title {
          word-break: break-all;
        }
      }
      @media (max-width: 350px) {
        .header .icon {
          margin: 20px 0 0 20px;
        }
        .header .left-hint {
          margin: 20px 0 0 calc(100% - 251px);
          width: 140px;
          font-size: 10px;
          line-height: 16px;
          letter-spacing: 2px;
        }
        .content {
          min-height: calc(100vh - 871px);
        }
        .title {
          margin: 90px 20px 41px;
          font-size: 40px;
          line-height: 56px;
        }
        .hi-title {
          padding: 30px 20px 10px;
          font-size: 24px;
          line-height: 34px;
        }
        .hi-content {
          padding: 0 20px 40px;
          font-size: 16px;
          line-height: 22px;
        }
        .confirm-btn {
          width: auto;
          margin: 0 20px 40px;
        }
        .confirm-btn a {
          font-size: 14px;
          line-height: 17px;
          letter-spacing: 3px;
        }
        .hi-ending {
          font-size: 16px;
          line-height: 22px;
          margin: 0 20px 40px;
        }
        .hi-note {
          font-size: 16px;
          line-height: 22px;
          padding: 0 20px 60px;
        }
        .footer {
          height: 555px;
        }
        .footer .links {
          font-size: 14px;
          line-height: 40px;
          letter-spacing: 3px;
          margin: 20px 0 0 20px;
          margin-left: 20px;
        }
        .footer .icon {
          margin: 80px 0 0 20px;
        }
        .footer .icon-350 {
          display: block;
        }
        .footer .icon-600 {
          display: none;
        }
        .footer .note {
          margin: 25px 0 0 20px;
          width: 80%;
          font-size: 14px;
          line-height: 18px;
        }
        .footer .right {
          margin: 40px 0 0 20px;
        }
        .question {
          margin-bottom: 15px;
        }
      }
    </style>
  </head>
  <body>
    <div class="main">
      <div class="header">
        <div class="icon"></div>
        <div class="left-hint">
          EUROPEAN EDITION<br />
          MONTH YEAR
        </div>
      </div>
      <div class="title">Confirm Your subscription</div>
      <div class="content">
        <div class="pic">
          <img
          src="data:image/png;base64,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"
          />
        </div>
        <div class="hi-title">Hi {{user_name}}</div>
        <div class="hi-content">
          Please confirm your subscription to our NIO Newsletter by clicking the
          link below.
        </div>
        <div class="confirm-btn">
          <a href="{{confirm_url}}" target="_blank" rel="noopener noreferrer"
            >CONFIRM</a
          >
        </div>
        <div class="hi-ending">
          We hope you enjoy reading,<br />
          Your NIO Team
        </div>
        <div class="hi-note">
          Important note: To ensure that our NIO newsletter actually reaches you
          and does not end up in the spam filter, please enter our sender
          address book of your email program.
        </div>
      </div>
      <div class="footer">
        <div class="footer-top-part">
          <div class="icon icon-600"></div>
          <div class="links">
            <a
              href="https://www.nio.com"
              target="_blank"
              rel="noopener noreferrer"
              >NIO.COM</a
            ><br />
            <a
              href="https://www.instagram.com/nioglobal/"
              target="_blank"
              rel="noopener noreferrer"
              >INSTAGRAM</a
            ><br />
            <a
              href="https://twitter.com/NIOGlobal"
              target="_blank"
              rel="noopener noreferrer"
              >TWITTER</a
            ><br />
            <a
              href="https://www.facebook.com/NIOGlobal/"
              target="_blank"
              rel="noopener noreferrer"
              >Facebook</a
            ><br />
          </div>
          <div class="icon icon-350"></div>
        </div>
        <div class="note">
          <div class="question">
            <div class="item">Have a question?</div>
            <a href="{{contact_url}}" class="contact-link" target="_blank" rel="noopener noreferrer">Contact Us</a>
          </div>
          <div class="address">
            <div class="item">NIO Norway AS</div>
            <div class="item">Karl Johansgate 33</div>
            <div class="item">0162 Oslo Norway </div>
          </div>
        </div>
        <div class="right">© NIO 2021</div>
      </div>
    </div>
  </body>
</html>
"""

H5_R_L = """
    <!doctype html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
      <head>
        <title>
          
        </title>
        <!--[if !mso]><!-->
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <!--<![endif]-->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style type="text/css">
          #outlook a { padding:0; }
          body { margin:0;padding:0;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%; }
          table, td { border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt; }
          img { border:0;height:auto;line-height:100%; outline:none;text-decoration:none;-ms-interpolation-mode:bicubic; }
          p { display:block;margin:13px 0; }
        </style>
        <!--[if mso]>
        <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
        <!--[if lte mso 11]>
        <style type="text/css">
          .mj-outlook-group-fix { width:100% !important; }
        </style>
        <![endif]-->
        
        
    <style type="text/css">
      @media only screen and (min-width:480px) {
        .mj-column-per-100 { width:100% !important; max-width: 100%; }
.mj-column-per-33-333333333333336 { width:33.333333333333336% !important; max-width: 33.333333333333336%; }
      }
    </style>
    <style media="screen and (min-width:480px)">
      .moz-text-html .mj-column-per-100 { width:100% !important; max-width: 100%; }
.moz-text-html .mj-column-per-33-333333333333336 { width:33.333333333333336% !important; max-width: 33.333333333333336%; }
    </style>
  
        <style type="text/css">
        
        

    @media only screen and (max-width:480px) {
      table.mj-full-width-mobile { width: 100% !important; }
      td.mj-full-width-mobile { width: auto !important; }
    }
  

      noinput.mj-menu-checkbox { display:block!important; max-height:none!important; visibility:visible!important; }

      @media only screen and (max-width:480px) {
        .mj-menu-checkbox[type="checkbox"] ~ .mj-inline-links { display:none!important; }
        .mj-menu-checkbox[type="checkbox"]:checked ~ .mj-inline-links,
        .mj-menu-checkbox[type="checkbox"] ~ .mj-menu-trigger { display:block!important; max-width:none!important; max-height:none!important; font-size:inherit!important; }
        .mj-menu-checkbox[type="checkbox"] ~ .mj-inline-links > a { display:block!important; }
        .mj-menu-checkbox[type="checkbox"]:checked ~ .mj-menu-trigger .mj-menu-icon-close { display:block!important; }
        .mj-menu-checkbox[type="checkbox"]:checked ~ .mj-menu-trigger .mj-menu-icon-open { display:none!important; }
      }
    
        </style>
        <style type="text/css">@media all and (max-width: 480px) {</style>
        
      </head>
      <body style="min-width: 300px; word-spacing: normal;">
        
        
      <div style>
        
      
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div style="margin:0px auto;max-width:600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
            
      <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">模板测试,公共变量用户名[*user_name*]，公共变量[*city*]</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">邮件测试自定义变量[#date#],变量[#time#],变量[#age#][#dist#]</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div style="margin:0px auto;max-width:600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:200px;" ><![endif]-->
            
      <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">[#picture#]1</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
        <tbody>
          <tr>
            <td style="width:150px;">
              
      <img height="auto" src="https://cdn-app-test.nio.com/account-center/2021/8/25/25a2fcf9-2842-4535-8ea0-f1f9a94b2de3.jpeg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="150">
    
            </td>
          </tr>
        </tbody>
      </table>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:200px;" ><![endif]-->
            
      <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">[#picture#]2</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
        <tbody>
          <tr>
            <td style="width:150px;">
              
      <img height="auto" src="https://cdn-app-test.nio.com/account-center/2021/8/25/25a2fcf9-2842-4535-8ea0-f1f9a94b2de3.jpeg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="150">
    
            </td>
          </tr>
        </tbody>
      </table>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:200px;" ><![endif]-->
            
      <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">[#picture#]3</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
        <tbody>
          <tr>
            <td style="width:150px;">
              
      <img height="auto" src="https://cdn-app-test.nio.com/account-center/2021/8/25/25a2fcf9-2842-4535-8ea0-f1f9a94b2de3.jpeg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="150">
    
            </td>
          </tr>
        </tbody>
      </table>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div style="margin:0px auto;max-width:600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
            
      <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td style="font-size:0px;word-break:break-word;">
                  
      <div style="height:20px;line-height:20px;">&#8202;</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <p style="border-top:solid 4px #000000;font-size:1px;margin:0px auto;width:100%;">
      </p>
      
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 4px #000000;font-size:1px;margin:0px auto;width:550px;" role="presentation" width="550px" ><tr><td style="height:0;line-height:0;"> &nbsp;
</td></tr></table><![endif]-->
    
    
                </td>
              </tr>
            
              <tr>
                <td align="center" style="font-size:0px;word-break:break-word;">
                  
        
        <div class="mj-inline-links" style>
        
    <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr><td style="padding:15px 10px;" class="" ><![endif]-->
  
        
      <a class="mj-link" target="_blank" style="display:inline-block;color:#000000;font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;font-weight:normal;line-height:22px;text-decoration:none;text-transform:uppercase;padding:15px 10px;">
        Link 1
      </a>
    
        
    <!--[if mso | IE]></td><td style="padding:15px 10px;" class="" ><![endif]-->
  
        
      <a class="mj-link" target="_blank" style="display:inline-block;color:#000000;font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;font-weight:normal;line-height:22px;text-decoration:none;text-transform:uppercase;padding:15px 10px;">
        Getting started
      </a>
    
        
    <!--[if mso | IE]></td><td style="padding:15px 10px;" class="" ><![endif]-->
  
        
      <a class="mj-link" target="_blank" style="display:inline-block;color:#000000;font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;font-weight:normal;line-height:22px;text-decoration:none;text-transform:uppercase;padding:15px 10px;">
        Try it live
      </a>
    
        
    <!--[if mso | IE]></td><td style="padding:15px 10px;" class="" ><![endif]-->
  
        
      <a class="mj-link" target="_blank" style="display:inline-block;color:#000000;font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;font-weight:normal;line-height:22px;text-decoration:none;text-transform:uppercase;padding:15px 10px;">
        Templates
      </a>
    
        
    <!--[if mso | IE]></td><td style="padding:15px 10px;" class="" ><![endif]-->
  
        
      <a class="mj-link" target="_blank" style="display:inline-block;color:#000000;font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;font-weight:normal;line-height:22px;text-decoration:none;text-transform:uppercase;padding:15px 10px;">
        Components
      </a>
    
        
    <!--[if mso | IE]></td></tr></table><![endif]-->
  
        </div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Content 1</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="content-outlook" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div class="content" style="margin:0px auto;max-width:600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
            
      <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
        <tbody>
          <tr>
            <td style="width:550px;">
              
      <img height="auto" src="https://d1pfnb75kyosdp.cloudfront.net/images/mail-templates/confirmImage.png" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="550">
    
            </td>
          </tr>
        </tbody>
      </table>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" class="hi-title" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Hi [#user_name#]</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" class="hi-content" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Thank you for your application to NIO Norway's User Advisory Board. We greatly appreciate your commitment to NIO Norway.</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" vertical-align="middle" class="confirm-btn" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
        <tr>
          <td align="center" bgcolor="#414141" role="presentation" style="border:none;border-radius:3px;cursor:auto;mso-padding-alt:10px 25px;background:#414141;" valign="middle">
            <a href="[#confirm_url#]" style="display:inline-block;background:#414141;color:#ffffff;font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;font-weight:normal;line-height:120%;margin:0;text-decoration:none;text-transform:none;padding:10px 25px;mso-padding-alt:0px;border-radius:3px;" target="_blank">
              CONFIRM
            </a>
          </td>
        </tr>
      </table>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" class="hi-note hi-sign" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">We will contact you if you are selected to participate in the panel.</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" class="hi-note" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">In the meantime, we hope you want to be part of our community, and follow us on social media.</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" class="hi-note" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Facebook and Instagram: @NIONorge</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><![endif]-->
    
    
      </div>
    
      </body>
    </html>
"""

html5_new1 = """
    <!doctype html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
      <head>
        <title>
          
        </title>
        <!--[if !mso]><!-->
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <!--<![endif]-->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style type="text/css">
          #outlook a { padding:0; }
          body { margin:0;padding:0;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%; }
          table, td { border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt; }
          img { border:0;height:auto;line-height:100%; outline:none;text-decoration:none;-ms-interpolation-mode:bicubic; }
          p { display:block;margin:13px 0; }
        </style>
        <!--[if mso]>
        <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
        <!--[if lte mso 11]>
        <style type="text/css">
          .mj-outlook-group-fix { width:100% !important; }
        </style>
        <![endif]-->
        
        
    <style type="text/css">
      @media only screen and (min-width:480px) {
        .mj-column-per-100 { width:100% !important; max-width: 100%; }
.mj-column-per-50 { width:50% !important; max-width: 50%; }
.mj-column-per-33-333333333333336 { width:33.333333333333336% !important; max-width: 33.333333333333336%; }
      }
    </style>
    <style media="screen and (min-width:480px)">
      .moz-text-html .mj-column-per-100 { width:100% !important; max-width: 100%; }
.moz-text-html .mj-column-per-50 { width:50% !important; max-width: 50%; }
.moz-text-html .mj-column-per-33-333333333333336 { width:33.333333333333336% !important; max-width: 33.333333333333336%; }
    </style>
  
        <style type="text/css">
        
        

    @media only screen and (max-width:480px) {
      table.mj-full-width-mobile { width: 100% !important; }
      td.mj-full-width-mobile { width: auto !important; }
    }
  
        </style>
        <style type="text/css">@media all and (max-width: 480px) {
  .title div {
    font-size: 40px !important;
    line-height: 56px !important;
  }

  .left-hint div {
    font-size: 10px !important;
    line-height: 16px !important;
    letter-spacing: 2px !important;
  }
  .hi-title div {
    font-size: 24px !important;
    line-height: 34px !important;
  }
  .hi-content div {
    font-size: 16px !important;
    line-height: 22px !important;
  }

  .confirm-btn a {
    font-size: 14px !important;
  }
  .hi-note div {
    font-size: 16px !important;
    line-height: 22px !important;
  }

  .links * {
    background: transparent !important;
    text-align: left !important;
  }

  .footer-icon img {
    margin: 60px 0 40px;
  }
  .links a {
    font-size: 14px !important;
  }
  .footer-note div {
    font-size: 14px !important;
    line-height: 18px !important;
  }
  .footer .right div {
    text-align: left !important;
  }
}</style>
        
      </head>
      <body style="word-spacing: normal; min-width: 300px;">
        
        
      <div style>
        
      
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="header-outlook" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div class="header" style="background-color: #ffffff; margin: 0px auto; max-width: 600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="width:600px;" ><![endif]-->
            
      <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0;line-height:0;text-align:left;display:inline-block;width:100%;direction:ltr;">
        <!--[if mso | IE]><table border="0" cellpadding="0" cellspacing="0" role="presentation" ><tr><td style="vertical-align:top;width:300px;" ><![endif]-->
                
      <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:50%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" class="icon" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
        <tbody>
          <tr>
            <td style="width:250px;">
              
      <img height="48" src="https://d1pfnb75kyosdp.cloudfront.net/images/mail-templates/topIcon.png" style="border: 0; display: block; outline: none; text-decoration: none; font-size: 13px; width: 51px; height: 48px;" width="51">
    
            </td>
          </tr>
        </tbody>
      </table>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
              <!--[if mso | IE]></td><td style="vertical-align:top;width:300px;" ><![endif]-->
                
      <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:50%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" class="left-hint" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="letter-spacing: 3px; word-break: break-word; height: 46px; line-height: 22px; font-size: 14px; font-family: BlueSkyStandard-Regular, BlueSkyStandard, Helvetica Neue,
    Helvetica, Arial, PingFang SC, Hiragino Sans GB, Heiti SC, Microsoft YaHei,
    WenQuanYi Micro Hei, sans-serif; font-weight: 400; color: rgba(0, 15, 22, 1); text-align: right;">NIO NORGE <br> [#month#] [#year#]</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
              <!--[if mso | IE]></td></tr></table><![endif]-->
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div style="margin:0px auto;max-width:600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:200px;" ><![endif]-->
            
      <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Content 1</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:200px;" ><![endif]-->
            
      <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Content 2</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td><td class="" style="vertical-align:top;width:200px;" ><![endif]-->
            
      <div class="mj-column-per-33-333333333333336 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Content 3</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
    
      
      <div style="margin:0px auto;max-width:600px;">
        
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
            
      <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
        
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
        <tbody>
          
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Content 1</div>
    
                </td>
              </tr>
            
              <tr>
                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                  
      <div style="font-family:BlueSkyStandard-Regular, BlueSkyStandard;font-size:13px;line-height:1;text-align:left;color:#000000;">Insert text here</div>
    
                </td>
              </tr>
            
        </tbody>
      </table>
    
      </div>
    
          <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
        
      </div>
    
      
      <!--[if mso | IE]></td></tr></table><![endif]-->
    
    
      </div>
    
      </body>
    </html>
"""

# 参考https://www.jianshu.com/p/191d1e21f7ed f"![图片tiff](img_v2_1c8e5d03-9a41-4c30-a7bf-6483a99c6e1g)\n" \
markdown_file_title = f"标题\n# 这是一级标题\n## 这是二级标题\n### 这是三级标题\n#### 这是四级标题\n##### 这是五级标题\n###### 这是六级标题\n"
markdown_file_font = f"字体\n**这是加粗的文字**\n*这是倾斜的文字*`\n***这是斜体加粗的文字***\n~~这是加删除线的文字~~\n"
markdown_file_url = f"链接\n>这是引用的内容\n>>这是引用的内容\n>>>>>>>>>>这是引用的内容\n[简书](http://jianshu.com)\n[百度](http://baidu.com)\n"
markdown_file_img = f"图片![blockchain](img_v2_1cff331e-d60e-4433-95fd-cac62b41b64g)\n" \
                    f"![图片gif](img_v2_fe42028a-9ebf-477f-bf97-4c95b0eb22eg)\n" \
                    f"![图片bmp](img_v2_86d56f8a-fc30-4553-9f4b-3b0201b14afg)\n" \
                    f"![图片jpeg](img_v2_ce6c6c62-2f15-4037-8524-fcae137374eg)\n" \
                    f"![图片png](img_v2_143c32b9-f08b-4788-b2ae-e55801c3af2g)\n" \
                    f"![图片jpg](img_v2_6951c0d9-7907-4535-aa74-dbdf7349c42g)\n" \
                    f"![图片webp](img_v2_5f4ed7db-e885-4f9c-9463-9dbec645196g)\n"
markdown_file_form = f"表格式\n姓名|技能|排行\n--|:--:|--:\n刘备|哭|大哥\n关羽|打|二哥\n张飞|骂|三弟\n"
markdown_file_emoji = f"标准emoji\n😁😢🌞💼🏆❌✅\n"

fei_shu_card = json.dumps({
    "config": {
        "wide_screen_mode": True
    },
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "markdown",
                "content": "普通文本\n标准emoji 😁😢🌞💼🏆❌✅\n*斜体*\n**粗体**\n~~删除线~~\n[文字链接](https://www.feishu.cn)\n[差异化跳转（桌面端和移动配置不同跳转链接）]($urlVal)\n<at id=all></at>",
                "href": {
                    "urlVal": {
                        "url": "https://www.feishu.com",
                        "android_url": "https://developer.android.com/",
                        "ios_url": "lark://msgcard/unsupported_action",
                        "pc_url": "https://www.feishu.com"
                    }
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "主按钮"
                        },
                        "type": "primary"
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "次按钮"
                        },
                        "type": "default"
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "危险按钮"
                        },
                        "type": "danger"
                    }
                ]
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "深度整合使用率极高的办公工具，企业成员在一处即可实现高效沟通与协作。"
                },
                "extra": {
                    "tag": "img",
                    "img_key": "img_e344c476-1e58-4492-b40d-7dcffe9d6dfg",
                    "alt": {
                        "tag": "plain_text",
                        "content": "图片"
                    }
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "在移动端同样进行便捷的沟通、互动与协作，手机电脑随时随地保持同步。"
                },
                "extra": {
                    "tag": "select_static",
                    "placeholder": {
                        "tag": "plain_text",
                        "content": "默认提示文本"
                    },
                    "value": {
                        "key": "value"
                    },
                    "options": [
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "选项1"
                            },
                            "value": "1"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "选项2"
                            },
                            "value": "2"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "选项3"
                            },
                            "value": "3"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "选项4"
                            },
                            "value": "4"
                        }
                    ]
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "ISV产品接入及企业自主开发，更好地对接现有系统，满足不同组织的需求。"
                },
                "extra": {
                    "tag": "overflow",
                    "options": [
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "打开飞书应用目录"
                            },
                            "value": "appStore",
                            "url": "https://app.feishu.cn"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "打开飞书开发文档"
                            },
                            "value": "document",
                            "url": "https://open.feishu.cn"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "打开飞书官网"
                            },
                            "value": "document",
                            "url": "https://www.feishu.cn"
                        }
                    ]
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "国际权威安全认证与信息安全管理体系，为企业提供全生命周期安全保障。"
                },
                "extra": {
                    "tag": "date_picker",
                    "placeholder": {
                        "tag": "plain_text",
                        "content": "请选择日期"
                    },
                    "initial_date": "2020-9-20"
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "img",
                        "img_key": "img_e344c476-1e58-4492-b40d-7dcffe9d6dfg",
                        "alt": {
                            "tag": "plain_text",
                            "content": "Image"
                        }
                    },
                    {
                        "tag": "plain_text",
                        "content": "Notes"
                    }
                ]
            }
        ],
        "en_us": [
            {
                "tag": "markdown",
                "content": "Normal text\nStandard emoji 😁😢🌞💼🏆❌✅\n*italic*\n**bold**\n~~strikethrough~~\n[Differentiated Jump (Desktop and mobile configurations are different jump links)]($urlVal)\n[Text link](https://feishu.cn)\n<at id=all></at>",
                "href": {
                    "urlVal": {
                        "url": "https://www.feishu.com",
                        "android_url": "https://developer.android.com/",
                        "ios_url": "lark://msgcard/unsupported_action",
                        "pc_url": "https://www.feishu.com"
                    }
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "Primary Button"
                        },
                        "type": "primary"
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "Secondary Button"
                        },
                        "type": "default"
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "Danger Button"
                        },
                        "type": "danger"
                    }
                ]
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "Feishu interconnects many essential collaboration tools in a single platform. Always in sync, and easy to navigate."
                },
                "extra": {
                    "tag": "img",
                    "img_key": "img_e344c476-1e58-4492-b40d-7dcffe9d6dfg",
                    "alt": {
                        "tag": "plain_text",
                        "content": "Image"
                    }
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "Feishu automatically syncs data between your devices, so everything you need is always within reach."
                },
                "extra": {
                    "tag": "select_static",
                    "placeholder": {
                        "tag": "plain_text",
                        "content": "Enter placeholder text"
                    },
                    "value": {
                        "key": "value"
                    },
                    "options": [
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "Option1"
                            },
                            "value": "1"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "Option 2"
                            },
                            "value": "2"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "Option 3"
                            },
                            "value": "3"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "Option 4"
                            },
                            "value": "4"
                        }
                    ]
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "With open API, Feishu allows integrating your own apps, existing systems, third-party systems, and quick tools."
                },
                "extra": {
                    "tag": "overflow",
                    "options": [
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "Open Feishu App Directory"
                            },
                            "value": "appStore",
                            "url": "https://app.feishu.cn"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "View Feishu Developer Docs"
                            },
                            "value": "document",
                            "url": "https://open.feishu.cn"
                        },
                        {
                            "text": {
                                "tag": "plain_text",
                                "content": "Open Feishu website"
                            },
                            "value": "document",
                            "url": "https://www.feishu.cn"
                        }
                    ]
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "With ISO 27001 & 27018 certification, the security of your data is always our top priority."
                },
                "extra": {
                    "tag": "date_picker",
                    "placeholder": {
                        "tag": "plain_text",
                        "content": "Please select date"
                    },
                    "initial_date": "2020-9-20"
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "img",
                        "img_key": "img_e344c476-1e58-4492-b40d-7dcffe9d6dfg",
                        "alt": {
                            "tag": "plain_text",
                            "content": "Image"
                        }
                    },
                    {
                        "tag": "plain_text",
                        "content": "Notes"
                    }
                ]
            }
        ]
    }
})

fei_shu_card1 = json.dumps(
    {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "🐈 英国短毛猫【test消息】"
            },
            "template": "indigo"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "英国短毛猫，体形圆胖，四肢短粗发达，毛短而密，头大脸圆，对人友善。 \n其历史可追溯至古罗马时期的家猫，由于拥有悠久的育种历史，称得上是猫家族中的典范。"
                },
                "extra": {
                    "tag": "img",
                    "img_key": "img_1cad0e51-26f6-492a-8280-a47057b09a0g",
                    "alt": {
                        "tag": "plain_text",
                        "content": "图片"
                    }
                }
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**中文学名：**\n英国短毛猫"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**拉丁学名：**\nFelinae"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": ""
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**体形：**\n圆胖"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**被毛：**\n短而浓密、俗称地毯毛"
                        }
                    }
                ]
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**1 形态特征**\n\n 🔵 外形：身体厚实，胸部饱满宽阔，腿部粗壮，爪子浑圆，尾巴的根部粗壮，尾尖钝圆。\n\n🔵 毛色：共有十五种品种被承认，其中最著名的是蓝色系的英国短毛猫。 "
                },
                "extra": {
                    "tag": "img",
                    "img_key": "img_70558e3a-2eef-4e8f-9a07-a701c165431g",
                    "alt": {
                        "tag": "plain_text",
                        "content": "图片"
                    }
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "img",
                        "img_key": "img_e61db329-2469-4da7-8f13-2d2f284c3b1g",
                        "alt": {
                            "tag": "plain_text",
                            "content": "图片"
                        }
                    },
                    {
                        "tag": "plain_text",
                        "content": "以上资料来自百度百科"
                    }
                ]
            }
        ]
    }
)

"""
>这是引用的内容
JPG,JPEG,PNG,BMP,WEBP,GIF
"""
template_str_text = f"【蔚来】亲爱的[user_name]你好，你订购的[mode_type]旗舰版车辆，已于[date]成功抵达[city_name]交付中心,请[user_name]早日提取您的[mode_type]旗舰版爱车。"

nuwa_policy_h5 = """{"category":"verify","subject":"Oppdaterte vilkår & betingelser","content":"\n    <!doctype html>\n    <html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:v=\"urn:schemas-microsoft-com:vml\" xmlns:o=\"urn:schemas-microsoft-com:office:office\" style=\"box-sizing: border-box;\">\n      <head>\n        <title>\n          \n        </title>\n        <!--[if !mso]><!-->\n        <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n        <!--<![endif]-->\n        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n        \n        <!--[if mso]>\n        <noscript>\n        <xml>\n        <o:OfficeDocumentSettings>\n          <o:AllowPNG/>\n          <o:PixelsPerInch>96</o:PixelsPerInch>\n        </o:OfficeDocumentSettings>\n        </xml>\n        </noscript>\n        <![endif]-->\n        <!--[if lte mso 11]>\n        <style type=\"text/css\">\n          .mj-outlook-group-fix { width:100% !important; }\n        </style>\n        <![endif]-->\n        \n        \n    <style type=\"text/css\">\n@media only screen and (min-width:480px) {\n  .mj-column-per-100 {\n    width: 100% !important;\n    max-width: 100%;\n  }\n}\n</style>\n    \n    \n  \n        \n        <style type=\"text/css\">\n@media only screen and (min-width:480px) {\n  .mj-column-per-100 {\n    width: 100% !important;\n    max-width: 100%;\n  }\n\n  .mj-column-per-50 {\n    width: 50% !important;\n    max-width: 50%;\n  }\n}\n@media only screen and (max-width:480px) {\n  table.mj-full-width-mobile {\n    width: 100% !important;\n  }\n\n  td.mj-full-width-mobile {\n    width: auto !important;\n  }\n}\n@media all and (max-width: 480px) {\n  .title div {\n    font-size: 40px !important;\n    line-height: 56px !important;\n  }\n\n  .left-hint div {\n    font-size: 10px !important;\n    line-height: 16px !important;\n    letter-spacing: 2px !important;\n  }\n\n  .hi-title div {\n    font-size: 24px !important;\n    line-height: 34px !important;\n  }\n\n  .hi-content div {\n    font-size: 16px !important;\n    line-height: 22px !important;\n  }\n\n  .confirm-btn a {\n    font-size: 14px !important;\n  }\n\n  .hi-note div {\n    font-size: 16px !important;\n    line-height: 22px !important;\n  }\n\n  .links * {\n    background: transparent !important;\n    text-align: left !important;\n  }\n\n  .links a {\n    font-size: 14px !important;\n  }\n\n  .footer-note div {\n    font-size: 14px !important;\n    line-height: 18px !important;\n  }\n\n  .footer .right div {\n    text-align: left !important;\n  }\n\n  .footer .store-image img {\n    width: 60px !important;\n    height: 18px !important;\n    margin-right: 8px;\n  }\n\n  .drive-title div {\n    font-size: 40px !important;\n    line-height: 56px !important;\n  }\n\n  .drive-content-title div {\n    font-size: 24px !important;\n    line-height: 34px !important;\n  }\n\n  .drive-content div {\n    font-size: 16px !important;\n    line-height: 22px !important;\n  }\n\n  .td-time div,\n.td-address div {\n    font-size: 18px !important;\n  }\n\n  .explain-title div {\n    font-size: 24px !important;\n  }\n\n  .explain-info-title div,\n.explain-info-content div {\n    font-size: 16px !important;\n  }\n\n  .footer a,\n.footer span {\n    font-size: 12px !important;\n    letter-spacing: 0 !important;\n  }\n\n  .footer .footer-mj-table .footer-mj-table-right-tb {\n    width: 53% !important;\n  }\n\n  .footer .footer-mj-table td {\n    padding-left: 14px !important;\n  }\n\n  .footer td.footer-mj-table td.right-border {\n    padding-left: 20px !important;\n    border-right: 1px solid rgba(255, 255, 255, 0.5);\n    vertical-align: bottom;\n  }\n\n  .footer .footer-ps {\n    padding: 20px !important;\n  }\n\n  .footer .footer-ps div {\n    font-size: 10px !important;\n  }\n}\n</style>\n        \n      </head>\n      <body style=\"padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; min-width: 300px; box-sizing: border-box; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; text-size-adjust: 100%; margin: 0; word-spacing: normal;\">\n        \n        \n      <div style=\"box-sizing: border-box;\">\n        \n      \n      <!--[if mso | IE]><table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"\" role=\"presentation\" style=\"width:600px;\" width=\"600\" ><tr><td style=\"line-height:0px;font-size:0px;mso-line-height-rule:exactly;\"><![endif]-->\n    \n      \n      <div style=\"box-sizing: border-box; margin: 0px auto; max-width: 600px;\">\n        \n        <table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; width: 100%;\" width=\"100%\">\n          <tbody style=\"box-sizing: border-box;\">\n            <tr style=\"box-sizing: border-box;\">\n              <td style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; direction: ltr; font-size: 0px; padding: 20px 0; text-align: center;\" align=\"center\">\n                <!--[if mso | IE]><table role=\"presentation\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\"><tr><td class=\"\" style=\"vertical-align:top;width:600px;\" ><![endif]-->\n            \n      <div class=\"mj-column-per-100 mj-outlook-group-fix\" style=\"box-sizing: border-box; font-size: 0px; text-align: left; direction: ltr; display: inline-block; vertical-align: top; width: 100%;\">\n        \n      <table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; vertical-align: top;\" width=\"100%\" valign=\"top\">\n        <tbody style=\"box-sizing: border-box;\">\n          \n              <tr style=\"box-sizing: border-box;\">\n                <td align=\"left\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\">\n                  \n      <div style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 1; text-align: left; color: #000000;\"><div id=\"i57u7\" class=\"content\" style=\"box-sizing: border-box; caret-color: rgb(0, 0, 0); font-family: Calibri; font-size: 14px; text-size-adjust: auto; margin: 0px auto; max-width: 600px;\"><table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\" width=\"600\" id=\"ihdii\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; width: 600px;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"center\" id=\"i92i5\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; direction: ltr; font-size: 0px; padding: 20px 0px; text-align: center;\"><div id=\"i21d5\" class=\"mj-column-per-100 mj-outlook-group-fix\" style=\"box-sizing: border-box; text-align: left; direction: ltr; display: inline-block; vertical-align: top; width: 600px;\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\" valign=\"top\" width=\"100%\" id=\"ivh9h\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; vertical-align: top;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"ivz8o\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><div id=\"igk43\" style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 32px; line-height: 36px;\">Vilkår &amp;<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span><br style=\"box-sizing: border-box;\">Betingelser</div></td></tr><tr style=\"box-sizing: border-box;\"><td align=\"center\" id=\"izk2k\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\" id=\"iev1k\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; border-spacing: 0px;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td width=\"550\" id=\"inbvj\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; width: 550px;\"><img height=\"auto\" src=\"https://cdn-app.eu.nio.com/mp/2021/09/17/fddbd4d9-9128-49d7-b153-e6474c6c3098.jpeg\" width=\"550\" id=\"i84oy\" style=\"border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; box-sizing: border-box; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; height: auto; outline-color: initial; outline-style: none; outline-width: initial; text-decoration-line: none; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; line-height: 13px; display: block; width: 550px; font-size: 13px;\"></td></tr></tbody></table></td></tr><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"ia92p\" class=\"hi-title\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><div id=\"ihtli\" style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 1;\">Hei.</div></td></tr><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"ijoa4\" class=\"hi-content\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><div id=\"irk2q\" style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 1;\">Vi ønsker å informere deg, at vi har oppdatert våre vilkår &amp; betingelser.</div></td></tr><tr style=\"box-sizing: border-box;\"><td align=\"left\" vertical-align=\"middle\" id=\"it5iw\" class=\"confirm-btn\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\" id=\"ibdwi\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: separate; line-height: 16px;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"center\" bgcolor=\"rgb(65, 65, 65)\" role=\"presentation\" valign=\"middle\" id=\"i7bbh\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; border: none; border-radius: 3px; cursor: auto; background-color: rgb(65, 65, 65);\"><a href=\"[#href#]\" target=\"_blank\" title=\"https://policy.eu.nio.com/#/app-tou?lang=no_NO&is_embed=0&ver=p211130\" id=\"irkyj\" style=\"box-sizing: border-box; display: inline-block; color: rgb(255, 255, 255); font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 15.6px; margin: 0px; text-decoration-line: none; padding: 10px 25px; border-radius: 3px;\">Les mer<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span></a></td></tr></tbody></table></td></tr><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"i6an5\" class=\"hi-note hi-sign\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><div id=\"igy39\" style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 1;\">Disse oppdateringene vil tre i kraft fra om med [#date#].</div></td></tr><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"icr1g\" class=\"hi-note\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 10px 25px; word-break: break-word;\"><div id=\"iz44k\" style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 1;\">Vennlig hilsen<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span><div style=\"box-sizing: border-box;\">NIO Norge</div></div></td></tr></tbody></table></div></td></tr></tbody></table></div><div id=\"i1t9i\" class=\"footer\" style=\"box-sizing: border-box; caret-color: rgb(0, 0, 0); font-family: Calibri; font-size: 14px; text-size-adjust: auto; margin: 20px auto 0px; max-width: 600px; background-color: rgb(0, 15, 22);\"><table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"i1rw8\" role=\"presentation\" width=\"600\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; width: 600px;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"center\" id=\"i1602\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; direction: ltr; font-size: 0px; padding: 20px 0px; text-align: center;\"><div id=\"ij2iw\" style=\"box-sizing: border-box; margin: 0px auto; max-width: 600px; font-size: 14px; color: rgb(255, 255, 255);\"><table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"i3af2\" role=\"presentation\" width=\"600\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; width: 600px;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"i4toh\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; direction: ltr; font-size: 0px; padding: 20px 0px 0px;\"><div id=\"izz9i\" class=\"mj-column-per-100 mj-outlook-group-fix\" style=\"box-sizing: border-box; direction: ltr; display: inline-block; vertical-align: top; width: 600px; font-size: 14px; color: rgb(255, 255, 255);\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"i660o\" role=\"presentation\" valign=\"top\" width=\"100%\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; vertical-align: top;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"i5slq\" class=\"footer-mj-table\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; padding: 0px; word-break: break-word;\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"im0yu\" width=\"600\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; color: rgb(0, 0, 0); font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 13px; line-height: 22px; table-layout: auto; width: 600px; border: none;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td id=\"i0gdh\" rowspan=\"6\" valign=\"top\" class=\"footer-icon right-border\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 60px; border-right: 1px solid rgba(255, 255, 255, 0.5); vertical-align: top;\"><img height=\"39\" id=\"ieo4a\" src=\"https://d1pfnb75kyosdp.cloudfront.net/images/mail-templates/footerIcon.png\" width=\"111\" style=\"border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; box-sizing: border-box; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; outline-color: initial; outline-style: none; outline-width: initial; text-decoration-line: none; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; line-height: 13px; width: 111px; height: 39px;\"></td><td id=\"igjj5\" width=\"300\" class=\"footer-mj-table-right-tb\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px; width: 300px;\"><a href=\"https://www.nio.com/no_NO/news/contact?noredirect=\" id=\"i008o\" title=\"https://www.nio.com/no_NO/news/contact?noredirect=\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\">KONTAKT OSS</a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"insyi\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px;\"><a href=\"https://www.nio.com/no_NO/newsletter\" id=\"ibykn\" title=\"https://www.nio.com/no_NO/newsletter\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\">ABONNER PÅ NIO-NYHETER</a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"i76wp\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px;\"><a href=\"https://www.nio.com/no_NO/privacy-policy/privacy-notice\" id=\"ivtaz\" title=\"https://www.nio.com/no_NO/privacy-policy/privacy-notice\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\">PERSONVERN</a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"i9czv\" class=\"footer-padding-top20\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px; padding-top: 20px;\"><a css-class=\"footer-padding-top\" href=\"https://www.nio.com/no_NO\" id=\"ipc5k\" title=\"https://www.nio.com/no_NO\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\">HJEMMESIDE</a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"ir8wv\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px;\"><a href=\"https://www.instagram.com/nionorge/\" id=\"i7oxf\" title=\"https://www.instagram.com/nionorge/\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\">INSTAGRAM</a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"iv2t7\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px;\"><a href=\"https://www.facebook.com/NIONorge\" id=\"iuk3l\" title=\"https://www.facebook.com/NIONorge\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\">FACEBOOK</a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"i745q\" rowspan=\"6\" valign=\"bottom\" class=\"right-border\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 60px; border-right: 1px solid rgba(255, 255, 255, 0.5); vertical-align: bottom;\">NIO Norge AS<br style=\"box-sizing: border-box;\">Karl Johans Gate 33<br style=\"box-sizing: border-box;\">0162 Oslo, Norge<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span></td><td id=\"iszqh\" class=\"footer-padding-top20\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px; padding-top: 20px;\">LAST NED APPEN VÅR<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"iunbai\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px;\"><a href=\"https://play.google.com/store/apps/details?id=com.nio.nioapp\" id=\"iy9q24\" target=\"_blank\" title=\"https://play.google.com/store/apps/details?id=com.nio.nioapp\" class=\"store-image\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\"><img height=\"25\" id=\"it25tb\" src=\"https://cdn-titan.eu.nio.com/titan/2021/08/19/c2c317c1-6b08-4171-8053-b8744b1dfa4f.png\" width=\"85\" style=\"border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; box-sizing: border-box; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; outline-color: initial; outline-style: none; outline-width: initial; text-decoration-line: none; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; line-height: 14px; position: static; margin-right: 16px; margin-top: 5px; width: 85px; height: 25px;\"><span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span></a><a href=\"https://apps.apple.com/no/app/nio/id1157302846\" id=\"irbju9\" target=\"_blank\" title=\"https://apps.apple.com/no/app/nio/id1157302846\" class=\"store-image\" style=\"box-sizing: border-box; text-decoration-line: none; font-size: 14px; color: rgb(255, 255, 255);\"><img height=\"25\" id=\"iudcjd\" src=\"https://cdn-titan.eu.nio.com/titan/2021/08/19/706c0faf-0c24-4af0-88b3-129d82937673.png\" width=\"85\" style=\"border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; box-sizing: border-box; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; outline-color: initial; outline-style: none; outline-width: initial; text-decoration-line: none; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; line-height: 14px; position: static; margin-right: 16px; margin-top: 5px; width: 85px; height: 25px;\"></a></td></tr><tr style=\"box-sizing: border-box;\"><td id=\"i9ogz4\" class=\"footer-padding-top20\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; padding-left: 50px; padding-top: 20px;\">© NIO 2021<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span></td></tr></tbody></table></td></tr></tbody></table></div></td></tr></tbody></table></div><div id=\"iv4ujq\" style=\"box-sizing: border-box; margin: 0px auto; max-width: 600px; font-size: 14px; color: rgb(255, 255, 255);\"><table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"ijodik\" role=\"presentation\" width=\"600\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; width: 600px;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"center\" id=\"io6zsa\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; direction: ltr; font-size: 0px; padding: 20px 0px; text-align: center;\"><div id=\"i2fata\" class=\"mj-column-per-100 mj-outlook-group-fix\" style=\"box-sizing: border-box; text-align: left; direction: ltr; display: inline-block; vertical-align: top; width: 600px; font-size: 14px; color: rgb(255, 255, 255);\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"im6mar\" role=\"presentation\" valign=\"top\" width=\"100%\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; vertical-align: top;\"><tbody style=\"box-sizing: border-box;\"><tr style=\"box-sizing: border-box;\"><td align=\"left\" id=\"i4276r\" class=\"footer-ps\" style=\"mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; border-collapse: collapse; font-size: 0px; word-break: break-word; padding: 20px 60px;\"><div id=\"idb1dx\" style=\"box-sizing: border-box; font-family: BlueSkyStandard-Regular, BlueSkyStandard; font-size: 14px; line-height: 16px; color: rgba(255, 255, 255, 0.5);\">Dette er en service-e-post. Denne kan ikke besvares.<span class=\"Apple-converted-space\" style=\"box-sizing: border-box;\"> </span></div></td></tr></tbody></table></div></td></tr></tbody></table></div></td></tr></tbody></table></div></div>\n    \n                </td>\n              </tr>\n            \n        </tbody>\n      </table>\n    \n      </div>\n    \n          <!--[if mso | IE]></td></tr></table><![endif]-->\n              </td>\n            </tr>\n          </tbody>\n        </table>\n        \n      </div>\n    \n      \n      <!--[if mso | IE]></td></tr></table><![endif]-->\n    \n    \n      </div>\n    \n      </body>\n    </html>\n  ","sender_name":"notification@nio.io"}"""

wechat_applet_template_dict = {"[#key1#]": "[#value1#]", "[#key2#]": "[#value2#]", "[#key3#]": "[#value3#]", "[#key4#]": "[#value4#]"}

with open(f'{BASE_DIR}/data/test.ftl', 'r') as f:
    free_marker = f.read()
