# API
#### 随机返回一首音乐

> 请求URL: https://anime-music.jijidown.com/api/v1/music

> 请求方式: GET

> 请求参数: <br>recommend   bool    非必须 #是否只返回推荐曲目

> 返回内容:
```
{
    id: "5b84d6e0b02de208826878ff", # 使用此ID可以直接获取到该条数据, 详见下面
    atime: 1535432416,
    play_url: "http://anime-music.files.jijidown.com/5b84d6e0b02de208826878ff_128.mp3?t=1536044958&sign=48242B5A45230126CE75E5F93ABAFABF",
    title: "Caffeine",
    recommend: false,
    type: "其他",
    author: "未知",
    anime_info: {
        id: "5b836fb6b02de2130c916306",
        logo: "",
        atime: 1390018594,
        desc: "《RWBY》是一部在2013年7月播出的动画。R、W、B、Y 分别是英语红白黑黄的首字母，代表的分别是四位女主角的主题色。由美国 Rooster Teeth 动画工作室RWBY团队制作，导演Monty Oum 。已正式播放正片。 本作的背景设定在类现代但是充满著超自然力量的世界。主要人物为四个拥有各自的特殊能力及武器的女孩，她们因各种原因聚在一起组成团队并接受训练，以对抗怪物、恶棍或其他类似的团体。在这系列中，“尘埃”（Dust）被用作魔力来源。",
        bg: "http://i1.fuimg.com/510372/1c1c5225f97f8b35.jpg",
        month: 99,
        title: "RWBY",
        year: 9999,
    },
}
```

#### 返回指定ID的信息
> 请求URL: https://anime-music.jijidown.com/api/v1/music/5b84d6e0b02de208826878ff

> 其他信息和上面的接口是一样的

# 前端
> 主要是用来给主站提供播放功能的一个小轮子, 包含完整的播放器功能, 提供了最常用的播放状态回调, 使用源生js实现。

> DEMO: [https://jxiaoc.github.io/animeMusic/demo.html](https://jxiaoc.github.io/animeMusic/demo.html)

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

播放器加载完毕后会触发此回调，并且会传入res, 请根据res返回的数据进行页面填充, res格式详见最上方API
 
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

> 后台通过/god可以直接访问, python中没有做任何权限设置, 而是直接交由nginx处理, 详见[此文件](https://github.com/JxiaoC/animeMusic/blob/master/animeMusic_server/anime_music/nginx/anime-music.jijidown.com.conf)

> 图片存储在贴图库中, 通过官方API进行上传, 需要单独新建setting.py文件并且配置相应key, 在[此文件](https://github.com/JxiaoC/animeMusic/blob/master/animeMusic_server/helper/tietuku.py)中有详细注释

> MP3文件分别存储在阿里云OSS和自建的文件服务器上, OSS主要用于备份, 文件服务器用于MP3播放器直链; 文件服务器的数据管理通过FTP实现, 所以需要在文件服务器上自己搭建好FTP, 并在配置文件中配置好相应参数; 所有的配置参数均在代码的注释中有详细说明, [OSS](https://github.com/JxiaoC/animeMusic/blob/master/animeMusic_server/aliyun/oss.py), [FTP](https://github.com/JxiaoC/animeMusic/blob/master/animeMusic_server/helper/ftp.py)

> 同时为了降低文件服务器的负荷, 后台会将上传上来的MP3文件自动转码成128Kbps音质, 转码使用ffmpeg, 所以需要提前安装
<br>sudo apt-get install ffmpeg<br>pip3 install ffmpy 

#### 服务端配置以及启动

> 启动文件main.py在 animeMusic_server/anime_music中

##### daemon.sh 文件
> daemon.sh文件主要负责主程序的启动和关闭
> <br> ./daemon.sh start ./daemon.sh stop

> 这里只写一些不常见的参数, 其他参数看变量名应该也能知道是什么
> <br>PORT_RANGE: 要监听的端口范围, 12040 12043 则为监听12040, 12041, 12042和12043共计4个端口, 也就意味着会启动4个线程
> <br>PORT_RANGE的端口范围要和nginx配置中的upstream一一对应

##### restart.sh 文件
> 负责启动和重启主程序, 通过调用daemon.sh的stop和start实现

##### main.py 文件
> 主程序入口, 负责监听指定端口, 常驻后台处理http请求, 一般情况下不需要直接运行此文件, 推荐通过restart.sh文件启动 

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