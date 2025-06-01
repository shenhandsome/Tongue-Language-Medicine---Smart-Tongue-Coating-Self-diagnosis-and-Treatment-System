//获取应用实例
const app = getApp()
var util = require("../../util.js");
var config = require("../../config.js");
Page({
    data: {
        imagelist: ["/static/image/healthknos/4.jpg"],

        navData: [{
            text: '舌苔分析'
        }, {
            text: '调理建议'
        }],
        report: [{
                tongue_proper_color: app.globalData.tonguefeature
            },
            {
                suggest: "对照表征分析进行调理"
            },
        ],
        currentTab: 0,
        navScrollLeft: 0,
    },

    switchNav(event) {
        var cur = event.currentTarget.dataset.current;
        var singleNavWidth = this.data.windowWidth / 2;                           
        this.setData({
            navScrollLeft: (cur - 2) * singleNavWidth
        })
        if (this.data.currentTab == cur) {
            return false;
        } else {
            this.setData({
                currentTab: cur
            })
        }
    },
    switchTab(event) {
        var cur = event.detail.current;
        var singleNavWidth = this.data.windowWidth / 2;
        this.setData({
            currentTab: cur,
            navScrollLeft: (cur - 2) * singleNavWidth
        });
    },

    onLoad: function(options) {
      // 获取传递过来的参数
      var time = util.formatTime(new Date());
      var answer = decodeURIComponent(options.answer);
      var response_text = decodeURIComponent(options.response_text);
      // 更新页面数据
      this.setData({
        answer: answer,
        response_text: response_text,
        time: time
      });
    }
})