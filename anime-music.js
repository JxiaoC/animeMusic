var animeMusic = {
    'recommend': false,
    'max_load_time': 10, // 最大加载时间, 一首歌的加载时间超过此数值, 将会直接跳到下一曲
    '_anime_music_player': new Audio(),
    '_loading': false,
    '_play_or_pauseing': false,
    '_setI_play': null,
    '_setI_pause': null,
    '_setI_progress': null,
    '_now_load_time': 0,
    'Play': function () {
        if ((animeMusic._play_or_pauseing || !animeMusic._anime_music_player.paused)) return;
        animeMusic._play_or_pauseing = true;
        try {
            animeMusic.onPlay();
        }
        catch (e) {
        }
        if (animeMusic._anime_music_player.paused) {
            animeMusic._anime_music_player.play();
            animeMusic._setI_progress = setInterval(function () {
                animeMusic.progress();
            }, 333);
            animeMusic._setI_play = setInterval(function () {
                try {
                    animeMusic._anime_music_player.volume += 0.01;
                }
                catch (e) {
                }
            }, 10);
            setTimeout(function () {
                clearInterval(animeMusic._setI_play);
                animeMusic._play_or_pauseing = false;
                try {
                    animeMusic.onPlayed();
                }
                catch (e) {
                }
            }, 1100);
        } else {
            animeMusic.Next();
        }
    },
    'PlayTo': function (percentage) {
        animeMusic._anime_music_player.currentTime = animeMusic._anime_music_player.duration * (percentage / 100);
    },
    'Pause': function () {
        if (animeMusic._play_or_pauseing || animeMusic._anime_music_player.paused) return;
        animeMusic._play_or_pauseing = true;
        clearInterval(animeMusic._setI_progress);
        try {
            animeMusic.onPause();
        }
        catch (e) {
        }
        animeMusic._setI_pause = setInterval(function () {
            try {
                animeMusic._anime_music_player.volume -= 0.01;
            }
            catch (e) {
            }
        }, 10);
        setTimeout(function () {
            clearInterval(animeMusic._setI_pause);
            animeMusic._anime_music_player.pause();
            animeMusic._play_or_pauseing = false;
            try {
                animeMusic.onPaused();
            }
            catch (e) {
            }
        }, 1100);
    },
    'Next': function (id) {
        if (animeMusic._loading) return;
        animeMusic._loading = true;
        try {
            animeMusic.onLoad();
        }
        catch (e) {
        }
        animeMusic.Pause();
        var url;
        if (id) url = '//anime-music.jijidown.com/api/v2/music/' + id + '?recommend=' + animeMusic.recommend.toString();
        else url = '//anime-music.jijidown.com/api/v2/music?recommend=' + animeMusic.recommend.toString();
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                if (xmlhttp.status == 200) {
                    var res = JSON.parse(xmlhttp.response).res;
                    if (res.code != 0) {
                        setTimeout(function () {
                            animeMusic._anime_music_player.src = res.play_url;
                            animeMusic.Play();
                            animeMusic._now_load_time = 0;
                            animeMusic._loading = false;
                            try {
                                animeMusic.onLoaded(res);
                            }
                            catch (e) {
                            }
                        }, 1300);
                    } else {
                        animeMusic._loading = false;
                        setTimeout(function () {
                            animeMusic.Next();
                        }, 3000);
                        console.log(res.msg);
                    }
                }
            }
        };
        xmlhttp.onerror = function () {
            animeMusic._loading = false;
            setTimeout(function () {
                animeMusic.Next();
            }, 3000);
            console.log('xmlhttp.onerror');
        };
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
    },
    'progress': function () {
        try {
            var all_time = secondToDate(animeMusic._anime_music_player.duration);
            var now_time = secondToDate(animeMusic._anime_music_player.currentTime);
            var percentage = parseInt(animeMusic._anime_music_player.currentTime / animeMusic._anime_music_player.duration * 100);
            try {
                animeMusic.onProgress(percentage, now_time, all_time);
            }
            catch (e) {
            }
        }
        catch (e) {
        }
    },
    'bindPlayTo': function (name) {
        var dom = document.querySelector(name);
        if (dom) {
            dom.onclick = function (ev) {
                var oEvent = ev || event;
                var left = oEvent.offsetX;
                var percentage = parseInt(left / dom.offsetWidth * 100);
                animeMusic.PlayTo(percentage);
            }
        }
        else {
            console.log('dom is not exists');
        }
    },
    'onPlay': null,
    'onPlayed': null,
    'onPause': null,
    'onPaused': null,
    'onLoad': null,
    'onLoaded': null,
    'onProgress': null
};

function secondToDate(result) {
    var m = Math.floor((result / 60 % 60)) < 10 ? '0' + Math.floor((result / 60 % 60)) : Math.floor((result / 60 % 60));
    var s = Math.floor((result % 60)) < 10 ? '0' + Math.floor((result % 60)) : Math.floor((result % 60));
    ret = m + ":" + s;
    return ret == 'NaN:NaN' ? '00:00' : ret;
}

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

animeMusic._anime_music_player.onended = function () {
    animeMusic.Next();
};