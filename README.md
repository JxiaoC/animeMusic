# 前端
> 主要是用来给主站提供播放功能的一个小轮子, 包含完整的播放器功能, 提供了最常用的播放状态回调, 使用源生js实现。

> [DEMO](http://anime-music.files.jijidown.com)

## 简易文档

### 事件

##### 监听播放器播放事件

> animeMusic.onPlay = function() {console.log('play')};

当播放器开始播放时则会触发回调

##### 监听播放器播放事件（播放的渐入效果执行完毕）

> animeMusic.onPlayed = function() {console.log('played')};

当播放器开始播放后, 1.1秒后触发此事件(1秒的播放淡入效果, 留0.1秒作为冗余)

##### 监听播放器暂停事件

> animeMusic.onPause = function() {console.log('pause')};

当播放器开始播放时则会触发回调

##### 监听播放暂停事件（播放的渐入效果执行完毕）

> animeMusic.onPaused = function() {console.log('paused')};

当播放器暂停播放后, 1.1秒后触发此事件(1秒的暂停淡出效果, 留0.1秒作为冗余)

##### 监听播放器当前播放进度

> animeMusic.onProgress = function(per, now, all) {console.log('onProgress')};

返回的依次为播放百分比(Number), 当前播放时间(MM:SS), 总长度(MM:SS), 请根据需要使用, per可以用于控制进度条位置

##### 监听播放器开始加载

> animeMusic.onLoad = function() {console.log('load')};

当播放器开始加载数据时则会触发此回调

##### 监听播放器加载完毕

> animeMusic.onLoaded = function(res) {console.log(res)};

播放器加载完毕后会触发此回调，并且会传入res, 请根据res返回的数据进行页面填充, res格式如下

``` {
    title: "迷惑スペクタクル",
    play_url: "http://anime-music.files.jijidown.com/5b852309b02de202d2f97a76_128.mp3?t=1535616962&sign=E3FFE0BB789F153EEFE5FCC4B5454100",
    recommend: 1,
    atime: 1535451913,
    id: "5b852309b02de202d2f97a76",
    anime_info: {
        title: "上课小动作",
        month: 1,
        bg: "http://i2.tiimg.com/510372/beb3c236c8e111fd.jpg",
        year: 2014,
        logo: "http://i1.fuimg.com/510372/e638b6c3413a884a.jpg",
        atime: 1402639425,
        id: "5b8389cbb02de275deb90f73",
        desc: "坐在横井同学隔壁的男生──关同学，是个总是在上课时以令人叹为观止的方式玩著各种游戏的人，因此横井同学每次都会不由自主的被他吸引住目光，无法认真上课，让横井同学每天都为此困扰不已。究竟关同学是如何的运用上课时间玩各种游戏，横井同学又会身不由己的陪著他闹出什麼笑话呢？这是一部以上课时间为舞台的搞笑诙谐故事。",
    }
}
 ```
 
### 方法

##### 播放

> animeMusic.Play();

PS：第一次播放请使用animeMusic.Next(); 详细方法见demo

##### 暂停

> animeMusic.Pause();

##### 下一曲

> animeMusic.Next(); 或 animeMusic.Next(id);

传入id将会播放指定id的音乐，否则随机返回一首， id在onLoaded事件中会作为回调参数传入, res.id为音乐id, res.anime_info.id为该音乐对应动漫的id

##### 从指定位置开始播放

> animeMusic.PlayTo(percentage);

传入进度百分比, 比如animeMusic.PlayTo(50); 则从一半的位置开始播放, 不推荐直接调用此方法, 推荐使用下面的bindPlayTo方法

##### 绑定进度条后，实现从鼠标点击的指定位置开始播放

> animeMusic.bindPlayTo(selectName);

传入进度条所在的选择器key, 例animeMusic.bindPlayTo('.player .progress');此时该进度条就拥有了点击播放的功能了, 详见demo中的示例代码

### 参数

##### 返回推荐曲目

> animeMusic.recommend = true

请求将只会返回推荐的曲目, 在下次执行Next时生效, Next指定id时无效



# 服务端

> 服务器基于debian + nginx + python + redis + mongodb 开发

> 服务端代码将在随后发出（现在还在写后台方面的东西）


# 文件服务器

> 为了保证可用性(之前使用网盘盗链导致后来所有文件失效, 还好有做备份, 所以这次重构不在考虑放在别的地方了QAQ)，所有MP3文件均存放在自己搭建的文件服务器上, 为了尽量保证可用性, 单线程限速512KB, 为了减少恶意盗链行为, 文件服务器基于openresty, 使用lua进行文件鉴权, 鉴权代码如下

```
local request_uri = ngx.var.request_uri;
local file_name = string.sub(request_uri, 2, 25);
local arg = ngx.req.get_uri_args();
local key = 'key';

local function auth(name, t, sign)
    if ngx.time() >= tonumber(t) then
        ngx.header.content_type = "text/plain";
	ngx.say('{"code": -1, "msg": "timeout"}');
	ngx.exit(400);
    end

    local _ = ngx.md5(name .. t .. key);

    if string.upper(_) ~= sign then
	ngx.header.content_type = "text/plain";
	ngx.say('{"code": -2, "msg": "sign fail"}');
        ngx.exit(400);
    end

    return true;
end

local auth_pass = auth(file_name, arg['t'], arg['sign']);
```