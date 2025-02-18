📅 时间：2024年7月11日  
👨‍💻 作者GitHub：@caspiankexin  
📨 作者邮箱： [联系我](mailto:mirror_flower@outlook.com)  
项目地址：[sxgbxx学习助手](https://github.com/caspiankexin/sxgbxx_assistant)   
下载地址：http://caspian.ysepan.com/  
转载至：原创

---
# 配合油猴脚本刷课程

> 2022年通过python模拟键鼠操作，来实现刷课（详情见旧文：https://mp.weixin.qq.com/s/EUQKUMutxCE30aYt8L67UQ ）。同时也在网上找到有人做的后台静默自动刷课的软件，但已经不能使用了。刚好之前又看到有油猴脚本可以刷专题课程，所以重新写个软件，让刷课更加高效简单。

# 一、程序思路

1. 程序运行的核心的网上别人写的自动刷专题课程的油猴脚本，通过Python来打开下一个专题，让脚本再开始刷课。
2. 通过Python逐个打开专题学习网址，在脚本学习完成后，让Python打开下一个专题网址。两者搭配实现自动还刷课。
3. 难点：每个专题学习时间各不相同，再加之需要多一点时间冗余，何时让Python打开下一个专题网址，就很困难。解决办法是，修改脚本，让学习完一个专题后，关闭标签页，同时对浏览器进行一些设置，可以实现学习完一个专题后关闭浏览器。检测浏览器运行状态就可以判断专题是否学习完成，可以间隔一段时间检测一下，这样就可以确保一个专题学完后开始下一个专题。

# 二、代码编写

1. 获取输入的多个专题网址

   ```python
   # 获取用户输入的专题网址和对应的时间
   urls_input = input("输入专题网址，用空格分隔多个网址: ")
   
   # 使用split方法分割字符串，获得专题网址列表和每个专题的注册时间列表
   urls = urls_input.split()  # 分割网址字符串
   ```

2. 检测浏览器是否在系统进程中，以此判断专题是否学习完毕

   ```Python
   def is_edge_running():
       # 在Windows上，Edge的进程名通常是'msedge.exe'
       edge_process_names = ['msedge.exe', 'MicrosoftEdge.exe']
       for proc in psutil.process_iter(['name']):
           if proc.info['name'] in edge_process_names:
               return False
       return True
   ```

3. 遍历专题网址列表，用浏览器打开网址，判断是否学完，进行循环

   ```python
   # 遍历网址列表
   for url in urls:
       counter += 1  # 增加计数器，用于记录是第几次循环
   
       # 打开新的浏览器标签页
       webbrowser.open_new_tab(url)
       print(f"已打开第{counter}个专题的网页，正在进行学习")
   
       # 等待指定的时间
       time.sleep(1200)
       print(f"第{counter}个专题已学习1200秒，准备开始检测是否学习完毕")
   
       # 循环检查条件，直到满足
       while not is_edge_running():
           print(f"第{counter}个专题还未学习完成，600秒后将再次检测")
           time.sleep(600)  # 等待600秒
       print(f"第{counter}个专题已学习完毕，准备开始学习下一个专题")
   print("所有专题学习完毕，请关闭软件。")
   ```

4. 完整代码

   ```python
   import webbrowser
   import time
   import psutil
   
   # 打印程序说明
   print("用默认浏览器登陆网站，并报名各专题，再进行操作")
   
   # 获取用户输入的专题网址
   urls_input = input("输入专题网址，用空格分隔多个网址: ")
   
   # 使用split方法分割字符串，获得专题网址列表
   urls = urls_input.split()  # 分割网址字符串
   
   # 初始化计数器
   counter = 0
   
   # 检测浏览器是否处于打开状态
   def is_edge_running():
       # 在Windows上，Edge的进程名通常是'msedge.exe'
       edge_process_names = ['msedge.exe', 'MicrosoftEdge.exe']
       for proc in psutil.process_iter(['name']):
           if proc.info['name'] in edge_process_names:
               return False
       return True
   
   # 遍历网址列表
   for url in urls:
       counter += 1  # 增加计数器，用于记录是第几次循环
   
       # 打开新的浏览器标签页
       webbrowser.open_new_tab(url)
       print(f"已打开第{counter}个专题的网页，正在进行学习")
   
       # 等待指定的时间
       time.sleep(1200)
       print(f"第{counter}个专题已学习1200秒，准备开始检测是否学习完毕")
   
       # 循环检查条件，直到满足
       while not is_edge_running():
           print(f"第{counter}个专题还未学习完成，600秒后将再次检测")
           time.sleep(600)  # 等待600秒
       print(f"第{counter}个专题已学习完毕，准备开始学习下一个专题")
       
   print("所有专题学习完毕，请关闭软件。")
   ```

# 三、具体操作教程

## （一）基础准备

1. 确保电脑安装了`Microsoft Edge`浏览器（一般系统自带），如果没有可在此处下载安装：[Edge下载地址](https://www.microsoft.com/en-us/edge/download?form=MA13FJ)

2. edge浏览器安装“`暴力猴`”插件，安装地址：[暴力猴 - Microsoft Edge Addons](https://microsoftedge.microsoft.com/addons/detail/暴力猴/eeagobfjdenkkddmbclomhiblgggliao?hl=zh-CN)

3. 在“暴力猴”插件中添加“`山西好干部`”油猴脚本，参照下方图片添加修改后的脚本，脚本原版本为：[山西好干部（原版）](https://greasyfork.org/zh-CN/scripts/466343-山西好干部)<img src="https://cors.zme.ink/http://cdn.idreams.cc/202407111849705.jpg" alt="添加油猴脚本" style="zoom:80%;" />
```js

// ==UserScript==
// @name         山西好干部
// @namespace    http://tampermonkey.net/
// @version      0.3.3
// @description  进入https://www.sxgbxx.gov.cn/uc/plan 选择专题，进入专题后开始学习
// @author       freeman99sd
// @license MIT
// @require      https://greasemonkey.github.io/gm4-polyfill/gm4-polyfill.js
// @require      https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js
// @require      https://cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue.min.js
// @require      https://cdn.jsdelivr.net/npm/@supabase/supabase-js@1.0.3/dist/umd/supabase.min.js
// @match        https://www.sxgbxx.gov.cn/
// @match        https://www.sxgbxx.gov.cn/uc/plan
// @match        https://www.sxgbxx.gov.cn/uc/plan/info?*
// @match        https://www.sxgbxx.gov.cn/front/couinfo*
// @match        https://www.sxgbxx.gov.cn/front/playkpoint*
// @grant        GM_download
// @grant        GM_openInTab
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @grant        unsafeWindow
// @grant        GM_setClipboard
// @grant        GM_getResourceURL
// @grant        GM_getResourceText
// @grant        GM_info
// @grant        GM_registerMenuCommand
// @run-at       document-idle
// @downloadURL https://update.greasyfork.org/scripts/466343/%E5%B1%B1%E8%A5%BF%E5%A5%BD%E5%B9%B2%E9%83%A8.user.js
// @updateURL https://update.greasyfork.org/scripts/466343/%E5%B1%B1%E8%A5%BF%E5%A5%BD%E5%B9%B2%E9%83%A8.meta.js
// ==/UserScript==

(async function () {
	'use strict';
  var newWindow

  var homeUrl = "https://www.sxgbxx.gov.cn/"
  var planListUrl = "https://www.sxgbxx.gov.cn/uc/plan"
  var planInfoUrl = "https://www.sxgbxx.gov.cn/uc/plan/info"
  var courseInfo = "https://www.sxgbxx.gov.cn/front/couinfo"
  var courseDetail = "https://www.sxgbxx.gov.cn/front/playkpoint"
  if(window.location.href.startsWith(planInfoUrl)) {
    studyPlan()
  } else if (window.location.href.startsWith(courseInfo)) {
    watchCourse()
  } else if (window.location.href.startsWith(courseDetail)) {
    playCourse()
  } else if (window.location.href == homeUrl) {
    let res = $(".u-login-box.pr")
    if (res.length == 0) {
      alert("请登录后再开始学习")
    } else {
      window.open(planListUrl)
    }
  }

  function playCourse() {
    $(document).ready(async() => {
      //如果当前播放进度为100%，切换到下一个不为100%的
      let currentProgress = $(".chap-seclist ul li.current .c-blue1").text()
      if(currentProgress.trim() == "100%") {
        let arr = $(".chap-seclist")
        for(let i = 0; i< arr.length; i++) {
          if($(arr[i]).find(".c-blue1").text().trim() != "100%") {
            $(arr[i]).find(".kpoint_list").click()
            return
          }
        }
        //所有的都学完，关闭
        window.close();
        return
      }

      //5s 后开始播放
      setTimeout(() => {
          if($(".chap-seclist ul li.current .play-icon-box.image-icon-box").attr("title") == "图文播放") {
              location.reload();
              return
          }
        $(".pv-volumebtn.pv-iconfont.pv-icon-volumeon")[0].click()
        $("button.pv-playpause.pv-iconfont.pv-icon-btn-play")[0].click()
      }, 15000);

      var timer = setInterval(function () {
				let text = $(".pv-time-wrap").text()
        let textArr = text.split("/")
        if(textArr[0].trim() == textArr[1].trim()) {
          clearInterval(timer);
          window.close();
        }
			}, 15000);
    })
  }


  function studyPlan() {
    $(document).ready(() => {
      let courseBtnArr = $("aside.u-f-c-more.my-cou-check")
      let willStudyArr = [] //待学的
      for(let i = 0; i<courseBtnArr.length; i++) {
        let temp = $(courseBtnArr[i]).prev("div.txtOf.mt5.hLh20")
        let reg_count = /总章节数：([0-9]+)\s*已学完章节：([0-9]+)/
        let regArr = reg_count.exec(temp.text())
        if (regArr[1] > regArr[2]) {
          willStudyArr.push(courseBtnArr[i])
        }
      }

      if (willStudyArr.length == 0) {
        // alert("本专题已学完，请切换专题")
      setTimeout(() => {window.close()}, 5000);
        return
      }

      $(willStudyArr[0]).find("a").click((e) => {
        e.preventDefault()
        // 打开新窗口并获取窗口对象
        newWindow = window.open($(willStudyArr[0]).find("a").attr('href'), '_blank');
        // 在新窗口加载完成后执行操作
        $(newWindow).on('load', function() {
          // 在新窗口中执行你想要的操作
          // 例如，修改新窗口的内容或调用新窗口的方法
          // 可以使用 newWindow.document 对象来访问新窗口的 DOM
          console.log('新窗口已加载');
        });
      })
      $(willStudyArr[0]).find("a")[0].click()

      var timer = setInterval(function () {
				if (newWindow.closed) {
					location.reload();
					clearInterval(timer);
				}
			}, 10000);
    })
  }

  function watchCourse() {
    $(document).ready(() => {
      $("a.bm-lr-btn").click()
    })
  }

})();
```
4. 设置Edge浏览器：设置→系统和性能→系统→关闭“启动增强”。如下图![Edge设置图片](https://cors.zme.ink/http://cdn.idreams.cc/202407111822112.png)

5. 设置Edge浏览器：设置→外观→自定义浏览器→关闭“关闭最后一个标签页时保留 Edge 窗口”。如下图<img src="https://cors.zme.ink/http://cdn.idreams.cc/202407111934988.png" alt="Edge设置图片-标签页" style="zoom:80%;" />

6. 设置Edge浏览器：设置→Cookie 和已存储数据→所有权限→弹出窗口和重定向→添加→“https://www.sxgbxx.gov.cn”。如下图![Edge设置图片-打开弹窗](https://cors.zme.ink/http://cdn.idreams.cc/202407122102006.png)![Edge设置图片-弹窗白名单](https://cors.zme.ink/http://cdn.idreams.cc/202407122104940.png)

## （二）前期准备

1. 打开“`暴力猴`”插件管理页面，关闭“`山西好干部`”脚本开关。“暴力猴”插件管理页面：extension://eeagobfjdenkkddmbclomhiblgggliao/options/index.html  ![暴力猴脚本关闭图片](https://cors.zme.ink/http://cdn.idreams.cc/202407111822799.png)
2. 打开“[山西干部在线学院 ](https://www.sxgbxx.gov.cn/)”官网→登录学习账号→打开“专题培训”页面→选择需要学习的专题→进行“报名”→点击“立即学习”，复制打开页面的网址。如下图![复制专题学习的网址](https://cors.zme.ink/http://cdn.idreams.cc/202407111822488.png)
3. 将需要学习的专题的网址进行整理，用空格隔开，之后会用到。（例如：网址1 网址2 网址3 网址4）
4. 将`前期准备`中的`第1步`里关闭的脚本开关，打开。
5. 关闭Edge浏览器，关闭其他不必要的软件，关闭不要的其他通知类消息。

## （三）运行程序

软件界面：<img src="https://cors.zme.ink/http://cdn.idreams.cc/202407122124982.png" alt="软件界面" style="zoom: 67%;" />

1. 双击运行“配合油猴脚本刷课程.exe”文件，在程序中输入`前期准备`中的`第3步`整理的网址，点击“开始学习”，开始运行程序。

   > 程序下载地址：http://caspian.ysepan.com/

2. 保持电脑网络连接正常，尽量不要再操作电脑，让程序自己运行。

3. 如果发现异常，一般是网络问题或电脑其他操作影响，可以直接关闭软件或点击“终止”按钮关闭。再重新开始操作。
