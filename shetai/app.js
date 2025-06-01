App({
  onLaunch: function () {
    wx.getSystemInfo({
      success: e => {
        this.globalData.StatusBar = e.statusBarHeight;
      }
    })
  },

  globalData: {
    isUse:false,  
    userInfo: {},
    hasUserInfo: false,
    imagelist: [], 
    imagecount: 0,
    mHidden:false,

    // 记录特征
    tonguefeature:[[],[],[],[],[],[]],
  },
})