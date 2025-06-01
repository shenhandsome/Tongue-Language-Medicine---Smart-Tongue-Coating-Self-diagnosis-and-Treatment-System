var app = getApp();
var config = require("../../config.js");
Page({
  data: {
    CustomBar: app.globalData.CustomBar,
    hidden: true,
    current: 0,
    lines: 0,

    indicatorDots: true,
    vertical: false,
    autoplay: true,
    interval: 3000,
    duration: 1200,

    iconList: [{
      id: 1,
      url: '/pages/tongue/tongue',
      image: '/static/image/11.png',
      text: '舌苔自诊'
    }, {
      id: 2,
      url: '/pages/ai/ai',
      image: '/static/image/12.png',
      text: 'AI问诊'
    }, {
      id: 3,
      url: '/pages/med/med',
      image: '/static/image/13.png',
      text: '灵药库'
    }
  ],
  },

  swiperchange: function (e) {
    this.setData({
      current: e.detail.current
    });
  },

  gotopage: function (event) {
    wx.reLaunch({
      url: event.currentTarget.dataset.url
    });
  },

  onLoad: function (options) {
    var that = this;
    that.setData({
      healthknos: config.healthknos,
      swiperlist:config.swiperlist
    });
  },


  onShareAppMessage: function () {
    return {
      title: '舌语医说',
      desc: '助力智慧医疗发展',
      imageUrl:"/static/image/logo.jpg",
      path: '/page/index/index'
    }
  },
})