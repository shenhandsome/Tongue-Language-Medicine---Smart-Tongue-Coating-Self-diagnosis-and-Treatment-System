//获取应用实例
var config = require("../../config.js");

Page({

  onLoad: function (options) {
    var that = this;
    that.setData({
      healthknos: config.healthknos[options.id - 1]
    });
  },
})